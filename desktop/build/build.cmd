@echo off

set NAME=PasswordManager1.0.4
set ROOT=C:\Projects\Python\PasswordManager\desktop
set MAIN=%ROOT%\main.py
set BUILD=%ROOT%\build
set OUTDIR=%BUILD%\Releases\%NAME%
set REQUIREMENTS=%ROOT%\requirements.txt
set VENV=%BUILD%\.venv
set ASSETS=%ROOT%\.assets
set ICON=%ASSETS%\icon.ico

rmdir /s /q %VENV%
python -m venv %VENV%
%VENV%\Scripts\python.exe -m pip install --upgrade pip
%VENV%\Scripts\python.exe -m pip install nuitka
%VENV%\Scripts\python.exe -m pip install -r %REQUIREMENTS%
%VENV%\Scripts\python.exe -m nuitka ^
    --windows-icon-from-ico=%ICON% ^
    --output-dir=%OUTDIR% ^
    --nofollow-import-to=tkinter ^
    --enable-plugin=pyside6 ^
    --standalone ^
    --follow-imports ^
    --onefile ^
    %MAIN%
xcopy %ASSETS% %OUTDIR%\.assets /e /s /t /i /h /k /c /o /y

pause