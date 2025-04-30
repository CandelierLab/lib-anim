import os
import inspect
import numpy as np
import imageio
from PyQt6.QtCore import pyqtSignal, QTimer
from PyQt6.QtGui import QKeySequence, QImage, QShortcut, QGuiApplication
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout

import anim 

class window(QWidget):
  '''
  Animation-specific window.

  Subclass of Qwidget. Creates a new window containing an animation.
  
  Attributes:
    title (string): Title of the window.
    app (QApplication): Underlying QApplication.
    anim (`Animation2d`): Animation to display.
    layout (QGridLayout): The main layout.
    information (`Information`): The object controlling the extra information displayed.
    width (?): width of the window (in ?)
    height (?): height of the window (in ?)
    fpt (int): The windows' fps. Default: 25.
    step (int):
    dt (float):
    timer (QTime)
    allow_backward (bool):
  '''

  # Generic event signal
  signal = pyqtSignal(dict)
  ''' A pyqtSignal object to manage external events.'''

  # ========================================================================
  def __init__(self, 
               title='Animation', 
               display_information=True, 
               autoplay=True, 
               dt=None, 
               style='dark', 
               height=0.75):
    '''
    Creates a new window
    
    * Initializes a QApplication in :py:attr:`self.app`
    * Defines the window layout in :py:attr:`self.layout`
    
    The dark style is set by defaut (if the corresponding stylesheet is found).

    Args:
      title (string): . Default: 'Animation'.
      display_information (bool): Determines if the extra information have to be displayed. Default: True.
      autoplay (bool): Indicating if autoplay is on or off. Default: True.
      dt (frames): time increment between two frames (in seconds). Default: None.
      style   ['dark', 'light', 'white']
    '''

    # Qapplication
    self.app = QApplication([])
    '''The qApplication of the animation window'''

    # Attributes
    self.title = title

    # Misc private properties
    self._nAnim = 0
    self._movieCounter = 0
    
    # Call widget parent's constructor (otherwise no signal can be caught)
    super().__init__()

    # --- Main Layout

    self.layout = QGridLayout()
    self.setLayout(self.layout)

    self.layout.setSpacing(0)
    # self.layout.setContentsMargins(0,0,0,0)

    # Window size
    if height<=1:
      self.height = int(self.app.screens()[0].size().height()*height);      
    else:
      self.height = int(height)
    self.width = None

    self.aspect_ratios = []

    # --- Style

    self.style = style

    with open(os.path.dirname(os.path.abspath(__file__)) + f'/style/{self.style}.css', 'r') as f:
      css = f.read()
      self.app.setStyleSheet(css)

    # --- Information

    if display_information:

      self.information = anim.information(self)
    
      self.layout.addWidget(self.information.view, 0, 0)
      self.signal.connect(self.information.receive)
      self.information.signal.connect(self.capture)
      self._nAnim += 1

      self.aspect_ratios.append(self.information.aspect_ratio)

    else:
      self.information = None
    
    # --- Timing

    # Framerate
    self.fps = 25

    # Time
    self.step = 0
    self.dt = dt if dt is not None else 1/self.fps

    # Timer
    self.timer = QTimer()
    self.timer.timeout.connect(self.set_step)

    # Play
    self.autoplay = autoplay
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
    
  # ========================================================================
  def add(self, panel, row=None, col=None):
    """ 
    Add a panel or a layout
    """

    # --- Default row / column

    if row is None:
      row = self.layout.rowCount()-1

    if col is None:
      col = self.layout.columnCount()

    # --- Instantiate classes

    if inspect.isclass(panel):
      panel = panel(self)

    # --- Append panel or layout

    if isinstance(panel, anim.plane.panel):

      self.layout.addWidget(panel.view, row, col)
      self.signal.connect(panel.receive)
      panel.signal.connect(self.capture)
      self._nAnim += 1

      self.aspect_ratios.append(panel.aspect_ratio)

    else:

      self.layout.addLayout(panel, row, col)

  # ========================================================================
  def show(self):
    """
    Display the animation window
    
    * Display the animation
    * Defines the shortcuts
    * Initialize and start the animation
    """

    # --- Settings ---------------------------------------------------------
    
    # Window title
    self.setWindowTitle(self.title)

    # --- Shortcuts

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

    # --- Display animation ------------------------------------------------

    super().show()
    self.signal.emit({'type': 'show'})

    # --- Sizing

    # Default size
    if self.height is None:
      self.height = int(self.information.viewHeight)

    if self.width is None:
      self.width = int(self.height*np.sum(self.aspect_ratios)) + 35

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

 # ========================================================================
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

  # ========================================================================
  def capture(self, force=False):

    if self.movieWriter is not None and not (self.step % self.keep_every):

      self._movieCounter += 1

      if force or self._movieCounter == self._nAnim:

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

  # ========================================================================
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

  # ========================================================================
  def increment(self):

    self.play_forward = True

    if not self.timer.isActive():
      self.set_step()

  # ========================================================================
  def decrement(self):

    if self.allow_backward:

      self.play_forward = False

      if not self.timer.isActive():
        self.set_step()

  # ========================================================================
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
