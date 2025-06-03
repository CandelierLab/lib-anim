import os
import inspect
import numpy as np
import imageio

from PyQt6.QtCore import pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QKeySequence, QImage, QShortcut
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout

import anim 

class window(QMainWindow):
  '''
  Animation-specific window.
  '''

  # Generic event signal
  signal = pyqtSignal(object)
  ''' A pyqtSignal object to manage external events.'''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, 
               title = 'Animation', 
               style = 'dark',
               height = 0.75,
               width = None,
               aspect_ratio = 1,
               information = None):
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

    # Window size
    self.height = height
    self.width = width
    self.aspect_ratio = aspect_ratio
    ''' The aspect ratio is the window's width / height. '''
    
    # ─── Layout ───────────────────────────────────────────────────────────

    # ─── Docks ─────────────────────────────────

    # Information panel
    self.information = anim.information(self) if information is None else information(self)

    # ─── Main widget and grid layout ───────────

    # Main widget
    self.mainWidget = QWidget()
    self.setCentralWidget(self.mainWidget)

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
    
    # ─── Timing ────────────────────────────────

    # Framerate
    self.fps = 25

    # Time
    self.step = 0
    self.dt = 1/self.fps

    # Timer
    self.timer = QTimer()
    self.timer.timeout.connect(self.setStep)

    # Play
    self.autoplay = True
    self.step_max = None
    self.allow_backward = False
    self.allow_negative_time = False
    
    self.play_forward = True

    # ─── Video output ──────────────────────────

    # Movie
    self.movieFile = None
    self.movieWriter = None
    self.movieWidth = 1600     # Must be a multiple of 16
    self.moviefps = 25
    self.keep_every = 1

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
       
    # ─── Information panel ─────────────────────
    
    # Connect display signal
    self.signal.connect(self.information.setTime)

    # Initial display
    self.information.display(self.information._display)

    # ─── Shortcuts ─────────────────────────────

    self.shortcut = {}

    # Quit
    self.shortcut['esc'] = QShortcut(QKeySequence('Esc'), self)
    self.shortcut['esc'].activated.connect(self.close)

    # Information panel
    self.shortcut['info'] = QShortcut(QKeySequence('i'), self)
    self.shortcut['info'].activated.connect(self.information.display)

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
    self.signal.emit(self.signalObject({'type' : 'show'}))

    # Sizing
    self.setWindowSize()

    # ─── Timing ────────────────────────────────    

    # Timer settings
    self.timer.setInterval(int(1000*self.dt))

    # Autoplay
    if self.autoplay:
      self.play_pause()
    
    # ─── Video output ──────────────────────────
    
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
  def setWindowSize(self):

    # Height
    if self.height<=1:
      height = self.app.screens()[0].size().height()*self.height

    # Compute width
    if self.width is None:

      # Main layout
      width = height*self.aspect_ratio

      # Information panel
      if self.information._display:
        width += self.information.setWidth(height)
      
    else: 
      width = self.app.screens()[0].size().width()*self.width

    # Set window size
    self.resize(int(width), int(height))

  # ────────────────────────────────────────────────────────────────────────
  def setStep(self, step=None):

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
    self.signal.emit(self.signalObject({'type': 'update', 'time': anim.time(self.step, self.step*self.dt)}))

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
      self.signal.emit(self.signalObject({'type': 'pause'}))

    else:

      # Start timer
      self.timer.start()
    
      # Emit event
      self.signal.emit(self.signalObject({'type': 'play'}))

  # ────────────────────────────────────────────────────────────────────────
  def increment(self):

    self.play_forward = True

    if not self.timer.isActive():
      self.setStep()

  # ────────────────────────────────────────────────────────────────────────
  def decrement(self):

    if self.allow_backward:

      self.play_forward = False

      if not self.timer.isActive():
        self.setStep()

  # ────────────────────────────────────────────────────────────────────────
  def close(self):
    """
    Stop the animation

    Stops the timer and close the window
    """

    # Stop the timer
    self.timer.stop()

    # Emit event
    self.signal.emit(self.signalObject({'type': 'stop'}))


    # Movie
    if self.movieWriter is not None:
      self.movieWriter.close()

    self.app.quit()

  # ────────────────────────────────────────────────────────────────────────
  @staticmethod
  def signalObject(d):
    return type('signal_object', (object,), d)

  # # ────────────────────────────────────────────────────────────────────────
  # def compute_canva_size(self):

  #   for i in range(self.layout.count()):
  #     r, c, rspan, cspan = self.layout.getItemPosition(i)
  #     nextrow = max(nextrow, r + rspan)
  #     nextcol = max(nextcol, c + cspan)

  #   return None