from setuptools import setup, find_packages


VERSION = '1.0.10'
DESCRIPTION = 'Beautifully simple animations'
LONG_DESCRIPTION = (
    'Documentation: https://candelierlab.github.io/lib-anim/\n\n'
    'lib-anim is a Python package to create interactive 2D and 3D animations '
    'with a simple, content-oriented API. It wraps Qt and matplotlib details '
    'so users can focus on animation concepts such as shapes, colors, motion, '
    'events, and scene composition.'
)

setup(
    name="lib-anim",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Raphaël Candelier",
    author_email="raphael.candelier@sorbonne-universite.fr",
    license='GNU GPL v3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['numpy', 'matplotlib', 'pyqt6', 'pyqt6-3d', 'imageio[ffmpeg]'],
    keywords='conversion',
    classifiers= [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Visualization",
    ]
)
