'''
Dictionnary of items
'''

class itemDict(dict):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, canva):
    
    # ─── Definition   
     
    self._canva = canva

  # ────────────────────────────────────────────────────────────────────────
  def __setattr__(self, name, value):
    '''
    Attribute shortcut notation
    '''

    if not name.startswith('_'):

      # Assign as item
      self[name] = value
        
    else:

      # Assign as attribute
      super().__setattr__(name, value)

  # ────────────────────────────────────────────────────────────────────────
  def __getattr__(self, name):
    '''
    Attribute shortcut notation
    '''

    if not name.startswith('_'):

      # Return item
      return self[name]
        
    else:

      # Return attribute
      return super().__getattr__(name)
    

  # ────────────────────────────────────────────────────────────────────────
  def __setitem__(self, key, item):

    # Add the canva attribute to the item
    item.canva = self._canva

    # Assign item name
    item.name = key

    # Initialize item
    item.initialize()

    # Add the item to the scene
    self._canva.scene.addItem(item)

    # Assign the key/value pair
    dict.__setitem__(self, key, item)