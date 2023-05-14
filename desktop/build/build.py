from os import getcwd, path, pardir, remove as rmfile, walk
from subprocess import PIPE, Popen
from shutil import rmtree as rmdir
from zipfile import ZipFile
from logging import getLogger


VERSION, NAME = '1.0.2', 'PasswordManager'

ROOT = 'C:\\Projects\\Python\\PasswordManager\\desktop'
MAIN = f'{ROOT}\\main.py'
BUILD = f'{ROOT}\\build'
OUTDIR = f'{BUILD}\\{NAME}{VERSION}'
REQUIREMENTS = f'{ROOT}\\requirements.txt'
VENV = f'{BUILD}\\.venv'

ASSETS = f'{ROOT}\\.assets'
ICON = f'{ASSETS}\\icon.ico'
SCREEN = f'{ROOT}\\background.png'


if __name__ == '__main__':
    for command in (
        f'rmdir /s /q {VENV}',

        f'python -m venv {VENV}',

        f'{VENV}\\Scripts\\python.exe -m pip install --upgrade pip',

        f'{VENV}\\Scripts\\python.exe -m pip install nuitka',

        f'{VENV}\\Scripts\\python.exe -m pip install -r {REQUIREMENTS}',

        f'{VENV}\\Scripts\\python.exe -m nuitka '
        f'--standalone '
        f'--output-dir={OUTDIR} '
        f'--enable-plugin=pyside6 '
        f'--nofollow-import-to=tkinter '
        f'--onefile '
        f'--follow-imports '
        f'--windows-icon-from-ico={ICON} '
        # f'--disable-console 
        # f'--onefile-windows-splash-screen-image={SCREEN} '  # No support for splash screens with MinGW64 yet, only works with MSVC
        f'{MAIN}',

        f'xcopy {ASSETS} {OUTDIR}\\.assets /E /I /H /K /O /Y'
    ):
        process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE)
        # getLogger().info(command)
        print(command)
        out, err = process.communicate()
        # getLogger().info(out.decode())
        print(out.decode())

    # rmdir(f'{BUILD}\\{NAME}')
    # rmfile(f'{BUILD}\\{NAME}.spec')

    # with ZipFile(f'{BUILD}\\Releases\\{NAME}-v{VERSION}.zip', 'w') as zip_release:
    #     zip_release.write(f'{NAME}.exe')
    #     for dirpath, dirnames, filenames in walk(f'{ROOT}\\.assets'):
    #         for filename in filenames:
    #             zip_release.write(path.join(dirpath, filename), f'.assets\\{filename}')
    #
    # rmfile(f'{BUILD}\\{NAME}.exe')
