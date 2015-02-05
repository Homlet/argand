import sys
from cx_Freeze import setup, Executable

if sys.platform == 'win32':
    base = 'Win32GUI'
else:
    raise Exception('Unsupported platform.')

buildOptions = dict(
    build_exe = '../build/' + base,
    include_files = 'img,examples',
    path = [sys.path[0] + '/../src'] + sys.path[1:])

executables = [
    Executable(
        'main.pyw',
        base = base,
        targetName = 'Argand.exe',
        icon = 'img/half_disk.ico')
]

setup(
    name='Argand Plotter',
    version = 'v1.0',
    description = 'A graphing package for plotting Argand diagrams.',
    options = dict(build_exe = buildOptions),
    executables = executables)
