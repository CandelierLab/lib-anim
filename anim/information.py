import re
import anim

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QDockWidget, QVBoxLayout, QLabel

class information:
    
  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window, width=0.25):

    # ─── Definitions ───────────────────────────

    # Set window
    self.window:anim.window = window

    # Dock width
    self.width = width

    # Display state
    self._display = False

    # Strings
    self.time = ''
    self.html = ''

    # ─── QWidgets ──────────────────────────────

    # ─── Dock

    self.dock = QDockWidget('', self.window)
    self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
    self.window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
    
    '''Custom size hints, minimum and maximum sizes and size policies
    should be implemented in the child widget'''

    # self.dock.setWindowTitle('dock title')

    # ─── Vertical layout

    self.dock.setWidget(QWidget())
    self.layout = QVBoxLayout(self.dock.widget())
       
    # ─── Label

    self.label = QLabel()
    self.layout.addWidget(self.label)

    self.setHtml()

    self.layout.addStretch()

  # ────────────────────────────────────────────────────────────────────────
  def setWidth(self, windowHeight):

    width = int(self.width*windowHeight)
    self.dock.widget().setMinimumWidth(width)
    self.dock.widget().setMaximumWidth(width)

    return width

  # ────────────────────────────────────────────────────────────────────────
  def display(self, state='toggle'):
    '''
    Defines if the dock is displayed or not
    '''

    # Display state
    if state=='toggle':
      self._display = not self._display
    else:
      self._display = state

    # Set visibility
    self.dock.setVisible(self._display)

    # Update window size
    self.window.setWindowSize()

  # ────────────────────────────────────────────────────────────────────────
  def setTime(self, signal):
    '''
    Format time string for display
    '''

    match signal.type:

      case 'show' | 'update':

        step = signal.time.step if hasattr(signal, 'time') else 0
        time = signal.time.time if hasattr(signal, 'time') else 0
    
        s = '<table width="100%"><tr><td align=center>step</td><td align=center>time</td></tr><tr>'
        s += f'<th align=center style="color:lightgrey;">{step}</th>'
        s += f'<th align=center style="color:lightgrey;">{time:.02f} sec</th>'
        s += '</tr></table><hr style="background-color:grey;">'
        self.time = s

        self.setHtml()

  # ────────────────────────────────────────────────────────────────────────
  def setHtml(self, html=None):

    if html is not None:
      self.html = html

    self.label.setText(self.time + self.html)