import os
import inspect
import numpy as np
import imageio
from PyQt6.QtCore import pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QKeySequence, QImage, QShortcut
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QSizeGrip

import anim 

class window(QMainWindow):
  '''
  Animation-specific window.
  '''

  # Generic event signal
  signal = pyqtSignal(dict)
  ''' A pyqtSignal object to manage external events.'''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, 
               title = 'Animation', 
               style = 'dark',
               height = 0.75,
               aspect_ratio = 1,
               display_information = True):
    '''
    Creates a new window.
        
    The dark style is set by defaut (if the corresponding stylesheet is found).
    '''

    # Qapplication
    self.app = QApplication([])
    '''The qApplication of the animation window'''

    # Attributes
    self.title = title

    # Misc private properties
    self._nCanva = 0
    self._movieCounter = 0
    
    # Call widget parent's constructor (otherwise no signal can be caught)
    super().__init__()

    # ─── Main widged and layout ────────────────

    # Window size
    self.height = height
    self.width = None
    self.aspect_ratio = aspect_ratio
    ''' The aspect ratio is the window's width / height. '''

    # Main widget
    self.mainWidget = QWidget()
    self.setCentralWidget(self.mainWidget)

    # ─── Grid layout ───────────────────────────

    self.layout = QGridLayout()
    self.mainWidget.setLayout(self.layout)

    # Default layout spacing
    self.layout.setSpacing(0)

    # Strech ratios
    self.rowHeights = None
    self.colWidths = None

    # ─── Style ─────────────────────────────────

    self.style = style

    with open(os.path.dirname(os.path.abspath(__file__)) + f'/style/{self.style}.css', 'r') as f:
      css = f.read()
      self.app.setStyleSheet(css)

    # ─── Information panel ─────────────────────

    if display_information:

      self.information = anim.information(self)
    
      self.layout.addWidget(self.information.view, 0, 0)
      self.signal.connect(self.information.receive)
      self.information.signal.connect(self.capture)
      self._nCanva += 1

    else:
      self.information = None
    
    # --- Timing

    # Framerate
    self.fps = 25

    # Time
    self.step = 0
    self.dt = 1/self.fps

    # Timer
    self.timer = QTimer()
    self.timer.timeout.connect(self.set_step)

    # Play
    self.autoplay = True
    self.step_max = None
    self.allow_backward = False
    self.allow_negative_time = False
    
    self.play_forward = True

    # --- Output 

    # Movie
    self.movieFile = None
    self.movieWriter = None
    self.movieWidth = 1600     # Must be a multiple of 16
    self.moviefps = 25
    self.keep_every = 1

  # def add_test(self):

  #   from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsRectItem
  #   from PyQt6.QtGui import QBrush

  #   # Define app and scene
  #   scene = QGraphicsScene(0, 0, 500, 500)

  #   # Create a red square
  #   rect = QGraphicsRectItem(100, 100, 100, 100)
  #   rect.setBrush(QBrush(Qt.GlobalColor.red))

  #   rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
  #   # rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

  #   # rect.setCacheMode(QGraphicsItem.CacheMode.ItemCoordinateCache)
  #   # rect.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)

  #   # Display
  #   scene.addItem(rect)
  #   view = QGraphicsView(scene)

  #   self.layout.addWidget(view, 0 , 0)

  # ────────────────────────────────────────────────────────────────────────
  def add(self, canva, row=None, col=None, **kwargs):
    """ 
    Add a canva or a layout
    """

    # ─── Default row / column ──────────────────

    '''
    NB: rowCount() and columnCount() will always return a number equal or
    greater than 1, even if the layout is empty. We therefore have to compute 
    the 'real' number of rows and columns occupied.
    '''

    if row is None or col is None:
      nextrow = 0
      nextcol = 0
      for i in range(self.layout.count()):
        r, c, rspan, cspan = self.layout.getItemPosition(i)
        nextrow = max(nextrow, r + rspan)
        nextcol = max(nextcol, c + cspan)

      if row is None: row = max(0, nextrow-1)
      if col is None: col = nextcol

    # ─── Instantiate class ─────────────────────

    if inspect.isclass(canva):
      canva = canva(self, **kwargs)

    # ─── Append canva or layout ────────────────

    if isinstance(canva, anim.plane.canva):

      self.layout.addWidget(canva.view, row, col)
      self.signal.connect(canva.receive)
      canva.signal.connect(self.capture)
      self._nCanva += 1

    else:

      self.layout.addLayout(canva, row, col)

  # ────────────────────────────────────────────────────────────────────────
  def compute_canva_size(self, canva):

    for i in range(self.layout.count()):
      r, c, rspan, cspan = self.layout.getItemPosition(i)
      nextrow = max(nextrow, r + rspan)
      nextcol = max(nextcol, c + cspan)

    print(canva.vspan)

    return None

  # ────────────────────────────────────────────────────────────────────────
  def show(self):
    """
    Display the animation window
    
    * Display the animation
    * Defines the shortcuts
    * Initialize and start the animation
    """

    # ─── Settings ──────────────────────────────
    
    # Window title
    self.setWindowTitle(self.title)

    # Window flags
    self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMinimizeButtonHint)
    self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
       
    # ─── Shortcuts

    self.shortcut = {}

    # Quit
    self.shortcut['esc'] = QShortcut(QKeySequence('Esc'), self)
    self.shortcut['esc'].activated.connect(self.close)

    # Play/pause
    self.shortcut['space'] = QShortcut(QKeySequence('Space'), self)
    self.shortcut['space'].activated.connect(self.play_pause)

    # Decrement
    self.shortcut['previous'] = QShortcut(QKeySequence.StandardKey.MoveToPreviousChar, self)
    self.shortcut['previous'].activated.connect(self.decrement)

    # Increment
    self.shortcut['next'] = QShortcut(QKeySequence.StandardKey.MoveToNextChar, self)
    self.shortcut['next'].activated.connect(self.increment)

    # ─── Window display ────────────────────────

    super().show()
    self.signal.emit({'type': 'show'})

    # ─── Sizing

    # Height
    if self.height<=1:
      self.height = self.app.screens()[0].size().height()*self.height
    self.height = int(self.height)

    # Compute width
    if self.width is None:
      self.width = int(self.height*self.aspect_ratio)

    # Set window size
    self.resize(self.width, self.height)

    # --- Timing -----------------------------------------------------------

    # Timer settings
    self.timer.setInterval(int(1000*self.dt))

    # Autoplay
    if self.autoplay:
      self.play_pause()
    
    # --- Movie ------------------------------------------------------------

    if self.movieFile is not None:

      # Check directory
      dname = os.path.dirname(self.movieFile)
      if not os.path.isdir(dname):
        os.makedirs(dname)

      # Open video file
      self.movieWriter = imageio.get_writer(self.movieFile, fps=self.moviefps)

      # Capture first frame
      self.capture(force=True)

    self.app.exec()

  # ────────────────────────────────────────────────────────────────────────
  def set_step(self, step=None):

    if step is None:
      self.step += 1 if self.play_forward else -1
    else:
      self.step = step

    # Check negative times
    if not self.allow_negative_time and self.step<0:
      self.step = 0

    # Check excessive times
    if self.step_max is not None and self.step>self.step_max:
        self.step = self.step_max
        self.play_pause()
        return
        
    # Emit event
    self.signal.emit({'type': 'update', 'time': anim.time(self.step, self.step*self.dt)})

  # ────────────────────────────────────────────────────────────────────────
  def capture(self, force=False):

    if self.movieWriter is not None and not (self.step % self.keep_every):

      self._movieCounter += 1

      if force or self._movieCounter == self._nCanva:

        # Reset counter
        self._movieCounter = 0

        # Get image
        img = self.grab().toImage().scaledToWidth(self.movieWidth).convertToFormat(QImage.Format.Format_RGB888)

        # Create numpy array
        ptr = img.constBits()
        ptr.setsize(img.height()*img.width()*3)
        A = np.frombuffer(ptr, np.uint8).reshape((img.height(), img.width(), 3))

        # Add missing rows (to get a height multiple of 16)
        A = np.concatenate((A, np.zeros((16-img.height()%16, img.width(), 3), dtype=np.uint8)), 0)
        
        # Append array to movie
        self.movieWriter.append_data(A)

  # ────────────────────────────────────────────────────────────────────────
  def play_pause(self, force=None):

    if self.timer.isActive():

      # Stop qtimer
      self.timer.stop()

      # Emit event
      self.signal.emit({'type': 'pause'})

    else:

      # Start timer
      self.timer.start()
    
      # Emit event
      self.signal.emit({'type': 'play'})

  # ────────────────────────────────────────────────────────────────────────
  def increment(self):

    self.play_forward = True

    if not self.timer.isActive():
      self.set_step()

  # ────────────────────────────────────────────────────────────────────────
  def decrement(self):

    if self.allow_backward:

      self.play_forward = False

      if not self.timer.isActive():
        self.set_step()

  # ────────────────────────────────────────────────────────────────────────
  def close(self):
    """
    Stop the animation

    Stops the timer and close the window
    """

    # Stop the timer
    self.timer.stop()

    # Emit event
    self.signal.emit({'type': 'stop'})

    # Movie
    if self.movieWriter is not None:
      self.movieWriter.close()

    self.app.quit()
