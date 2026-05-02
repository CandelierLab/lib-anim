2D canvas
=========

A :py:class:`anim.plane.canva` is the 2D drawing surface embedded in a
:py:class:`anim.window`. It defines scene limits, coordinate scaling,
bounding-box display, and optional grid display.

Minimal setup
-------------

.. code-block:: python

   import anim

   W = anim.window('2D canvas')
   C = anim.plane.canva(W)
   W.add(C)
   W.show()

Constructor options
-------------------

The :py:class:`anim.plane.canva` constructor exposes the following options:

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parameter
     - Default
     - Description
   * - ``window``
     - required
     - Parent :py:class:`anim.window` instance.
   * - ``boundaries``
     - ``None``
     - Scene limits as ``[[x0, x1], [y0, y1]]``. If omitted, default is
       ``[[0, 1], [0, 1]]``.
   * - ``display_boundaries``
     - ``True``
     - Show or hide the boundary rectangle.
   * - ``boundaries_color``
     - theme-dependent
     - Boundary rectangle color (auto-selected from window style if omitted).
   * - ``boundaries_thickness``
     - ``None``
     - Boundary thickness setting stored in the bounding-box model.
   * - ``padding``
     - ``0``
     - Extra margin used by the 2D view fit.
   * - ``background_color``
     - ``None``
     - View background color.
   * - ``pixelperunit``
     - ``1``
     - Scale factor: pixels per scene unit.
   * - ``coordinates``
     - ``'xy'``
     - Coordinate convention. With ``'xy'``, y-axis is upward.
   * - ``grid``
     - ``None``
     - Grid control: ``True`` for default grid, or provide a
       :py:class:`anim.plane.grid` instance.

Defining dimensions and extents
-------------------------------

Canvas dimensions are controlled by :py:attr:`anim.plane.canva.boundaries`.
Use ``[[x0, x1], [y0, y1]]`` to set visible extents.

.. code-block:: python

   C = anim.plane.canva(W, boundaries=[[-2, 2], [-1, 1]])

   # Runtime update of visible extents
   C.boundaries = [[-3, 3], [-2, 2]]

The boundary box model is :py:class:`anim.core.boundingBox`, which stores
``x0``, ``x1``, ``y0``, ``y1``, width, height, aspect ratio, and style
metadata.

Bounding-box style
------------------

You can control visibility and color of the boundary rectangle:

.. code-block:: python

   C.display_boundaries = True
   C.boundaries.color = 'white'
   C.setBoundaryStyle()

Notes:

* :py:attr:`anim.plane.canva.display_boundaries` toggles visibility.
* Color comes from ``C.boundaries.color``.
* :py:meth:`anim.plane.canva.setBoundaryStyle` reapplies current style
  settings to the Qt item.

Coordinate system
-----------------

The ``coordinates`` parameter controls the orientation of the y-axis.

**``coordinates='xy'`` (default)** — mathematical convention
  The y-axis points **upward**, as in standard Cartesian coordinates.
  A point at ``y=1`` is displayed above a point at ``y=0``.
  This mode is the default and is suited for scientific or mathematical
  content where the natural y-direction is upward.

  .. code-block:: python

     C = anim.plane.canva(W, boundaries=[[-2, 2], [-2, 2]], coordinates='xy')
     # A circle placed at (0, 1) appears near the top of the canvas.

**``coordinates='screen'`` (or any other value)** — screen convention
  The y-axis points **downward**, following Qt's native coordinate system.
  A point at ``y=1`` is displayed *below* a point at ``y=0``.
  This mode is suitable for UI-like layouts or image processing where
  the origin is at the top-left corner.

  .. code-block:: python

     C = anim.plane.canva(W, boundaries=[[0, 800], [0, 600]], coordinates='screen')
     # A circle placed at (0, 0) appears at the top-left corner.

.. note::
   The two modes only differ in the direction of the y-axis. The x-axis
   always points to the right. Switching from one mode to the other
   mirrors all y-coordinates, so the same positions will produce
   vertically mirrored results.

Scale: ``pixelperunit``
-----------------------

The ``pixelperunit`` parameter sets how many **screen pixels** correspond
to one **scene unit**. It acts as a global zoom factor for the scene.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Value
     - Effect
   * - ``pixelperunit=1`` (default)
     - 1 pixel = 1 scene unit. Suitable when boundaries span a small integer range, e.g. ``[0, 1]``.
   * - ``pixelperunit=100``
     - 100 pixels = 1 scene unit. Larger pixel budget means smoother rendering of fine details (thin lines, small shapes).
   * - ``pixelperunit=400``
     - High-density canvas. Use when the boundary range is small (e.g. ``[0, 1]``) but the output window is large.

.. code-block:: python

   # Unit square, high pixel density
   C = anim.plane.canva(W, boundaries=[[0, 1], [0, 1]], pixelperunit=400)

   # Large coordinate range, 1:1 mapping
   C = anim.plane.canva(W, boundaries=[[0, 800], [0, 600]], pixelperunit=1)

.. tip::
   If shapes appear jagged or text looks blurry, try increasing
   ``pixelperunit``. As a rule of thumb, set ``pixelperunit`` so that
   ``(x1 - x0) * pixelperunit`` roughly matches the width of the window
   in pixels.

Grid options
------------

To add a default grid quickly:

.. code-block:: python

   C = anim.plane.canva(W, grid=True)

To fully control grid behavior, pass a configured :py:class:`anim.plane.grid`
instance.

.. code-block:: python

   G = anim.plane.grid(spacing=0.5, shift=[0.1, 0.0], color='grey', zvalue=-1)
   C = anim.plane.canva(W, boundaries=[[-2, 2], [-2, 2]], grid=G)

At runtime, you can animate grid shift through :py:attr:`anim.plane.grid.shift`.
