# AGENTS.md file

## General
- This package provides an API for creating Qt and matplotlib animations in a GUI. It is designed for user who don't know how Qt works, hence the user should never have to import pyqt modules and all the Qt details should be embedded in the package classes. 
- More generally, this API should let as much as possible the user focus on concepts related to the animation itself (like shapes, colors, motion or user events) and hide all the implementation details.

## Documentation
- The documentation is generated with sphinx. Use `sphinx-build doc/source/ doc/build` to build the documentation.
- Before every documentation building, check that the version number (release) in doc/source/conf.py is incremented with respect to the version number (VERSION) in setup.py.
- Build the documentation every time you make modifications to the source folder.

### Documentation demos
- When I specifically ask for a video or gif rebuild, a short mp4 movie should be generated or regenerated and stored in /doc/source/media/movies. The video should be generated with the dark theme and should be compressed after creation. Then, an animated gif of size 500x500 should be created and stored in doc/build/media. The gifs ares used in the html pages of the documentation.
- The structure of a demo rst file contains the following paragraphs, in this order: 
  - Some textual explanation of what the demo is about, what concept it illustrates and how it works. Important lines can be highlighted in code snippets.
  - [Paragraph without title] The animated gif of the demo, with automatically playing.
  - The full code of the demo
 
