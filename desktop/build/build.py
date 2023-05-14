from os import getcwd, path, pardir, remove as rmfile, walk
from subprocess import PIPE, Popen
from shutil import rmtree as rmdir
from zipfile import ZipFile


if __name__ == '__main__':
    VERSION, NAME = '1.1.3', 'PasswordManager'

    # ROOT = path.abspath(path.join(getcwd(), pardir))
    ROOT = 'C:\\Projects\\Python\\PasswordManager\\desktop'
    MAIN = f'{ROOT}\\main.py'
    BUILD = f'{ROOT}\\build'
    OUTDIR = f'{BUILD}\\{NAME}'
    ASSETS = f'{ROOT}\\.assets'
    ICON = f'{ASSETS}\\icon.ico'

    command = f"python -m nuitka --standalone --output-dir={OUTDIR} --enable-plugin=pyside6 main.py"
    process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE)
    print(command)
    out, err = process.communicate()
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
