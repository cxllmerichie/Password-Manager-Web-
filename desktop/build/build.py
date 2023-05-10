from subprocess import PIPE, Popen
from os import getcwd, path, pardir, remove as rmfile, walk
from shutil import rmtree as rmdir
from zipfile import ZipFile


if __name__ == '__main__':
    VERSION = '2.1'
    NAME = 'BrightnessControl'
    ROOT = path.abspath(path.join(getcwd(), pardir))
    MAIN = f'{ROOT}\\main.py'
    BUILD = f'{ROOT}\\build'
    ICON = f'{ROOT}\\assets\\icon.ico'

    command = f'pyinstaller --onefile --windowed --specpath {BUILD} --workpath {BUILD} --distpath {BUILD} --icon={ICON} --name={NAME} {MAIN}'

    process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE)
    out, err = process.communicate()
    print(f'{command}\n{out.decode()}')

    rmdir(f'{BUILD}\\{NAME}')
    rmfile(f'{BUILD}\\{NAME}.spec')

    with ZipFile(f'{ROOT}\\Releases\\{NAME}-v{VERSION}.zip', 'w') as zip_release:
        zip_release.write(f'{NAME}.exe')
        for dirpath, dirnames, filenames in walk(f'{ROOT}\\assets'):
            for filename in filenames:
                zip_release.write(path.join(dirpath, filename), f'assets/{filename}')

    rmfile(f'{BUILD}\\{NAME}.exe')
