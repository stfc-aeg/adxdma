from cffi import FFI
import sys
import os

cffi_driver_path = os.environ.get("ADXDMA_ROOT")
print(cffi_driver_path)

if not cffi_driver_path:
    raise Exception("NO ADXDMA_ROOT FOUND")


libdirs = [os.path.join(cffi_driver_path, 'api/linux/obj')]
include_dirs = [os.path.join(cffi_driver_path, 'include')]
libs = ['adxdma']

print(libdirs)
print(include_dirs)

ffibuilder = FFI()

ffibuilder.set_source("xdma_cffi",
                      r"""
                      #define LINUX
                      #include "adxdma.h"
                      #include <stdint.h>
                      """,
                      libraries=libs,
                      include_dirs=include_dirs, library_dirs=libdirs
                      )

if __name__ == "__main":
    with open("pyxdma.h", "r") as header:
        header_info = header.read()
else:
    with open("../lib/pyxdma.h", "r") as header:
        header_info = header.read()

ffibuilder.cdef(header_info)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True, debug=False)