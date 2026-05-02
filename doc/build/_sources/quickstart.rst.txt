Quickstart
==========

In this tutorial, you will build a first animation: a red point rotating around a center.

Creating a window
-----------------

Creating a :doc:`window <guide/windows>` is straightforward. We will start with default parameters:

.. code-block:: python

  import anim

  W = anim.window('Simple animation')
  W.show()

When you run this script, a small empty window should appear.
You can close it either with the close button or with the ``Esc`` shortcut.

Creating an animation
---------------------

To create a custom animation, define a child class of :py:class:`anim.plane.canva`:

.. code-block:: python

  class myAnimation(anim.plane.canva):

    def __init__(self, window):

      # Call parent constructor
      super().__init__(window)

You can then add this animation to the window with :py:func:`anim.window.add`:

.. code-block:: python

  # Create a window
  W = anim.window('Simple animation')

  # Add the animation
  W.add(myAnimation)

  # Display the window and start the animation
  W.show()

If you run this script now, you should see an empty animation area in the window.

Populate the animation
----------------------

Next, add visual elements to the scene.
The constructor of your animation class is the right place to define them:

.. code-block:: python

  class myAnimation(anim.plane.canva):

    def __init__(self, window):

      super().__init__(window, boundaries=[[0,1],[0,1]])

      self.padding = 0.01

      self.x0 = 0.5
      self.y0 = 0.5
      self.R = 0.25
      self.r = 0.01

      self.add(anim.plane.ellipse, 'E0',
        position = [self.x0, self.y0],
        major = 0.005,
        minor = 0.005,
        colors = ('white', None),
      )

      self.add(anim.plane.circle, 'C0',
        position = [self.x0, self.y0],
        radius = self.R,
        colors = (None, 'grey'),
        thickness = 2,
        linestyle = '--'
      )

      self.add(anim.plane.circle, 'C',
        position = [self.x0 + self.R, self.y0],
        radius = self.r,
        colors = ('red', None),
      )

Define updates to create motion
-------------------------------

An animation is a sequence of time steps, so you need to define what changes from one step to the next.
This is done in the :py:func:`update <anim.plane.canva.update>` method of :py:class:`anim.plane.canva`:

.. code-block:: python

  import numpy as np

  def update(self, t):

      # Update timer display
      super().update(t)

      # Update position
      x = self.x0 + self.R*np.cos(t.time)
      y = self.y0 + self.R*np.sin(t.time)
      self.item['C'].position = [x, y]

This sets the position of the ``C`` item to time-dependent coordinates defining a circular trajectory.

Final code
----------

Putting everything together, the final script is:

.. code-block:: python
  :linenos:

  import numpy as np
  import anim

  # === 2D Animation =========================================================

  class myAnimation(anim.plane.canva):

    def __init__(self, window):

      super().__init__(window, boundaries=[[0,1],[0,1]])

      self.padding = 0.01

      self.x0 = 0.5
      self.y0 = 0.5
      self.R = 0.25
      self.r = 0.01

      self.add(anim.plane.ellipse, 'E0',
        position = [self.x0, self.y0],
        major = 0.005,
        minor = 0.005,
        colors = ('white', None),
      )

      self.add(anim.plane.circle, 'C0',
        position = [self.x0, self.y0],
        radius = self.R,
        colors = (None, 'grey'),
        thickness = 2,
        linestyle = '--'
      )

      self.add(anim.plane.circle, 'C',
        position = [self.x0 + self.R, self.y0],
        radius = self.r,
        colors = ('red', None),
      )

    def update(self, t):

      # Update timer display
      super().update(t)

      # Update position
      x = self.x0 + self.R*np.cos(t.time)
      y = self.y0 + self.R*np.sin(t.time)
      self.item['C'].position = [x, y]

  # === Main =================================================================

  # Create a window
  W = anim.window('Simple animation')

  # Add the animation
  W.add(myAnimation)

  # Display the window and start the animation
  W.show()

When you run this script, you should see the red point moving along a circular path.
Congratulations 🎉, you have completed the quickstart tutorial.