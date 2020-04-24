''' cx_freeze setup file
matthew oppenheim 2017 '''

from cx_Freeze import setup, Executable

executables = [
    Executable('blink_leo.py')
]

setup(name='blink_leo',
      version='1.0',
      description='hand gesture indicator',
      executables=executables
      )
