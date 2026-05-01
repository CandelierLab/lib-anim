2D Path Demo
============

This demo illustrates how to animate a polyline by updating its point list at each frame.
The `Canva` class subclasses `anim.plane.canva`, builds an `anim.plane.path` item, and recomputes
its points with a sinusoidal profile in `update`, which creates a smooth waveform motion.

Movie
-----

.. raw:: html

   <video controls autoplay loop muted playsinline style="max-width: 100%; height: auto;">
     <source src="movies/2d_path.mp4" type="video/mp4">
     Your browser does not support the video tag.
   </video>

Full Code
---------

.. literalinclude:: ../../demo/2d_path.py
   :language: python
   :linenos:
