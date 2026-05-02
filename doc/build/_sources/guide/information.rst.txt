Information panel
=================

Each window includes an :py:class:`anim.information` dock that can display
live HTML text and an optional helper canvas. This panel is useful for
showing values, metrics, and contextual messages during animation.

Basic usage
-----------

The dock exists by default in every :py:class:`anim.window` instance, but
it is hidden at startup.

.. code-block:: python

	import anim

	W = anim.window('Animation with information panel')
	W.information.display(True)

Press :kbd:`i` during animation to toggle visibility.

Default temporal information
----------------------------

When the information panel is visible, temporal metadata is inserted by
default at the top of the panel by :py:meth:`anim.information.setTime`:

* the current iteration index (``step``)
* the animation time in seconds (``time``)

You can control this display with two flags:

.. code-block:: python

	W.information.show_steps = True   # show/hide iteration index
	W.information.show_time = True    # show/hide animation time

.. warning::

	The displayed ``time`` value is the animation time computed from
	``step / fps``. It matches physical time only when the animation effectively
	runs at its target fps.

	In practice, this value is reliable in exported movies when animation fps and
	movie fps are consistent. During interactive playback, if update steps are
	heavy and the window cannot keep up with the target fps, displayed animation
	time can diverge from wall-clock time.

Updating displayed content
--------------------------

The text area renders HTML. Update it by assigning to
``W.information.html`` (typically inside your canvas ``update`` method):

.. code-block:: python

	def update(self, t):
		 self.window.information.html = f'<p>Step: {t.step}</p>'
		 super().update(t)

In the :doc:`informations demo <../demos/demo_informations>`, the panel is
updated in real time with the animated image width and height.

Layout and sizing
-----------------

The dock width is controlled by ``W.information.width``. This value is a
fraction of the window height (default: ``0.25``).

.. code-block:: python

	W.information.width = 0.30

You can also provide your own information panel class when creating the
window by passing the ``information`` constructor argument of
:py:class:`anim.window`.

