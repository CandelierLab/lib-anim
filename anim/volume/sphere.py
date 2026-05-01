from PyQt6.QtGui import QColor
from PyQt6.Qt3DCore import QEntity
from PyQt6.Qt3DExtras import QSphereMesh, QDiffuseSpecularMaterial


from .item import item

# ══════════════════════════════════════════════════════════════════════════
#                                 SPHERE
# ══════════════════════════════════════════════════════════════════════════
   
class sphere(item):
  '''
  A sphere item is defined by its:

  - radius
  - position of the point of reference
  - styling
  
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, radius):
    '''
    Sphere item constructor
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
    self.material = QDiffuseSpecularMaterial(self.canva.scene)
    self.material.setAmbient(QColor('red'))
    self.entity.addComponent(self.material)

    # Geometry
    self.setGeometry()

  # ────────────────────────────────────────────────────────────────────────
  def setGeometry(self):
    '''
    Set the sphere's geometry
    '''

    # Check entity
    if self.entity is None: return

    # ─── Mesh

    if self.mesh is not None:
      # Mesh already exists: just update the radius in place
      self.mesh.setRadius(self._radius)
    else:
      # First time: create the mesh with the entity as parent to prevent GC
      self.mesh = QSphereMesh(self.entity)
      self.mesh.setRadius(self._radius)
      self.entity.addComponent(self.mesh)

  # ─── radius ─────────────────────────────────────────────────────────────
  
  @property
  def radius(self): return self._radius

  @radius.setter
  def radius(self, r):
    self._radius = abs(r)
    self.setGeometry()
    
    

