# AGENTS.md file
 
## Documentation
- The documentation is generated with sphinx. Use `sphinx-build doc/source/ doc/build` to build the documentation.
- Before every documentation building, check that the version number (release) in doc/source/conf.py is incremented with respect to the version number (VERSION) in setup.py.
- Build the documentation every time you make modifications to the source folder.

### Documentation demos
- When I specifically ask for a demo rebuild, a short mp4 movie should be created and stored in /doc/source/media/movies. The video should be generated with the dark theme and should be compressed after creation.
- The structure of a demo rst file contains the following paragraphs, in this order: 
  - Some textual explanation of what the demo is about, what concept it illustrates and how it works. Important lines can be highlighted in code snippets.
  - The movie of the demo, with automatically playing.
  - The full code of the demo
 
