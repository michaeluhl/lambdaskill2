from setuptools import setup, find_packages


def readme():
    with open('README.rst', 'rt') as readme_file:
        return readme_file.read()


setup(name='lambdaskill2',
      version='0.0.0',
      description='A simple toolkit for building Alexa skills.',
      long_description=readme(),
      author='Michael Uhl',
      url='https://github.com/michaeluhl/lambdaskill2',
      license='LGPL',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      install_requires=[
          'aniso8601',
          ],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Other Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
          ],
      zip_safe=True)
