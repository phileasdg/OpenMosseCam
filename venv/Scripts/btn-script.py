#!C:\Users\phile\PycharmProjects\OpenMosseCam\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'button==0.0.3.post3','console_scripts','btn'
__requires__ = 'button==0.0.3.post3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('button==0.0.3.post3', 'console_scripts', 'btn')()
    )
