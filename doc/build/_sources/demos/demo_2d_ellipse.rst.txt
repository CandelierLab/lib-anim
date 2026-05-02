2D Ellipse Demo
===============

This demo shows a dynamic grid of ellipses whose horizontal and vertical dimensions are continuously swapped over time.
The class ``Canva`` subclasses ``anim.plane.canva`` and updates each ellipse in ``update`` using ``np.cos(t.step/20)``
so alternating cells animate in opposite deformation directions.

.. raw:: html

   <img src="../media/2d_ellipse.gif" alt="2D ellipse demo" style="max-width: 100%; height: auto;" />

Full Code
---------

.. literalinclude:: ../../../demo/2d_ellipse.py
   :language: python
   :linenos:
