#! /usr/bin/env python

from setuptools import setup

exec(open("./mapcraft_slice_maker/_version.py").read())

setup(name="mapcraft-slice-maker",
      version=__version__,
      author="Rory McCann",
      author_email="rory@technomancy.org",
      packages=['mapcraft_slice_maker'],
      install_requires = [
          "fiona",
          "openstreetmap-writer"
      ],
      license = 'AGPLv3+',
      description = "Convert geofiles into mapcraft suitable slice files",
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
      ],
      entry_points={
          'console_scripts': [
              'geojson2mapcraft = mapcraft_slice_maker:main',
              'shp2mapcraft = mapcraft_slice_maker:main',
              'bbox2mapcraft = mapcraft_slice_maker:bbox2mapcraft',
          ]
      },
)
