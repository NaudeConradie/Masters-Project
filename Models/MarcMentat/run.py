 ##  Main program

#   Imports

from py_mentat import *
from py_post import *

import subprocess
import time
import random

###################################################################

#   Main function


mentat_path = r'C:\Users\Naude Conradie\AppData\Roaming\MSC.Software\Marc\2019.0.0\mentat2019\bin\mentat.bat'

file_path = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\main.py'

p = subprocess.Popen([mentat_path, file_path], bufsize=2048)