import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(include_files = "img,examples")

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.pyw', base=base, targetName = 'Argand.exe')
]

setup(name='Argand Plotter',
      version = 'v1.0',
      description = 'A graphing package for Argand diagrams.',
      options = dict(build_exe = buildOptions),
      executables = executables)
