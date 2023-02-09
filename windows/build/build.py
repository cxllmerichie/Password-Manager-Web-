import subprocess


name = 'PasswordManager'
root = 'C:\\Projects\\Python\\PasswordManager'
src = 'C:\\Projects\\Python\\PasswordManager\\src'
main = f'{root}\\main.py'
build = f'{root}\\build'
commands = [
    f'pyinstaller --onefile --windowed --specpath {build} --workpath {build} --distpath {build} --name={name} {main}'
]

for command in commands:
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate()
    print(f'{command}\n{out.decode()}')
