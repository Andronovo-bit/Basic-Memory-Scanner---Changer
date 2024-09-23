import ctypes
import ctypes.wintypes

# Windows API sabitleri
PROCESS_ALL_ACCESS = 0x1F0FFF
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# Bellek okuma işlemi (hatalara karşı daha dayanıklı)
def read_memory(process_handle, address, size):
    buffer = ctypes.create_string_buffer(size)
    bytesRead = ctypes.c_size_t(0)

    # Belleği küçük parçalara ayırarak okuma denemesi
    try:
        result = kernel32.ReadProcessMemory(process_handle, ctypes.c_void_p(address), buffer, size, ctypes.byref(bytesRead))
        if not result:
            error = ctypes.get_last_error()
            if error == 299:  # WinError 299: Sadece bir kısmı tamamlandı hatası
                # Sadece kısmi okuma yapıldığında bu durumu yönetiyoruz
                print(f"Partial read error at address {hex(address)}: [WinError {error}]")
            else:
                raise ctypes.WinError(error)
        return buffer.raw
    except Exception as e:
        print(f"Bellek okuma hatası adres: {hex(address)}, hata: {e}")
        return None

# Process açma
def open_process(pid):
    process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not process_handle:
        raise ctypes.WinError(ctypes.get_last_error())
    
    return process_handle

# Process kapama
def close_process(process_handle):
    kernel32.CloseHandle(process_handle)
