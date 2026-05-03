from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QSplitter
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QImage, QMatrix4x4, QQuaternion, QVector3D, QColor, QGuiApplication
from PyQt6.QtCore import QSize, Qt
import sys
from PyQt6.Qt3DCore import QEntity, QTransform, QAspectEngine
from PyQt6.Qt3DRender import QCamera, QCameraLens, QRenderAspect
from PyQt6.Qt3DInput import QInputAspect
from PyQt6.Qt3DExtras import QForwardRenderer, QPhongMaterial, QCylinderMesh, QSphereMesh, QTorusMesh, Qt3DWindow, QOrbitCameraController

import anim
  
class canva(QObject):

  # Events
  signal = pyqtSignal()

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window:anim.window):
    '''
    Canva constructor
    '''

    # Parent constructor
    super().__init__()

    # Window
    self.window = window

    # View
    self.view = anim.core.viewplot()
    
  # ────────────────────────────────────────────────────────────────────────
  def update(self, t=None):
    """
    Update animation state
    """

    # Repaint
    # self.view.viewport().repaint()

    # Confirm update
    self.signal.emit()

  # ────────────────────────────────────────────────────────────────────────
  def receive(self, event):
    """
    Event reception
    """

    match event.type:

      case 'show':
        
        pass

      case 'update':

        # Update dispay
        self.update(event.time)

      case 'stop':
        self.stop()

      case _:
        # print(event)
        pass

  # ────────────────────────────────────────────────────────────────────────
  def stop(self):
    '''
    Stop notification

    This method is triggered when the window is closed.
    It does nothing and has to be reimplemented in subclasses.
    '''
    pass