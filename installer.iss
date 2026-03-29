; AI News Radar — Inno Setup Installer Script
; 사용법: Inno Setup 6 설치 후 이 파일을 열어 Compile (Ctrl+F9)
; 다운로드: https://jrsoftware.org/isdl.php

#define MyAppName "AI News Radar"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "SoDam AI Studio"
#define MyAppURL "https://github.com/sodam-ai/ai-news-radar"
#define MyAppExeName "AI_News_Radar.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; 출력 디렉토리
OutputDir=installer_output
OutputBaseFilename=AI_News_Radar_Setup_{#MyAppVersion}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"
Name: "chinese"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startupicon"; Description: "Windows 시작 시 자동 실행"; GroupDescription: "자동 실행:"

[Files]
; PyInstaller 빌드 결과물 전체
Source: "dist\AI_News_Radar\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; .env.example 복사
Source: ".env.example"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
; 자동 시작
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "{#MyAppName}"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: startupicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  EnvFile: string;
begin
  if CurStep = ssPostInstall then
  begin
    { .env 파일이 없으면 .env.example을 .env로 복사 }
    EnvFile := ExpandConstant('{app}\.env');
    if not FileExists(EnvFile) then
    begin
      FileCopy(ExpandConstant('{app}\.env.example'), EnvFile, False);
    end;
  end;
end;
