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
  def __init__(self, window:anim.window,
               boundaries = None,
               display_boundaries = True, 
               boundaries_color = None,
               boundaries_thickness = None,
               padding = 0,
               background_color = '#181818',
               pixelperunit = 1,
               grid = None):
    '''
    Canva constructor
    '''

    # Parent constructor
    super().__init__()

    # Window
    self.window = window

    # ─── Scene boundaries

    if boundaries_color is None:
      match self.window.style:
        case 'white' | 'light': boundaries_color = 'black'
        case _: boundaries_color = 'white'
    
    self._boundaries = anim.core.boundingBox(display_boundaries, boundaries, boundaries_color, boundaries_thickness)

    # ─── Qt elements

    # Scene (root entity)
    self.scene = QEntity()

    # # Material.
    # material = QPhongMaterial(self.scene)

    # # # Torus.
    # # torusEntity = QEntity(rootEntity)
    # # torusMesh = QTorusMesh()
    # # torusMesh.setRadius(5)
    # # torusMesh.setMinorRadius(1)
    # # torusMesh.setRings(100)
    # # torusMesh.setSlices(20)

    # # torusTransform = QTransform()
    # # torusTransform.setScale3D(QVector3D(1.5, 1.0, 0.5))
    # # torusTransform.setRotation(
    # #         QQuaternion.fromAxisAndAngle(QVector3D(1.0, 0.0, 0.0), 45.0))

    # # torusEntity.addComponent(torusMesh)
    # # torusEntity.addComponent(torusTransform)
    # # torusEntity.addComponent(material)

    # # Sphere.
    # sphereEntity = QEntity(self.scene)
    # sphereMesh = QSphereMesh()
    # sphereMesh.setRadius(3)

    # sphereEntity.addComponent(sphereMesh)
    # sphereEntity.addComponent(material)

    # View
    self.view = anim.core.view3d(self.scene)

    # Pixels per scene unit
    self.pixelperunit = pixelperunit

    # ─── Background color

    fg = self.view.qt3dwindow.defaultFrameGraph()
    if isinstance(background_color, str):
      fg.setClearColor(QColor(background_color))
    elif isinstance(background_color, QColor):
      fg.setClearColor(background_color)
    
    # ─── Display items ────────────────────────────

    self.item = anim.core.itemDict(self) 
      
    # ─── Dummy boundary rectangle ──────────────

    # # # self.bounds = QGraphicsRectItem(self.boundaries.x0*self.pixelperunit, 
    # # #                            self.boundaries.y0*self.pixelperunit,
    # # #                            self.boundaries.width*self.pixelperunit,
    # # #                            self.boundaries.height*self.pixelperunit)
    
    # # # self.scene.addItem(self.bounds)
    # # # self.setBoundaryStyle()

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t=None):
    """
    Update animation state
    """

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
  def event(self, item, desc):
    '''
    Event notification

    This method is triggered whenever an event occurs.
    It has to be reimplemented in subclasses.

    args:
      type (str): Event type (``move``).
      item (:class:`item` *subclass*): The changed item.
    '''
    pass
  
  # ────────────────────────────────────────────────────────────────────────
  def stop(self):
    '''
    Stop notification

    This method is triggered when the window is closed.
    It does nothing and has to be reimplemented in subclasses.
    '''
    pass