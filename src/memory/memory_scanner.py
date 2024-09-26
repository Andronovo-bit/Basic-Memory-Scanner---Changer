import json
from src.memory.memory_reader import read_memory
import ctypes
from ctypes import wintypes
from typing import Dict, Any

# MEMORY_BASIC_INFORMATION structure definition
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

# Windows API functions
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
VirtualQueryEx = kernel32.VirtualQueryEx

def get_memory_ranges(process_handle: int) -> list:
    """
    Get memory ranges of a process.

    Args:
        process_handle (int): Handle to the process.

    Returns:
        list: List of memory ranges.
    """
    memory_ranges = []
    address = 0x0000000000
    max_address = 0x00007fffffffffff  # Search up to 0x7******** addresses
    
    mbi = MEMORY_BASIC_INFORMATION()
    while address < max_address:
        result = VirtualQueryEx(process_handle, ctypes.c_void_p(address), ctypes.byref(mbi), ctypes.sizeof(mbi))
        
        if result == 0:
            break
        
        base_address = mbi.BaseAddress
        region_size = mbi.RegionSize
        state = mbi.State
        protect = mbi.Protect

        # Scan regions with PAGE_READWRITE and PAGE_READONLY permissions
        if state == 0x1000 and (protect == 0x04 or protect == 0x02):  # MEM_COMMIT and PAGE_READWRITE or PAGE_READONLY
            if base_address > 0x700000000000:  # Skip memory regions greater than 0x700000000000
                break
            
            memory_ranges.append((base_address, region_size))
        
        address += region_size
    
    return memory_ranges

def scan_memory(process_handle: int, search_value: int = None, value_type: str = 'int') -> Dict[str, Any]:
    """
    Scan memory for a specific value.

    Args:
        process_handle (int): Handle to the process.
        search_value (int, optional): Value to search for. Defaults to None.
        value_type (str, optional): Type of value. Defaults to 'int'.

    Returns:
        Dict[str, Any]: Found addresses and their values.
    """
    memory_ranges = get_memory_ranges(process_handle)
    found_addresses = {}
    for base_address, region_size in memory_ranges:
        address = base_address
        while address < base_address + region_size:
            memory_value = read_memory(process_handle, address, 4)  # Read 4 bytes (int)
            if memory_value:
                int_value = int.from_bytes(memory_value, byteorder='little')
                if search_value is None or int_value == search_value:
                    found_addresses[hex(address)] = int_value  # Save address and value
            address += 4  # Step by 4 bytes (int)
    
    return found_addresses

def save_addresses_to_json(addresses: Dict[str, Any], filename: str = 'found_addresses.json') -> None:
    """
    Save found addresses and values to a JSON file.

    Args:
        addresses (Dict[str, Any]): Addresses and values to save.
        filename (str, optional): Filename to save to. Defaults to 'found_addresses.json'.
    """
    with open(filename, 'w') as file:
        json.dump(addresses, file, indent=4)
    print(f"Found addresses and values saved to '{filename}'.")

def check_for_changes(process_handle: int, filename: str = 'found_addresses.json') -> Dict[str, Dict[str, int]]:
    """
    Check for changes in saved memory addresses.

    Args:
        process_handle (int): Handle to the process.
        filename (str, optional): Filename to read saved addresses from. Defaults to 'found_addresses.json'.

    Returns:
        Dict[str, Dict[str, int]]: Changed addresses and their old and new values.
    """
    try:
        with open(filename, 'r') as file:
            saved_addresses = json.load(file)
    except FileNotFoundError:
        print(f"'{filename}' not found.")
        return {}

    changed_values = {}
    for address, old_value in saved_addresses.items():
        try:
            current_value = read_memory(process_handle, int(address, 16), 4)
            if current_value:
                int_value = int.from_bytes(current_value, byteorder='little')
                if int_value != old_value:  # Save if value has changed
                    changed_values[address] = {"old": old_value, "new": int_value}
        except Exception as e:
            print(f"Error reading address {address}: {e}")
    
    if changed_values:
        print("Changed addresses and values:")
        for address, values in changed_values.items():
            print(f"Address {address} - Old value: {values['old']}, New value: {values['new']}")
    else:
        print("No values have changed.")
    
    return changed_values