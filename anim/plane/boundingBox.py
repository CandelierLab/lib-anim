class boundingBox:

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, display, boundaries, color, thickness):
    '''
    Boundaries inputs are formated as [[x0,x1],[y0,y1]]
    '''

    self.display = display

    # ─── Reference points (bottom-left and top-right corners)

    # Default values
    if boundaries is None:
      self.x0 = 0
      self.x1 = 1
      self.y0 = 0
      self.y1 = 1
    else:
      self.x0 = boundaries[0][0]
      self.x1 = boundaries[0][1]
      self.y0 = boundaries[1][0]
      self.y1 = boundaries[1][1]
      
    # ─── Extension

    self.width = self.x1 - self.x0
    self.height = self.y1 - self.y0

    # ─── Aspect ratio

    self.aspect_ratio = self.width/self.height

    # ─── Color

    self.color = color if color is not None else 'white'

    # ─── Thickness

    self.thickness = thickness if thickness is not None else 1