2D Path Demo
============

This demo illustrates how to animate a polyline by updating its point list at each frame.
The `Canva` class subclasses `anim.plane.canva`, builds an `anim.plane.path` item, and recomputes
its points with a sinusoidal profile in `update`, which creates a smooth waveform motion.

.. raw:: html

   <img src="../media/2d_path.gif" alt="2D path demo" style="max-width: 100%; height: auto;" />

Full Code
---------

.. literalinclude:: ../../../demo/2d_path.py
   :language: python
   :linenos:
