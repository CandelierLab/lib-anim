Installation
============

The library is distributed as a standard Python package.

Prerequisites
-------------

- Python 3
- A working virtual environment tool (`venv` is recommended)

Create and activate a virtual environment
-----------------------------------------

Using an isolated environment is strongly recommended.

.. code-block:: console

  $ python -m venv .venv

Activate it:

.. code-block:: console

  # Linux / macOS
  $ source .venv/bin/activate

  # Windows (PowerShell)
  > .venv\Scripts\Activate.ps1

Install from PyPI
-----------------

.. code-block:: console

  (.venv) $ pip install --upgrade pip
  (.venv) $ pip install lib-anim

Install from source (development mode)
--------------------------------------

If you are working on the package itself, install it in editable mode from the
repository root.

.. code-block:: console

  (.venv) $ pip install --upgrade pip
  (.venv) $ pip install -e .

Quick verification
------------------

Check that import works:

.. code-block:: console

  (.venv) $ python -c "import anim; print(anim.__file__)"

Optional: run one demo to confirm the GUI stack works:

.. code-block:: console

  (.venv) $ python demo/2d_line.py

Dependencies
------------

`lib-anim` depends on:

- `numpy`
- `matplotlib`
- `pyqt6`
- `pyqt6-3d`
- `imageio[ffmpeg]`

These are installed automatically by `pip`.

Troubleshooting
---------------

- If `python -m venv .venv` fails on Debian/Ubuntu, ensure the `python3-venv`
  package is installed for your Python version.
- If a demo cannot import `anim`, ensure your virtual environment is activated
  and that installation was done in the same environment.