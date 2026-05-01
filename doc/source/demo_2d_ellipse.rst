2D Ellipse Demo
===============

This demo shows a dynamic grid of ellipses whose horizontal and vertical dimensions are continuously swapped over time.
The class ``Canva`` subclasses ``anim.plane.canva`` and updates each ellipse in ``update`` using ``np.cos(t.step/20)``
so alternating cells animate in opposite deformation directions.

Movie
-----

.. raw:: html

   <video controls autoplay loop muted playsinline style="max-width: 100%; height: auto;">
       <source src="movies/2d_ellipse.mp4" type="video/mp4">
     Your browser does not support the video tag.
   </video>

Full Code
---------

.. literalinclude:: ../../demo/2d_ellipse.py
   :language: python
   :linenos:
