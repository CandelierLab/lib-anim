Windows
=======

Animations are displayed in dedicated windows created with
:py:class:`anim.window`. A single instantiation is enough to get a fully
functional animation window: the Qt event loop, keyboard shortcuts, layout
management, and movie recording are handled internally.

Creating a window
-----------------

Start with the smallest possible setup:

.. code-block:: python

   import anim

   W = anim.window('My animation')
   W.add(anim.plane.canva(W))
   W.show()

Then tune :py:class:`anim.window` with constructor options:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Default
     - Description
   * - ``title``
     - ``'Animation'``
     - Title displayed in the window title bar.
   * - ``style``
     - ``'dark'``
     - Visual theme. Available values are ``'dark'``, ``'light'``, and
       ``'white'``.
   * - ``height``
     - ``0.75``
     - Window height as a fraction of the screen height. For example,
       ``0.75`` means 75% of the screen height.
   * - ``width``
     - ``None``
     - Window width as a fraction of the screen width. If ``None``, the
       width is computed from ``height`` and ``aspect_ratio``.
   * - ``aspect_ratio``
     - ``1``
     - Width/height ratio of the animation area (excluding the information
       dock).
   * - ``information``
     - ``None``
     - Custom :py:class:`anim.information` subclass for the information
       dock.

Styling
-------

Styling is controlled by the ``style`` argument of
:py:class:`anim.window`.

.. code-block:: python

   # Default dark theme
   W = anim.window('Night view', style='dark')

   # Bright theme for print-like visuals
   W2 = anim.window('Day view', style='light')

The ``dark`` theme is usually best for high-contrast animated objects,
while ``light`` is useful when your figure uses dark strokes and you want
an interface close to standard report figures.

Adding canvas panels
--------------------

Canvas panels are added with
:py:meth:`anim.window.add <anim.window.add>` and arranged in a
grid. By default, each new panel is appended to the right.

.. code-block:: python

   W.add(MyCanva)               # automatic placement
   W.add(MyCanva, row=1, col=0) # explicit placement

You can pass a class (instantiated automatically) or an existing object.
Extra keyword arguments are forwarded to the canvas constructor (for example
:py:class:`anim.plane.canva` subclasses):

.. code-block:: python

   W.add(clock, city='Europe/Paris')

For instance in the :doc:`multiple canva demo <../demos/demo_multiple_canva>`,
each canvas is added by a call to
:py:meth:`anim.window.add <anim.window.add>`:

.. code-block:: python

   W.add(clock, city='America/New_York')
   W.add(clock, city='Europe/Paris')
   W.add(clock, city='Asia/Singapore')

Timing and playback
-------------------

The animation runs at a fixed frame rate, defaulting to 25 fps. Each frame
increments an integer step counter. Real time is ``step * dt`` where
``dt = 1 / fps``.

The following attributes can be set before
:py:meth:`anim.window.show <anim.window.show>`:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Attribute
     - Default
     - Description
   * - ``fps``
     - ``25``
     - Frames per second.
   * - ``autoplay``
     - ``True``
     - Start playing automatically when the window opens.
   * - ``step_max``
     - ``None``
     - Maximum step. If set, animation pauses at this value.
   * - ``allow_backward``
     - ``False``
     - Allow backward stepping.
   * - ``allow_negative_time``
     - ``False``
     - Allow step values below zero.

.. code-block:: python

   W.fps = 30
   W.autoplay = False
   W.step_max = 200
   W.allow_backward = True

Keyboard shortcuts
------------------

The following shortcuts are available in every window:

+---------------------+-----------------------------------------------------------+
| Key                 | Action                                                    |
+=====================+===========================================================+
| :kbd:`Space`        | Play/pause                                                |
+---------------------+-----------------------------------------------------------+
| :kbd:`Right`        | Step forward by one frame (when paused)                   |
+---------------------+-----------------------------------------------------------+
| :kbd:`Left`         | Step backward by one frame (if ``allow_backward=True``)   |
+---------------------+-----------------------------------------------------------+
| :kbd:`i`            | Show/hide the information panel                           |
+---------------------+-----------------------------------------------------------+
| :kbd:`Esc`          | Close the window                                          |
+---------------------+-----------------------------------------------------------+

Information dock behavior and content updates are documented in
:doc:`the information section <information>`.

Recording a movie
-----------------

Set ``W.movieFile`` before calling
:py:meth:`anim.window.show <anim.window.show>` to record the animation:

.. code-block:: python

   W.movieFile = 'output/my_movie.mp4'
   W.show()

Additional recording options:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Attribute
     - Default
     - Description
   * - ``moviefps``
     - ``25``
     - Output video frame rate.
   * - ``movieWidth``
     - ``1600``
     - Output video width in pixels (must be a multiple of 16).
   * - ``keep_every``
     - ``1``
     - Record one frame every ``n`` animation frames.