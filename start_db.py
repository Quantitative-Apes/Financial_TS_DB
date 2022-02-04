from dotenv import load_dotenv
import os
import platform

load_dotenv()

QUESTDB_PATH = os.path.abspath(os.getenv('QUESTDB_PATH'))

print("Running database...")


platform_system = platform.system()

if platform_system == 'Windows':
    os.system(f"{os.path.join(QUESTDB_PATH, 'questdb.exe')} start")
elif platform_system == 'Linux':
    os.system(f"./{os.path.join(QUESTDB_PATH, 'questdb.sh')} start")
elif platform_system == 'Darwin': # mac
    raise NotImplementedError
else:
    exit('Error: Unrecognized platform')