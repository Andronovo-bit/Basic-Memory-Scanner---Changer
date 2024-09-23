import ctypes

# Gerekli Windows API sabitleri ve fonksiyonları
PROCESS_ALL_ACCESS = 0x1F0FFF

# Windows API bağlantısı
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# Bellek yazma işlemi
def write_memory(process_handle, address, data, size):
    buffer = ctypes.create_string_buffer(data.to_bytes(size, byteorder='little'))
    bytesWritten = ctypes.c_size_t(0)
    
    if not kernel32.WriteProcessMemory(process_handle, ctypes.c_void_p(address), buffer, size, ctypes.byref(bytesWritten)):
        raise ctypes.WinError(ctypes.get_last_error())

# Process açma
def open_process(pid):
    process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not process_handle:
        raise ctypes.WinError(ctypes.get_last_error())
    
    return process_handle

# Process kapama
def close_process(process_handle):
    kernel32.CloseHandle(process_handle)
