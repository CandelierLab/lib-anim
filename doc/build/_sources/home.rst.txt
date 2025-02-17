The ``lib-anim`` toolbox aims at using minimal code to leverage the power of ``Qt`` and produce smooth animations.

No need to be a Qt guru
-----------------------

The user manages meaningfull objects and variables directly related to the animation like rectangles, positions or colors, and not abstract objects like ``QGraphicsScene`` or ``QInputMethodQueryEvent`` 😱. In other words, all the complexity of ``Qt`` programming is hidden, so you can spend your time on what matters for the final result.

Key features
------------

* Animations are rendered in separate :doc:`windows <guide/windows>` with customizable layouts.
* :doc:`2D animations <guide/2D animations>` are supported.
* Multiple cross-linked animations can be displayed in the same window.
* An :doc:`information panel <guide/information>` can display textual information (html), with live updates.
* Animations can be recorded in movies.

Installation
------------

.. code-block:: console

  $ pip install lib-anim