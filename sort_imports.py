import os

import isort

paths = [os.getcwd(), os.path.join(os.getcwd(), 'webapp')]

for path in paths:
    with os.scandir(path) as loe:
        for entry in loe:
            if entry.is_file() and entry.name.endswith('.py'):
                print(entry.name)
                isort.file(os.path.join(path, entry.name))

