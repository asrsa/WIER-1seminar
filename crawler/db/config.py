import os
from configparser import ConfigParser


def config(section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    databasePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.ini')
    parser.read(databasePath)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, databasePath))
    return db
