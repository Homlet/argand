[Setup]
AppName=Argand Plotter
AppVersion=1.0
DefaultDirName={pf}\Homletmoo\Argand
DefaultGroupName=Argand Plotter
ChangesAssociations=yes

[Files]
Source: "Win32GUI\*"; DestDir: "{app}"             
Source: "Win32GUI\examples\*"; DestDir: "{app}\examples"
Source: "Win32GUI\imageformats\*"; DestDir: "{app}\imageformats"
Source: "Win32GUI\img\*"; DestDir: "{app}\img"

[Icons]
Name: "{group}\Argand Plotter"; Filename: "{app}\Argand.exe"

[Registry]
Root: HKCR; Subkey: ".arg";
  ValueType: string;
  ValueName: "";
  ValueData: "ArgandPlotterDiagram";
  Flags: uninsdeletevalue
Root: HKCR; Subkey: "ArgandPlotterDiagram";
  ValueType: string;
  ValueName: "";
  ValueData: "Argand Plotter Diagram";
  Flags: uninsdeletekey
Root: HKCR; Subkey: "ArgandPlotterDiagram\DefaultIcon";
  ValueType: string;
  ValueName: "";
  ValueData: "{app}\Argand.exe,0"
Root: HKCR; Subkey: "ArgandPlotterDiagram\shell\open\command";
  ValueType: string;
  ValueName: "";
  ValueData: """{app}\Argand.exe"" ""%1"""
