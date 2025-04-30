import re
import anim

class information(anim.plane.panel):
    
  # ========================================================================
  def __init__(self, W, disp_time=True):
    
    # Parent contructor
    super().__init__(W, 
                     boundaries=[[0, 0.2], [0, 1]], 
                     boundaries_color = None)

    # --- Optional display

    # Time string
    self.disp_time = disp_time

    if self.disp_time:
      self.add(anim.plane.text, 'Time',
        stack = True,
        string = self.time_str(anim.time(0,0)),
        fontsize = 12,
      )

  # ========================================================================
  def time_str(self, t):
    '''
    Format time string for display
    '''

    s = '<p>step {:06d}</p><font size=2> {:06.02f} sec</font>'.format(t.step, t.time)

    # Grey zeros
    s = re.sub(r'( )([0]+)', r'\1<span style="color:grey;">\2</span>', s)

    return s
  
  # ========================================================================
  def update(self, t):

    if self.disp_time:
      self.item['Time'].string = self.time_str(t) 

    # Repaint & confirm
    super().update(t)