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
    '''

    print('ok')

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