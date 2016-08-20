from setuptools import setup


setup(
    name='http-server',
    description='A http server in python.',
    version=0.1,
    author='Mike Harrison, Jeffery Russell',
    author_email='sample@sample.com',
    license='MIT',
    py_modules=['client', 'server'],
    package_dir={'': 'src'},
    instal_requires=[],
    extra_requires={'test': ['pytest', 'tox']},
)
