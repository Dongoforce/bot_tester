
from cx_Freeze import setup, Executable

executables = [Executable('gui_connector.py')]

setup(name='gui',
      version='0.0.1',
      description='Gui',
      executables=executables)