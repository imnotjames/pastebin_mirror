from setuptools import setup

setup(
    name='pastebin_mirror',
    version='0.0.1',
    description='Mirror Pastebin to an SQLite DB',
    url='http://github.com/imnotjames/pastebin_mirror',
    author='James Ward',
    author_email='james@notjam.es',
    license='MIT',
    packages=[
        'pastebin_mirror'
    ],
    install_requires=[
      'requests',
    ],
    zip_safe=False
)
