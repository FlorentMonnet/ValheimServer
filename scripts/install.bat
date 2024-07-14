@echo off

REM  Install chocolatey
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

REM  Install chocolatey librairies
SET choco_librairies=python3

(FOR %%a IN (%choco_librairies%) DO ( 
   choco install -y %%a 
))

CALL "%ProgramData%\chocolatey\bin\RefreshEnv.cmd"

REM Install python librairies

CD ../src 

python -m pip install --upgrade pip --user
pip install -r requirements.txt