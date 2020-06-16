r"""Python interface to the CAS DLL

v1.0

Use at your own risk.
"""

from pyclibrary import CParser, CLibrary
from pathlib import Path
from ctypes import create_string_buffer
import os


class CasDll(object):
    def __init__(self, cache_path="cache", lib_path=None, header_path=None):
        if not header_path:
            header_path = r"C:\Program Files\Instrument Systems\CAS4x64-SDK\VC2013\CAS4.h"
        if not lib_path:
            lib_path = r"C:\Windows\System32\CAS4x64.dll"
        lib_name = Path(lib_path).name
        if cache_path:
            cache_name = lib_name + ".cache"
            cache_path_ = Path(cache_path)
            cache_path_.mkdir(parents=True, exist_ok=True)
            cache_file_path = str(cache_path_ / cache_name)
        else:
            cache_file_path = None
        self.parser = CParser(
            header_path,
            cache=cache_file_path,
            # The handling of "__stdcall" is buggy in pyclibrary, here is a workaround.
            # See also https://github.com/MatthieuDartiailh/pyclibrary/issues/38
            replace={"#define __callconv __stdcall": "#define __callconv"})
        # To see what has been parsed, call:
        #    parser.print_all()

        self.clib = CLibrary(lib_path, self.parser)

    def new_struct(self, name):
        classs = getattr(self.clib, name)
        return classs()

    def has_function(self, name):
        try:
            self.clib._get_function(name)
            return True
        except KeyError:
            return False

    def check_cas4_error_code(self, code):
        if (code < self.clib.ErrorNoError):
            p = create_string_buffer(255)
            self.clib.casGetErrorMessageA(code, p, 255)
            raise Exception("CAS DLL reported error: code=" + str(code) +
                            " message=" + p.value.decode())

    def check_cas4_device_error(self, casid):
        self.check_cas4_error_code(self.clib.casGetError(casid).rval)

    def __getattr__(self, name):
        return getattr(self.clib, name)

