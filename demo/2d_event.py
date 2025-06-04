'''
2D event demo
'''

import numpy as np
import anim

# ═══ 2D Animation canva ═══════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window, **kwargs):

    super().__init__(window, 
                     boundaries = [[0, 1],[0,1]],
                     display_boundaries = True,    
                     **kwargs)

    # ─── Click

    self.item.group_click = anim.plane.group(
      position = [0.5, 0.7]
    )

    self.item.rect_click = anim.plane.rectangle(
      group = self.item.group_click,
      position = [0, 0],
      dimension = [0.25, 0.1]
    )
    
    self.item.text_click = anim.plane.text(
      group = self.item.group_click,
      position = [0, 0],
      string = 'Click me',
      color = 'black'
    )

    # ─── Drag

    self.item.group_drag = anim.plane.group(
      position = [0.5, 0.3],
      draggable = True
    )

    self.item.rect_drag = anim.plane.rectangle(
      group = self.item.group_drag,
      position = [0, 0],
      dimension = [0.25, 0.1]
    )
    
    self.item.text_drag = anim.plane.text(
      group = self.item.group_drag,
      position = [0, 0],
      string = 'Drag me',
      color = 'black'
    )

    # ─── Result

    self.item.group_result = anim.plane.group(
      position = [0.5, 0.5]
    )

    self.item.rect_result = anim.plane.rectangle(
      group = self.item.group_result,
      position = [0, 0],
      dimension = [0.5, 0.1],
      color = 'white'
    )
    
    self.item.text_result = anim.plane.text(
      group = self.item.group_result,
      position = [0, 0],
      string = '',
      fontsize = 0.04,
      color = 'black'
    )

  # ────────────────────────────────────────────────────────────────────────
  def event(self, item, desc):

    match item:
      
      case self.item.group_click.qitem:

        self.item.text_result.string = str(desc)

      case self.item.group_drag.qitem:

        p = self.item.group_drag.qitem.pos()

        self.item.text_result.string = f'position ({p.x():.02f},{p.y():.02f})'
    
# ═══ Main ═════════════════════════════════════════════════════════════════

W = anim.window('Event animation')

# Add animation
W.add(Canva)

W.autoplay = False
W.show()