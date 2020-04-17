##  Test program

#   Imports

##  Main program

#   Imports

import hashlib

m = hashlib.md5()

m.update(b"8")

f_id = str(m.hexdigest())

print(f_id)