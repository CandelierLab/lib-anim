2D shapes
=========

This section presents the main shape classes available in
:py:mod:`anim.plane`, and how to control their geometry and style.

Available shapes
----------------

The following classes cover the standard 2D shapes.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - API class
     - Demo
   * - :py:class:`anim.plane.line`
     - :doc:`Line <../demos/demo_2d_line>`
   * - :py:class:`anim.plane.circle`
     - :doc:`Circle <../demos/demo_2d_circle>`
   * - :py:class:`anim.plane.ellipse`
     - :doc:`Ellipse <../demos/demo_2d_ellipse>`
   * - :py:class:`anim.plane.rectangle`
     - :doc:`Rectangle <../demos/demo_2d_rectangle>`
   * - :py:class:`anim.plane.polygon`
     - :doc:`Polygon <../demos/demo_2d_polygon>`
   * - :py:class:`anim.plane.path`
     - :doc:`Path <../demos/demo_2d_path>`
   * - :py:class:`anim.plane.arrow` (composite shape)
     - :doc:`Arrow <../demos/demo_2d_arrow>`

Anchor point (reference point)
------------------------------

Each shape inherits from :py:class:`anim.plane.item` and is positioned using a
reference point (anchor point). This anchor is the point controlled by
:py:attr:`anim.plane.item.position` (or by
:py:attr:`anim.plane.item.x` and :py:attr:`anim.plane.item.y`).

The exact geometric meaning of the anchor depends on the shape:

* :py:class:`anim.plane.circle`: the anchor is the center.
* :py:class:`anim.plane.ellipse`: the anchor is the center.
* :py:class:`anim.plane.line`: the anchor is one endpoint by default, or the
  center if ``center=True``.
* :py:class:`anim.plane.rectangle`: by default the anchor is the center;
  with ``center=[False, False]`` it becomes the bottom-left corner.
* :py:class:`anim.plane.polygon` and :py:class:`anim.plane.path`: points are
  defined relative to the anchor.
* :py:class:`anim.plane.arrow`: the anchor follows the first point of the
  arrow trajectory.

.. code-block:: python

   C.item.rect = anim.plane.rectangle(dimension=[1.2, 0.6], center=[False, False])
   C.item.rect.position = [0.0, 0.0]   # bottom-left corner at origin

Rotation and center of rotation
-------------------------------

Rotations are controlled by :py:attr:`anim.plane.item.orientation` (in
radians), or by calling :py:meth:`anim.plane.item.rotate` for relative updates.

The pivot point is controlled by :py:attr:`anim.plane.item.center_of_rotation`:

* for most shapes, default is ``[0, 0]`` in local item coordinates
* for :py:class:`anim.plane.circle`, the natural center rotation is obtained
  with ``center_of_rotation=[0, 0]``
* for polygons/paths, ``[0, 0]`` means rotating around the anchor point

.. code-block:: python

   import numpy as np

   C.item.rect = anim.plane.rectangle(dimension=[1.4, 0.5], position=[0.5, -0.2])

   # Absolute orientation (30 degrees)
   C.item.rect.orientation = np.pi / 6

   # Relative rotation (+15 degrees)
   C.item.rect.rotate(np.pi / 12)

   # Change pivot to the rectangle corner in local coordinates
   C.item.rect.center_of_rotation = [0.7, 0.25]
   C.item.rect.orientation = np.pi / 3

Geometry control by shape
-------------------------

Each shape exposes specific geometry attributes:

* :py:class:`anim.plane.line`:
  ``Lx``, ``Ly`` or ``dimension=[Lx, Ly]`` define the segment vector.
* :py:class:`anim.plane.circle`:
  ``radius`` defines size.
* :py:class:`anim.plane.ellipse`:
  ``Lx`` and ``Ly`` (or ``dimension``) define width and height.
* :py:class:`anim.plane.rectangle`:
  ``Lx`` and ``Ly`` (or ``dimension``), plus ``center`` for anchor behavior.
* :py:class:`anim.plane.polygon`:
  ``points`` defines vertices relative to the anchor.
* :py:class:`anim.plane.path`:
  ``points`` defines a polyline relative to the anchor.
* :py:class:`anim.plane.arrow`:
  ``points`` defines the trajectory; dedicated options control head and text.

Style: fill and stroke
----------------------

Shape style is controlled by four attributes settable directly on any shape
instance, either at construction time or at runtime.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Attribute
     - Description
   * - ``color``
     - Fill color (string, hex, or ``[r, g, b]`` in [0, 1]). Set to ``None`` for no fill (transparent).
   * - ``stroke``
     - Contour color. Set to ``None`` (default) for no contour.
   * - ``thickness``
     - Contour thickness in scene units (default ``0``).
   * - ``linestyle``
     - Contour pattern: ``'-'`` solid, ``'--'`` dashed, ``':'`` dotted, ``'-.'`` dash-dot.

.. code-block:: python

   C.item.ell = anim.plane.ellipse(dimension=[1.2, 0.5], position=[0.0, 0.0])

   # Fill only
   C.item.ell.color = '#4aa3ff'

   # Fill + contour
   C.item.ell.color = '#4aa3ff'
   C.item.ell.stroke = 'white'
   C.item.ell.thickness = 0.01

   # Contour only (no fill)
   C.item.ell.color = None
   C.item.ell.stroke = 'white'
   C.item.ell.thickness = 0.01
   C.item.ell.linestyle = '--'

For :py:class:`anim.plane.line` and :py:class:`anim.plane.path`, there is no
fill — only ``stroke``, ``thickness``, and ``linestyle`` apply.
