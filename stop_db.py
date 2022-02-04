from dotenv import load_dotenv
import os
import platform

load_dotenv()

QUESTDB_PATH = os.path.abspath(os.getenv('QUESTDB_PATH'))

print("Stopping database...")


platform_system = platform.system()

if platform_system == 'Windows':
    os.system(f"{os.path.join(QUESTDB_PATH, 'questdb.exe')} stop")
elif platform_system == 'Linux':
    os.system(f"./{os.path.join(QUESTDB_PATH, 'questdb.sh')} stop")
elif platform_system == 'Darwin': # mac
    raise NotImplementedError
else:
    exit('Error: Unrecognized platform')