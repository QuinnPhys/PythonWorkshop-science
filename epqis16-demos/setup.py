from setuptools import setup

setup(
    name='epqis16_demos',
    version='0.1',
    py_modules=['epqis16_demos'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        epqis16=epqis16_demos:main
    ''',
)
