import subprocess


name = 'PasswordGenerator'
root = 'C:\\Projects\\Python\\PasswordGenerator'
main = f'{root}\\main.py'
build = f'{root}\\build'
icon = f'{root}\\assets\\icon-black.ico'
commands = [
    f'pyinstaller --onefile --windowed --specpath {build} --workpath {build} --distpath {build} --icon={icon} --name={name} {main}',
    f'exit'
]

for command in commands:
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate()
    print(f'{command}\n{out.decode()}')
