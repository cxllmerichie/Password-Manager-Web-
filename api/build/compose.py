from subprocess import Popen, PIPE
from os import path


commands = [
    f"docker-compose -p postgres -f {path.abspath('postgres.yml')} up -d --build",
    f"docker-compose -p redis -f {path.abspath('redis.yml')} up -d --build"
]
for command in commands:
    print(f'{command}')
    process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE)
    out, err = process.communicate()
    print(f'{out.decode()}')
