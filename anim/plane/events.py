'''
Events
'''

from PyQt6.QtWidgets import QGraphicsItem

class event:

  # ────────────────────────────────────────────────────────────────────────
  def mousePressEvent(self, event):
    '''
    Simple click event

    For internal use only.

    args:
      event (QGraphicsSceneMouseEvent): The click event.
    '''

    self.item.canva.event(self, event.button())

  # ────────────────────────────────────────────────────────────────────────
  def mouseDoubleClickEvent(self, event):
    '''
    Double click event

    For internal use only.

    args:
      event (QGraphicsSceneMouseEvent): The double click event.
    '''

    self.item.canva.event(self, event.button().__str__() + '.double')

  # ────────────────────────────────────────────────────────────────────────
  def itemChange(self, change, value):
    '''
    Item change notification

    This method is triggered upon item change. The item's transformation
    matrix has changed either because setTransform is called, or one of the
    transformation properties is changed. This notification is sent if the 
    ``ItemSendsGeometryChanges`` flag is enabled (e.g. when an item is 
    :py:attr:`item.movable`), and after the item's local transformation 
    matrix has changed.

    args:

      change (QGraphicsItem constant): 
    '''

    # ─── Define type

    desc = None

    match change:
      case QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
        desc = 'motion'

    # ─── Report to canva

    if self.item.canva is not None and desc is not None:
      self.item.canva.event(self, desc)

    # ─── Propagate change
    
    return QGraphicsItem.itemChange(self, change, value)