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
    max_address = 0x00007fffffffffff  # 0x7******** adreslerine kadar arama yapıyoruz
    
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
            # Adresin 0x7******** olmamasını kontrol et
            if base_address > 0x700000000000:  # Bellek bölgesi 0x700000000000'den büyükse atlıyoruz
                break
            
            memory_ranges.append((base_address, region_size))
        
        address += region_size
    
    return memory_ranges

# Bellekte belirli bir değeri aramak ve kaydetmek
def scan_memory(process_handle, search_value=None, value_type='int'):
    memory_ranges = get_memory_ranges(process_handle)
    found_addresses = {}  # Bulunan adresler ve değerleri burada tutulacak
    for base_address, region_size in memory_ranges:
        address = base_address
        while address < base_address + region_size:
            memory_value = read_memory(process_handle, address, 4)  # 4 byte (int) boyutunda okuma yapıyoruz
            if memory_value:
                int_value = int.from_bytes(memory_value, byteorder='little')
                if search_value is None or int_value == search_value:
                    found_addresses[hex(address)] = int_value  # Adres ve değeri kaydet
            address += 4  # 4 byte'lık adım atıyoruz (int için)
    
    return found_addresses

# Bulunan adresleri ve değerlerini JSON dosyasına kaydetme
def save_addresses_to_json(addresses, filename='found_addresses.json'):
    with open(filename, 'w') as file:
        json.dump(addresses, file, indent=4)
    print(f"Bulunan adresler ve değerler '{filename}' dosyasına kaydedildi.")

# Kaydedilen adreslerdeki değişiklikleri kontrol etme
def check_for_changes(process_handle, filename='found_addresses.json'):
    try:
        with open(filename, 'r') as file:
            saved_addresses = json.load(file)
    except FileNotFoundError:
        print(f"'{filename}' dosyası bulunamadı.")
        return

    changed_values = {}  # Değişen adresler burada tutulacak
    for address, old_value in saved_addresses.items():
        try:
            current_value = read_memory(process_handle, int(address, 16), 4)
            if current_value:
                int_value = int.from_bytes(current_value, byteorder='little')
                if int_value != old_value:  # Değer değişmişse kaydet
                    changed_values[address] = {"old": old_value, "new": int_value}
        except Exception as e:
            print(f"Adres {address} okunurken hata: {e}")
    
    if changed_values:
        print("Değişen adresler ve değerler:")
        for address, values in changed_values.items():
            print(f"Adres {address} - Eski değer: {values['old']}, Yeni değer: {values['new']}")
    else:
        print("Hiçbir değer değişmemiş.")
    
    return changed_values
