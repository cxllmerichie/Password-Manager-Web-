from contextlib import redirect_stdout
from io import StringIO
from datetime import datetime
from functools import wraps


database = './Database/pypmdb.txt'
flask = './Frontend/flask.txt'


def log(filename: str = 'log'):
    def decorator(sender):
        def message(context: str) -> str:
            source = str(repr(sender)).split(' ')[1]
            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            split, output, sep = context.split('\n'), '', '\n'
            for index, string in enumerate(split):
                if len(string) != 0:
                    output += f'\t{string}' if index == 0 else f'\n\t{string}'
            return f'{timestamp} | {source}\n{output}{"" if len(split) == 0 or len(split) == 1 else sep}'

        @wraps(sender)
        def wrapper(*argc, **kwargs):
            with open(filename, 'a') as file:
                try:
                    with StringIO() as buffer, redirect_stdout(buffer):
                        retval = sender(*argc, **kwargs)
                        file.write(message(buffer.getvalue()))
                    return retval
                except Exception as exception:
                    file.write(message(str(exception)))
        return wrapper
    return decorator
