##  Run program

#   Run from Visual Studio Code

#   Imports

from py_mentat import *
from py_post import *

import subprocess

###################################################################

#   Main function

mentat_path = r'C:\Users\Naude Conradie\AppData\Roaming\MSC.Software\Marc\2019.0.0\mentat2019\bin\mentat.bat'

file_path = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\main.py'

#   Mentat wants procedure file
#   Major code restructure required to generate procedure file
p = subprocess.Popen([mentat_path, file_path], bufsize=2048)