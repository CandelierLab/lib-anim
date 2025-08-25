from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QVector3D, QColor
from PyQt6.QtWidgets import QWidget, QGraphicsView, QGridLayout

from PyQt6.Qt3DCore import QEntity, QTransform
from PyQt6.Qt3DExtras import QPhongMaterial, QSphereMesh, QTorusMesh, Qt3DWindow, QOrbitCameraController

from .boundingBox import boundingBox

# ══════════════════════════════════════════════════════════════════════════
#                                 2D VIEW
# ══════════════════════════════════════════════════════════════════════════

class view2d(QGraphicsView):
    
  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, scene, boundaries:boundingBox, pixelperunit, padding=0, *args, **kwargs):

    # Parent constructor
    super().__init__(*args, *kwargs)

    # ─── View and scene

    self.ppu = float(pixelperunit)
    self.padding = padding

    # Disable scrollbars
    self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    # Antialiasing
    self.setRenderHints(QPainter.RenderHint.Antialiasing)

    # Scene
    self.setScene(scene)

    # ─── Boundaries

    self.boundaries = boundaries
    # if self.boundaries.display:
    #   self.setStyleSheet(f'border: {self.boundaries.thickness}px solid {self.boundaries.color};')

  # ────────────────────────────────────────────────────────────────────────
  def fit(self):

    self.fitInView(QRectF(0, 0,
                          (self.boundaries.width + 2*self.padding)*self.ppu,
                          (self.boundaries.height + 2*self.padding)*self.ppu),
                   Qt.AspectRatioMode.KeepAspectRatio)
    
    # self.centerOn(QPointF(self.boundaries.x0 + self.boundaries.width/2,
    #                       self.boundaries.y0 + self.boundaries.height/2))
    
    self.setSceneRect(QRectF((self.boundaries.x0 - self.padding)*self.ppu,
                             (self.boundaries.y0 - self.padding)*self.ppu,
                             (self.boundaries.width + 2*self.padding)*self.ppu,
                             (self.boundaries.height + 2*self.padding)*self.ppu))
    
    # self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.NoViewportUpdate)

  # ────────────────────────────────────────────────────────────────────────
  def showEvent(self, event):

    self.fit()    
    super().showEvent(event)

  # ────────────────────────────────────────────────────────────────────────
  def resizeEvent(self, event):
    
    self.fit()
    super().resizeEvent(event)

  # ────────────────────────────────────────────────────────────────────────
  def wheelEvent(self, event):
    '''
    Capture the wheel events to avoid scene motion.
    '''
    pass

# ══════════════════════════════════════════════════════════════════════════
#                                 3D VIEW
# ══════════════════════════════════════════════════════════════════════════

class view3d(QWidget):

  def __init__(self, scene):
      
    super().__init__()

    # Qt3d window object
    self.qt3dwindow = Qt3DWindow()

    # Layout
    layout = QGridLayout()
    layout.addWidget(self.createWindowContainer(self.qt3dwindow))
    self.setLayout(layout)

    # Assign scene
    self.scene = scene
    self.qt3dwindow.setRootEntity(self.scene)

    camera = self.qt3dwindow.camera()
    camera.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000.0)
    camera.setPosition(QVector3D(0.0, 0.0, 40.0))
    camera.setViewCenter(QVector3D(0.0, 0.0, 0.0))

    # For camera controls
    camController = QOrbitCameraController(self.scene)
    camController.setLinearSpeed(50.0)
    camController.setLookSpeed(180.0)
    camController.setCamera(camera)

