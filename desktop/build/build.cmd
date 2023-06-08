::@echo off

set NAME=nouvi-qfix-nostand-onef
set ROOT=C:\Projects\Python\PasswordManager\desktop
set MAIN=%ROOT%\main.py
set BUILD=%ROOT%\build
set OUTDIR=%BUILD%\Releases\%NAME%
set REQUIREMENTS=%ROOT%\requirements.txt
set VENV=%BUILD%\.venv
set ASSETS=%ROOT%\.assets
set ICON=%ASSETS%\icon.ico

::rmdir /s /q %VENV%
::python -m venv %VENV%
::%VENV%\Scripts\python.exe -m pip install --upgrade pip
::%VENV%\Scripts\python.exe -m pip install nuitka
::%VENV%\Scripts\python.exe -m pip install -r %REQUIREMENTS%
%VENV%\Scripts\python.exe -m nuitka ^
--windows-icon-from-ico=%ICON% ^
--output-dir=%OUTDIR% ^
--nofollow-import-to=tkinter ^
--enable-plugin=pyside6 ^
--standalone ^
%MAIN%
::    --follow-imports ^
::    --warn-implicit-exceptions ^
::    --warn-unusual-code ^
::    --show-progress ^
::    --show-modules ^
::    --remove-output ^
::    --onefile ^

xcopy %ASSETS% %OUTDIR%\.assets /E/H/C/I

pause

