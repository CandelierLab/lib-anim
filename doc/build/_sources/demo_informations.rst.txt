Informations Demo
=================

This demo shows how to drive the information panel from animation state updates.
A `Canva` subclass updates an image size over time and writes formatted HTML metrics
(width and height) into `window.information.html` at every frame.

Movie
-----

.. raw:: html

   <video controls autoplay loop muted playsinline style="max-width: 100%; height: auto;">
     <source src="movies/informations.mp4" type="video/mp4">
     Your browser does not support the video tag.
   </video>

Full Code
---------

.. literalinclude:: ../../demo/informations.py
   :language: python
   :linenos:
