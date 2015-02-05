[Setup]
AppName=Argand Plotter
AppVersion=1.0
DefaultDirName={pf}\Homletmoo\Argand
DefaultGroupName=Argand Plotter

[Files]
Source: "Win32GUI\*"; DestDir: "{app}"             
Source: "Win32GUI\examples\*"; DestDir: "{app}\examples"
Source: "Win32GUI\imageformats\*"; DestDir: "{app}\imageformats"
Source: "Win32GUI\img\*"; DestDir: "{app}\img"

[Icons]
Name: "{group}\Argand Plotter"; Filename: "{app}\Argand.exe"
