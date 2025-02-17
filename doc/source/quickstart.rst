Quickstart
==========

Let's create our first animation, consisting of a red point spinning around.

Creating a window
-----------------

Creating a :doc:`window <guide/windows>` is easy, we'll just use the default parameters:

.. code-block:: python

  import anim

  W = anim.window('Simple animation')
  W.show()

When executed, this should display a small, empty window. You can close it by clicking on the close button or using the ``Esc`` shortcut.

Creating an animation
---------------------

A custom animation is created by defining a children class to the :py:class:`anim.plane.view` class:

.. code-block:: python

  class myAnimation(anim.plane.view):

    def __init__(self, window):

      # Call parent constructor
      super().__init__(window)

The animation can then added to the window with the :py:func:`anim.window.add` method:

.. code-block:: python

  # Create a window
  W = anim.window('Simple animation')

  # Add the animation
  W.add(myAnimation)

  # Display the window and animation running
  W.show()

If you now run the script, an empty animation should appear in the window.

Populate the animation
----------------------

Now, you want to put different elements on the scene. The constructor of the animation view is where you define them:

.. code-block:: python

  class myAnimation(anim.plane.view):

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

An animation is a sequence of steps, so we have to define what we'd like to change from one step to the other. This is where the :py:func:`update <anim.plane.view.update>` method of the :py:class:`anim.plane.view` is brought to action:

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

Putting everythign together, the final code looks like:

.. code-block:: python
  :linenos:

  import numpy as np
  import anim

  # === 2D Animation =========================================================

  class myAnimation(anim.plane.view):

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

  # Create a window
  W = anim.window('Simple animation')

  # Add the animation
  W.add(myAnimation)

  # Display the window and animation running
  W.show()

If you try and execute this script, you should see the animation witht the red dot moving around. 🎉 Congratulations, you have completed the quickstart tutorial !