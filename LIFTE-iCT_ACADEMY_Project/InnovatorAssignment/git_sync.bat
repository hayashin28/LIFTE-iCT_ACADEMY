@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM (^_^) base paths
set "USB_DRIVE=%~d0"
if not defined PORTABLE_ROOT set "PORTABLE_ROOT=%USB_DRIVE%\PortableApps"
set "ENABLE_DRIVE_SCAN=0"

REM (^_^) PlantUML / MkDocs / SSH key candidates
set "PUML_INPUT_DIR=docs"
set "PUML_EXT=*.puml"
set "PUML_OUT_REL=..\assets"
set "PLANTUML_JAR_CAND[0]=%~dp0tools\plantuml.jar"
set "PLANTUML_JAR_CAND[1]=%PORTABLE_ROOT%\tools\plantuml.jar"
set "PLANTUML_JAR_CAND[2]=%~dp0..\tools\plantuml.jar"
set "MKDOCS_CAND[0]=%PORTABLE_ROOT%\Python\Scripts\mkdocs.exe"
set "MKDOCS_CAND[1]=%~dp0PortableApps\Python\Scripts\mkdocs.exe"
set "SSH_KEY_CAND[0]=%PORTABLE_ROOT%\.ssh\id_ed25519"
set "SSH_KEY_CAND[1]=%~dp0.ssh\id_ed25519"
set "COMMIT_MSG=chore: rebuild diagrams & docs [skip ci]"

REM (^_^) find Git (auto; no 'goto' inside ())
set "BASE=%~dp0"
set "GIT_HOME="
set "CAND[0]=%PORTABLE_ROOT%\Git"
set "CAND[1]=%BASE%Git"
set "CAND[2]=%BASE%..\Git"
set "CAND[3]=%BASE%..\..\Git"
set "CAND[4]=%BASE%PortableApps\Git"
set "CAND[5]=%USB_DRIVE%\Git"
set "CAND[6]=%ProgramFiles%\Git"
set "CAND[7]=%ProgramFiles(x86)%\Git"

for /L %%I in (0,1,7) do (
  for %%P in ("!CAND[%%I]!") do (
    if not defined GIT_HOME if exist "%%~fP\cmd\git.exe" set "GIT_HOME=%%~fP"
  )
)
if not defined GIT_HOME (
  for /f "delims=" %%G in ('where git.exe 2^>nul') do (
    for %%H in ("%%~dpG\..") do if not defined GIT_HOME if exist "%%~fH\cmd\git.exe" set "GIT_HOME=%%~fH"
  )
)
if not defined GIT_HOME if /I "%ENABLE_DRIVE_SCAN%"=="1" (
  for /f "delims=" %%G in ('where /r "%USB_DRIVE%\" git.exe ^| findstr /i "\\Git\\cmd\\git.exe" 2^>nul') do (
    for %%H in ("%%~dpG\..") do if not defined GIT_HOME if exist "%%~fH\cmd\git.exe" set "GIT_HOME=%%~fH"
  )
)
if not defined GIT_HOME (
  echo [ERROR] Git not found (T_T)
  exit /b 1
)

set "PATH=%GIT_HOME%\cmd;%GIT_HOME%\mingw64\bin;%SystemRoot%\system32;%SystemRoot%"
echo [OK] Git home: %GIT_HOME%
for /f "delims=" %%V in ('git --version 2^>nul') do echo [Git] %%V

REM (^_^) quiet auth (disable broken manager -> use store; SSH if found)
git config --local credential.helper "" 1>nul 2>nul
git config --local --add credential.helper "store --file=%PORTABLE_ROOT:\=/%/.git-credentials" 1>nul 2>nul

REM find SSH key (no goto in ())
set "SSH_KEY="
for /L %%I in (0,1,1) do (
  for %%K in ("!SSH_KEY_CAND[%%I]!") do (
    if not defined SSH_KEY if exist "%%~fK" set "SSH_KEY=%%~fK"
  )
)
if defined SSH_KEY (
  set "GIT_SSH_COMMAND=ssh -i %SSH_KEY% -o IdentitiesOnly=yes"
  echo [OK] SSH key: %SSH_KEY% (^_^)
)

REM (^_^) find Java and plantuml.jar (no goto in ())
set "JAVA_EXE="
for /L %%I in (0,1,2) do (
  for %%J in ("!%PORTABLE_ROOT%!\dummy") do rem just to keep structure
)
for /L %%I in (0,1,2) do (
  for %%J in ("!JAVA_CAND[%%I]!") do (
    if defined JAVA_CAND[%%I] if not defined JAVA_EXE if exist "%%~fJ" set "JAVA_EXE=%%~fJ"
  )
)
if not defined JAVA_EXE (
  for /f "delims=" %%J in ('where java.exe 2^>nul') do if not defined JAVA_EXE set "JAVA_EXE=%%~fJ"
)
if defined JAVA_EXE echo [OK] Java: %JAVA_EXE%

set "PLANTUML_JAR="
for /L %%I in (0,1,2) do (
  for %%P in ("!PLANTUML_JAR_CAND[%%I]!") do (
    if not defined PLANTUML_JAR if exist "%%~fP" set "PLANTUML_JAR=%%~fP"
  )
)
if defined PLANTUML_JAR echo [OK] PlantUML: %PLANTUML_JAR%

REM (^_^) rebuild diagrams (*.puml -> svg)
set "RENDERED=0"
if defined JAVA_EXE if defined PLANTUML_JAR (
  echo [1/3] PlantUML build...
  for /r "%PUML_INPUT_DIR%" %%F in (%PUML_EXT%) do (
    echo   - %%~fF
    "%JAVA_EXE%" -jar "%PLANTUML_JAR%" -tsvg "%%~fF" -o %PUML_OUT_REL% 1>nul
    if not errorlevel 1 set "RENDERED=1"
  )
  if "%RENDERED%"=="1" echo   => done :)
) else (
  echo [INFO] skip PlantUML (no Java/jar) :|
)

REM (^_^) mkdocs build (if mkdocs.yml + mkdocs.exe) ? no goto in ()
set "MKDOCS_EXE="
for /L %%I in (0,1,1) do (
  for %%M in ("!MKDOCS_CAND[%%I]!") do (
    if not defined MKDOCS_EXE if exist "%%~fM" set "MKDOCS_EXE=%%~fM"
  )
)
if defined MKDOCS_EXE (
  if exist "mkdocs.yml" (
    echo [2/3] mkdocs build...
    "%MKDOCS_EXE%" build 1>nul
    if errorlevel 1 ( echo [WARN] mkdocs failed (>_<) ) else ( echo   => done :) )
  ) else (
    echo [INFO] skip mkdocs (no mkdocs.yml)
  )
) else (
  echo [INFO] skip mkdocs (no mkdocs.exe)
)

REM (^_^) sync to origin/main (rebase -> push)
echo [3/3] sync to origin/main...
git remote -v | findstr /i "origin" >nul || (
  echo [ERROR] no remote "origin" (T_T)
  echo tip: git remote add origin https://github.com/<USER>/<REPO>.git
  exit /b 1
)

git rev-parse --abbrev-ref HEAD | findstr /i "^main$" >nul || (
  git switch -c main 2>nul || git switch main 2>nul || git checkout -B main
)
git fetch origin 1>nul
git pull --rebase origin main 1>nul || git pull --rebase origin main --allow-unrelated-histories 1>nul

set "DIFF="
for /f "delims=" %%S in ('git status --porcelain') do set "DIFF=1"
if defined DIFF (
  git add -A
  git commit -m "%COMMIT_MSG%" 1>nul
)

git push -u origin main
if errorlevel 1 (
  echo [WARN] push failed... fallback -> initial-sync
  git push -u origin HEAD:refs/heads/initial-sync
) else (
  echo [OK] sync done (^_^)
)

git status -sb
endlocal
