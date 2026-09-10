; WPOS PRO V1.0 Inno Setup
#define MyAppName "WPOS PRO"
#define MyAppVersion "1.0"
#define MyAppPublisher "WPOS PRO"
#define MyAppExeName "WPOS PRO.exe"

[Setup]
AppId={{B7D0E6A8-7B7A-4D74-9A4D-9C6C5E9E1A10}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
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
Source: "dist\WPOS PRO\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\WPOS PRO"; Filename: "{app}\WPOS PRO.exe"
Name: "{autodesktop}\WPOS PRO"; Filename: "{app}\WPOS PRO.exe"

[Run]
Filename: "{app}\WPOS PRO.exe"; Description: "Jalankan WPOS PRO"; Flags: nowait postinstall skipifsilent
