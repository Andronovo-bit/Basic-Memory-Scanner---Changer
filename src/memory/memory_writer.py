import ctypes
from typing import Optional

# Windows API constants
PROCESS_ALL_ACCESS = 0x1F0FFF
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

def write_memory(process_handle: int, address: int, data: int, size: int) -> None:
    """
    Write memory to a process.

    Args:
        process_handle (int): Handle to the process.
        address (int): Memory address to write to.
        data (int): Data to write.
        size (int): Number of bytes to write.

    Raises:
        ctypes.WinError: If the memory write operation fails.
    """
    buffer = ctypes.create_string_buffer(data.to_bytes(size, byteorder='little'))
    bytes_written = ctypes.c_size_t(0)

    try:
        result = kernel32.WriteProcessMemory(process_handle, ctypes.c_void_p(address), buffer, size, ctypes.byref(bytes_written))
        if not result:
            raise ctypes.WinError(ctypes.get_last_error())
    except ctypes.WinError as e:
        print(f"Memory write error at address {hex(address)}, error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error at address {hex(address)}, error: {e}")
        raise

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