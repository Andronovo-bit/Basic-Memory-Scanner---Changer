import json
from src.memory.memory_reader import read_memory
import ctypes
from ctypes import wintypes

# MEMORY_BASIC_INFORMATION yapısını tanımlıyoruz
class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p),
        ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", wintypes.DWORD),
        ("RegionSize", ctypes.c_size_t),
        ("State", wintypes.DWORD),
        ("Protect", wintypes.DWORD),
        ("Type", wintypes.DWORD),
    ]

# Windows API fonksiyonları
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
VirtualQueryEx = kernel32.VirtualQueryEx

# Bellek bilgilerini elde etme (VirtualQueryEx kullanarak)
def get_memory_ranges(process_handle):
    memory_ranges = []
    address = 0x0000000000
    max_address = 0x00007fffffffffff
    
    mbi = MEMORY_BASIC_INFORMATION()
    while address < max_address:
        result = VirtualQueryEx(process_handle, ctypes.c_void_p(address), ctypes.byref(mbi), ctypes.sizeof(mbi))
        
        if result == 0:
            break
        
        base_address = mbi.BaseAddress
        region_size = mbi.RegionSize
        state = mbi.State
        protect = mbi.Protect

        # PAGE_READWRITE ve PAGE_READONLY izinlerine sahip bölgeleri tarıyoruz
        if state == 0x1000 and (protect == 0x04 or protect == 0x02):  # MEM_COMMIT ve PAGE_READWRITE veya PAGE_READONLY
            if base_address > 0x700000000000:  # Bellek bölgesi 0x700000000000'den büyükse atlıyoruz
                break
            memory_ranges.append((base_address, region_size))
        
        address += region_size
    
    return memory_ranges

# Bellekte belirli bir değeri aramak için tarama (belirli bellek aralıklarında)
def scan_memory(process_handle, search_value, value_type='int'):
    memory_ranges = get_memory_ranges(process_handle)
    found_addresses = []  # Bulunan adresler burada tutulacak
    for base_address, region_size in memory_ranges:
        address = base_address
        while address < base_address + region_size:
            memory_value = read_memory(process_handle, address, 4)  # 4 byte (int) boyutunda okuma yapıyoruz
            if memory_value:
                int_value = int.from_bytes(memory_value, byteorder='little')
                if int_value == search_value:
                    print(f"Value found at address: {hex(address)}")
                    found_addresses.append(hex(address))  # Bulunan adresi listeye ekle
            address += 4  # 4 byte'lık adım atıyoruz (int için)
    
    # Bulunan adresleri JSON dosyasına kaydetme
    save_addresses_to_json(found_addresses)
    
    return found_addresses

# Bulunan adresleri JSON dosyasına kaydetme
def save_addresses_to_json(addresses, filename='found_addresses.json'):
    with open(filename, 'w') as file:
        json.dump(addresses, file, indent=4)
    print(f"Bulunan adresler '{filename}' dosyasına kaydedildi.")
