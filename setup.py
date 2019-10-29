from setuptools import setup, find_packages

from apigee import APP, __version__, description

setup(name=APP,
      version=__version__,
      description=description,
      author='Matthew Delotavo',
      author_email='matthew.t.delotavo@gmail.com',
      url='https://github.com/mdelotavo/apigee-cli',
      download_url='https://github.com/mdelotavo/apigee-cli/archive/v' + __version__ + '.tar.gz',
      keywords=['apigee', 'management', 'api', 'oauth'],
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'apigee=apigee.__main__:main'
          ]
      },
      python_requires='>=3.5',
      install_requires=['pyotp', 'requests'],
      license='Apache license 2.0',
      classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ])
