from os import getcwd, path, pardir, remove as rmfile, walk
from subprocess import PIPE, Popen
from shutil import rmtree as rmdir
from zipfile import ZipFile


if __name__ == '__main__':
    VERSION = '1.1.1'
    NAME = 'PasswordManager'
    ROOT = path.abspath(path.join(getcwd(), pardir))
    MAIN = f'{ROOT}\\main.py'
    BUILD = f'{ROOT}\\build'
    ASSETS = f'{ROOT}\\.assets'
    ICON = f'{ASSETS}\\icon.ico'

    command = f'pyinstaller --add-data "{ASSETS};.assets" --noconsole --onefile --windowed --specpath {BUILD} --workpath {BUILD} --distpath {BUILD} --icon={ICON} --name={NAME} {MAIN}'

    process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE)
    print(command)
    out, err = process.communicate()
    print(out.decode())

    rmdir(f'{BUILD}\\{NAME}')
    rmfile(f'{BUILD}\\{NAME}.spec')

    # with ZipFile(f'{BUILD}\\Releases\\{NAME}-v{VERSION}.zip', 'w') as zip_release:
    #     zip_release.write(f'{NAME}.exe')
    #     for dirpath, dirnames, filenames in walk(f'{ROOT}\\.assets'):
    #         for filename in filenames:
    #             zip_release.write(path.join(dirpath, filename), f'.assets\\{filename}')
    #
    # rmfile(f'{BUILD}\\{NAME}.exe')
