'''
Generic 3d item
'''

from .canva import canva

# ══════════════════════════════════════════════════════════════════════════
#                               GENERIC 3D ITEM
# ══════════════════════════════════════════════════════════════════════════

class item:
  '''
  3d item
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self):
    '''
    Constructor
    '''

    # ─── Definitions

    # Reference canva
    self.canva:canva = None

    # 3d entity
    self.entity = None
    self.mesh = None

    # Assign name
    self.name = None

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the item

    This method is meant to be overloaded and called.
    At this point:
    - the canva should be defined (automatically managed by itemDict)
    - the qitem should be defined (managed by the children class)
    '''

    pass