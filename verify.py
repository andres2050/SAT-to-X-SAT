import sys
import subprocess
import pkg_resources
import struct

required = {'python-sat', 'wrapt_timeout_decorator'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

if sys.version_info.major != 3 or sys.version_info.minor <= 6:
    print("Se requiere Python 3.6 o superior de 64 Bits.")
    print("Estás usando Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    exit()

get_bits = 8 * struct.calcsize("P")
if get_bits != 64:
    print("No se ha encontrado una versión de Python 3.6+ 64 Bits.")
    print("Estas usando Python de {} Bits.".format(get_bits))
    exit()
