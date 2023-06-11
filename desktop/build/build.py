from subprocess import PIPE, Popen


name = 'PasswordManager'
root = 'C:\\Projects\\Python\\PasswordManager\\desktop'
main = f'{root}\\main.py'
build = f'{root}\\build\\v8'
icon = f'{root}\\.assets\\icon.ico'
command = f'pyinstaller -p {root} --onefile --windowed --specpath {build} --workpath {build} --distpath {build} --icon={icon} --name={name} {main}'
process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE)
out, err = process.communicate()
print(f'{command}\n{out.decode()}')
