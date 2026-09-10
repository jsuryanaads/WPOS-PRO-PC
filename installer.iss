; WPOS PRO V1.0 Inno Setup
[Setup]
AppName=WPOS PRO
AppVersion=1.0
DefaultDirName={autopf}\WPOS PRO
DefaultGroupName=WPOS PRO
OutputDir=installer
OutputBaseFilename=WPOS_PRO_V1.0_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayName=WPOS PRO V1.0

[Files]
Source: "dist\WPOS PRO\WPOS PRO.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\WPOS PRO"; Filename: "{app}\WPOS PRO.exe"
Name: "{autodesktop}\WPOS PRO"; Filename: "{app}\WPOS PRO.exe"

[Run]
Filename: "{app}\WPOS PRO.exe"; Description: "Jalankan WPOS PRO"; Flags: nowait postinstall skipifsilent
