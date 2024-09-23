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
        return None
    return buffer.raw

# Process açma
def open_process(pid):
    process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not process_handle:
        raise ctypes.WinError(ctypes.get_last_error())
    
    return process_handle

# Process kapama
def close_process(process_handle):
    kernel32.CloseHandle(process_handle)

# Bellekte belirli bir değeri aramak için tarama
def scan_memory(process_handle, start_address, end_address, value, value_type='int'):
    address = start_address
    while address < end_address:
        if value_type == 'int':
            memory_value = read_memory(process_handle, address, 4)
            if memory_value:
                int_value = int.from_bytes(memory_value, byteorder='little')
                if int_value == value:
                    print(f"Value found at address: {hex(address)}")
        address += 4  # 4 byte adım atıyoruz (int için)

# Process'in bellek alanlarını bulma (Windows için basit bir örnek)
def get_memory_ranges(pid):
    # Burada detaylı bellek taraması için bölge adreslerini ve büyüklüklerini çekebiliriz.
    # Daha karmaşık bellek yöneticilerine ihtiyaç duyulabilir.
    # Örneğin VirtualQueryEx kullanabiliriz.
    pass
