import ctypes
import ctypes.wintypes
from ctypes import wintypes

# Gerekli Windows API sabitleri ve fonksiyonları
PROCESS_ALL_ACCESS = 0x1F0FFF

# Windows API bağlantısı
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# Bellek okuma işlemi
def read_memory(process_handle, address, size):
    buffer = ctypes.create_string_buffer(size)
    bytesRead = ctypes.c_size_t(0)
    
    if not kernel32.ReadProcessMemory(process_handle, ctypes.c_void_p(address), buffer, size, ctypes.byref(bytesRead)):
        raise ctypes.WinError(ctypes.get_last_error())
    
    return buffer.raw

# Process açma
def open_process(pid):
    process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not process_handle:
        raise ctypes.WinError(ctypes.get_last_error())
    
    return process_handle

# Process'i kapatma
def close_process(process_handle):
    kernel32.CloseHandle(process_handle)
