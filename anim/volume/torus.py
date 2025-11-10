from PyQt6.QtGui import QColor
from PyQt6.Qt3DCore import QEntity
from PyQt6.Qt3DExtras import QTorusMesh, QDiffuseSpecularMaterial

from .item import item

# ══════════════════════════════════════════════════════════════════════════
#                                 TORUS
# ══════════════════════════════════════════════════════════════════════════
   
class torus(item):
  '''
  A torus item is defined by its:

  - radius
  - position of the point of reference
  - styling
  
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, radius):
    '''
    Item constructor
    '''  

    # Parent constructors
    item.__init__(self)

    # ─── Internal properties

    self.mesh = None
    self._radius = radius

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the sphere

    At this point:
    - the canva should be defined (automatically managed by itemDict)
    - the qitem should be defined (managed by the children class)
    '''

    # Parent initialization
    item.initialize(self)

    # Entity
    self.entity = QEntity(self.canva.scene)

    # Material
    material = QDiffuseSpecularMaterial(self.canva.scene)
    material.setAmbient(QColor('red'))
    self.entity.addComponent(material)

    # Geometry
    self.setGeometry()

  # ────────────────────────────────────────────────────────────────────────
  def setGeometry(self):
    '''
    Set the item's geometry
    '''

    # Check entity
    if self.entity is None: return

    # ─── Mesh

    # Remove current mesh
    if self.mesh is not None:
      self.entity.removeComponent(self.mesh)

    # Define mesh
    self.mesh = QTorusMesh()

    # Set radius
    self.mesh.setRadius(self._radius)
    self.mesh.setMinorRadius(1)
    self.mesh.setRings(100)
    self.mesh.setSlices(20)

    # Add mesh component
    self.entity.addComponent(self.mesh)

  # ─── radius ─────────────────────────────────────────────────────────────
  
  @property
  def radius(self): return self._radius

  @radius.setter
  def radius(self, r):
    self._radius = abs(r)
    self.setGeometry()
    
    

