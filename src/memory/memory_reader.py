import ctypes
import ctypes.wintypes
from typing import Optional

# Windows API constants
PROCESS_ALL_ACCESS = 0x1F0FFF
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

def read_memory(process_handle: int, address: int, size: int) -> Optional[bytes]:
    """
    Read memory from a process.

    Args:
        process_handle (int): Handle to the process.
        address (int): Memory address to read from.
        size (int): Number of bytes to read.

    Returns:
        Optional[bytes]: The read bytes, or None if an error occurred.
    """
    buffer = ctypes.create_string_buffer(size)
    bytes_read = ctypes.c_size_t(0)

    try:
        result = kernel32.ReadProcessMemory(process_handle, ctypes.c_void_p(address), buffer, size, ctypes.byref(bytes_read))
        if not result:
            error = ctypes.get_last_error()
            if error == 299:  # WinError 299: Only part of a ReadProcessMemory or WriteProcessMemory request was completed.
                print(f"Partial read error at address {hex(address)}: [WinError {error}]")
            else:
                raise ctypes.WinError(error)
        return buffer.raw
    except ctypes.WinError as e:
        print(f"Memory read error at address {hex(address)}, error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error at address {hex(address)}, error: {e}")
        return None

def open_process(pid: int) -> int:
    """
    Open a process by PID.

    Args:
        pid (int): Process ID.

    Returns:
        int: Handle to the process.

    Raises:
        ctypes.WinError: If the process cannot be opened.
    """
    process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not process_handle:
        raise ctypes.WinError(ctypes.get_last_error())
    
    return process_handle

def close_process(process_handle: int) -> None:
    """
    Close a process handle.

    Args:
        process_handle (int): Handle to the process.
    """
    kernel32.CloseHandle(process_handle)