The :py:mod:`Animation` toolbox aims at using minimal code to leverage the power of ``Qt`` and produce smooth animations. All the complexity of ``Qt`` programming is hidden, so the end user only manages meaningfull objects and variables directly related to the animation — like rectangles, positions or colors — instead of ``QGraphicsScene`` or ``QInputMethodQueryEvent`` 😱.

If you are discovering the toolbox, you may want to read the Concepts section below, follow the quickstart tutorial and run some demonstrations.

Concepts
--------

**Windows**

Animations are displayed in dedicated windows.

* Windows are created *via* the :py:class:`Window<Animation.Window>` class. Users typically just have to instantiate a :py:class:`Window<Animation.Window>` object to have a functional animation window, where all the complexity of ``Qt`` windows (layout, events, etc.) and of animations (main loop, keyboard shortcuts, recording movies, etc.) are managed under the hood.
* Windows embed one or several animation panels, as well as other useful elements like an information panel. These different elements are automatically synchronized during the animation.

**Animation panels**

Animation panels are the widgets where animations are rendered.

* There are only 2D animation panels for the moment.
* 

**Information panel**

The information panel displays useful information alongside the animation. It is highly customizable.
