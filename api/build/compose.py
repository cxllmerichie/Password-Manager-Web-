from subprocess import Popen, PIPE
from os import path


if __name__ == '__main__':
    commands = [
        {'src': f"docker-compose -p postgres -f {path.abspath('postgres.yml')} up -d --build", 'alt': 'Creating PostgreSQL database'},
        {'src': f"docker-compose -p redis -f {path.abspath('redis.yml')} up -d --build", 'alt': 'Creating PostgreSQL database'}
    ]
    for command in commands:
        print(f"{command['alt']}")
        process = Popen(command['src'], shell=True, stdin=PIPE, stdout=PIPE)
        out, err = process.communicate()
        print(f'{out.decode()}')
