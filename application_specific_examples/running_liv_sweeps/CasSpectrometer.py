# Goal: 
# Vektrex interface to CAS4 Spectrometer
# Version 1.0.0
# 
# Expectation: 
# Uses the PyCLibrary to create a wrapper for the native C CAS4x64.dll
# For more info, see the PyCLibrary website: https://pyclibrary.readthedocs.io/en/latest/

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
            replace={"#define __callconv __stdcall": "#define __callconv"})

        self.clib = CLibrary(lib_path, self.parser)

    def new_struct(self, name):
        class_ = getattr(self.clib, name)
        return class_()

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
            raise Exception("CAS Spectrometer Error: {}, {}".format(str(code), p.value.decode()))

    def check_cas4_device_error(self, casid):
        self.check_cas4_error_code(self.clib.casGetError(casid).rval)

    def __getattr__(self, name):
        return getattr(self.clib, name)

