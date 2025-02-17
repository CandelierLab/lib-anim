Windows
=======

Animations are displayed in dedicated windows.

* Windows are created *via* the :py:class:`Window<Animation.Window>` class. Users typically just have to instantiate a :py:class:`Window<Animation.Window>` object to have a functional animation window, where all the complexity of ``Qt`` windows (layout, events, etc.) and of animations (main loop, keyboard shortcuts, recording movies, etc.) are managed under the hood.
* Windows embed one or several animation panels, as well as other useful elements like an information panel. These different elements are automatically synchronized during the animation.


* Size
* Layout
* Style