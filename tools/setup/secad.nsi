!include "MUI2.nsh"

; The name of the installer
Name "SECAD"

; The file to write
;OutFile "secad-setup.exe"

; Request application privileges for Windows Vista
;RequestExecutionLevel admin

; Build Unicode installer
Unicode True

; The default installation directory
InstallDir $PROGRAMFILES64\SECAD

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\SECAD Software\SECAD" "InstallFolder"
  
;  Icon "setup.ico"

;  !define MUI_ICON "setup.ico"
;  !define MUI_UNICON "setup.ico"

SetCompressor /SOLID lzma


;Interface Settings

!define MUI_HEADERIMAGE
!define MUI_ABORTWARNING


;Pages

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_RUN "$INSTDIR\SECAD.exe"
!insertmacro MUI_PAGE_FINISH
  
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH
  
!insertmacro MUI_LANGUAGE "English"


;Installer Sections

Section "Application Files" SecSECAD

  SectionIn RO
  SetOutPath "$INSTDIR"

  File /r /x library.bin "appdir\*.*"

  ;Register file extension
  WriteRegStr HKCR ".lcd" "" "SECAD.Project"
  WriteRegStr HKCR ".lcd\ShellNew" "NullFile" ""
  WriteRegStr HKCR "SECAD.Project" "" "SECAD Project"
  WriteRegStr HKCR "SECAD.Project\DefaultIcon" "" "$INSTDIR\SECAD.exe,0"
  WriteRegStr HKCR "SECAD.Project\shell" "" "open"
  WriteRegStr HKCR "SECAD.Project\shell\open\command" "" '"$INSTDIR\SECAD.exe" "%1"'
  System::Call 'shell32.dll::SHChangeNotify(i, i, i, i) v (0x08000000, 0, 0, 0)'

  IfFileExists "$INSTDIR\vc_redist.x64.exe" VcRedist64Exists PastVcRedist64Check
  VcRedist64Exists:
    ExecWait '"$INSTDIR\vc_redist.x64.exe"  /quiet /norestart'
  PastVcRedist64Check:

  ;Store installation folder
  ;WriteRegStr HKLM "Software\SECAD Software\SECAD" "InstallFolder" $INSTDIR
  
  CreateShortCut "$SMPROGRAMS\SECAD.lnk" "$INSTDIR\SECAD.exe"

  ;Create uninstaller
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SECAD" "DisplayName" "SECAD"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SECAD" "DisplayVersion" $%VERSION%
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SECAD" "Publisher" "SECAD.org"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SECAD" "DisplayIcon" '"$INSTDIR\SECAD.exe"'
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SECAD" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SECAD" "URLUpdateInfo" "https://www.secad.org"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SECAD" "URLInfoAbout" "https://www.secad.org"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SECAD" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SECAD" "NoRepair" 1

  !include "FileFunc.nsh"
  ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
  IntFmt $0 "0x%08X" $0
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SECAD" "EstimatedSize" "$0"

  WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd

Section "Parts Library" SecLibrary

  SetOutPath "$INSTDIR"

  File "appdir\library.bin"

SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_SecSECAD ${LANG_ENGLISH} "Application Files (required)"
  LangString DESC_SecLibrary ${LANG_ENGLISH} "Library of parts that represent those produced by the LEGO company and created by the LDraw community"

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecSECAD} $(DESC_SecSECAD)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecLibrary} $(DESC_SecLibrary)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  Delete "$SMPROGRAMS\SECAD.lnk"
  Delete "$INSTDIR\Uninstall.exe"

  Delete "$INSTDIR\SECAD.exe"
  Delete "$INSTDIR\SECAD.hlp"
  Delete "$INSTDIR\SECAD.cnt"
  Delete "$INSTDIR\readme.txt"
  Delete "$INSTDIR\library.bin"
  Delete "$INSTDIR\povconsole32-sse2.exe"
  Delete "$INSTDIR\vc_redist.x64.exe"

  RMDir "$INSTDIR"

  DeleteRegKey HKCR ".lcd"
  DeleteRegKey HKCR "SECAD.Project"
  System::Call 'shell32.dll::SHChangeNotify(i, i, i, i) v (0x08000000, 0, 0, 0)'

  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SECAD"
  DeleteRegKey HKLM "Software\SECAD Software\SECAD\InstallFolder"
  DeleteRegKey /ifempty HKCU "Software\SECAD Software\SECAD"

SectionEnd
