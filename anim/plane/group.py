from PyQt6.QtWidgets import QGraphicsItemGroup

from .item import item
from .itemDict import itemDict
from .events import event

class group(item):
  '''
  Group item

  A group item has no representation upon display but serves as a parent for
  multiple other items in order to create and manipulate compositions.

  Note on rotation: 
    Be carefull to rotate the group AFTER having added the items.

  Parameters
  ══════════

    * name       
        str
        The group name.

    * group
        anim.plane.group
        default: None
        The group's group. If None, the position of the reference point and
        center of rotation are in absolute coordinates. Otherwise, the
        position is relative to the parent group's reference point.

    ─── position ────────────────────────────────

    * x           
        float
        default: 0
        x-position of the reference point.

    * y
        float
        default: 0
        y-position of the reference point.

    * position
        (float, float), [float, float], complex
        default: [0,0]
        Position of the reference point. The user can define either x, y or
        the position. In case of conflict, the position attribute wins.

    ─── transformations ─────────────────────────

    * orientation
        float
        default: 0, unit: radians
        Orientation of the item, with respect to the positive part of the 
        x-axis.

    * center_of_rotation
        None, (float, float), [float, float], complex
        default: None
        Center point for the rotation.

    * draggable
        bool
        default: False
        Boolean specifying if the item can be dragged. If True, the dragging
        callback is defined in the 'itemChange' method of the event class,
        which is transfered to the canva's 'event' method (recommended).

    ─── stack ───────────────────────────────────

    * zvalue
        float
        default: 0
        Z-value (stack order) of the item.

  Methods
  ═══════
  
    * Lx(): return the group's total width
    * Ly(): return the group's total height
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self,
               group = None,
               x = 0,
               y = 0,
               position = None,
               center_of_rotation = [0,0],
               orientation = 0,
               zvalue = 0,
               draggable = False):
    '''
    Group item constructor

    Defines a group, which inherits both from ``QGraphicsItemGroup`` and
    :class:`item`.
    '''  

    # ─── Parent constructor
    
    item.__init__(self, 
                  group = group,
                  x = x,
                  y = y,
                  position = position,
                  center_of_rotation = center_of_rotation,
                  orientation = orientation,
                  zvalue = zvalue,
                  draggable = draggable)

    # ─── QGraphicsItem
    
    class QGroup(QGraphicsItemGroup, event): pass
    self.qitem = QGroup()


  # # ────────────────────────────────────────────────────────────────────────
  # def initialize(self):
  #   '''
  #   Initialize the item

  #   This method is meant to be overloaded and called.
  #   At this point:
  #   - the canva should be defined (automatically managed by itemDict)
  #   - the qitem should be defined (managed by the children class)
  #   '''

  #   # Generic item initialization
  #   super().initialize()



  # ────────────────────────────────────────────────────────────────────────
  def Lx(self):
    return self.qitem.childrenBoundingRect().width()/self.ppu

  # ────────────────────────────────────────────────────────────────────────
  def Ly(self):
    return self.qitem.childrenBoundingRect().height()/self.ppu

# ══════════════════════════════════════════════════════════════════════════
#                                COMPOSITES
# ══════════════════════════════════════════════════════════════════════════

class composite(group):
  '''
  Composite  item
  '''

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the composite

    At this point:
    - the canva should be defined (automatically managed by itemDict)
    - the qitem should be defined (managed by the children class)
    '''

    # Parent constructor
    super().initialize()

    # ─── Child items (for composite items)

    self.subitem = itemDict(self.canva)