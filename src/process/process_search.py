from typing import List, Dict
from src.process.process_list import list_all_processes

def search_process_by_name(name: str) -> List[Dict[str, str]]:
    """
    Search for running processes by name.

    Args:
        name (str): The name of the process to search for.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing process information.
    """
    try:
        processes = list_all_processes()
        results = [proc for proc in processes if name.lower() in proc['name'].lower()]
        return results
    except Exception as e:
        print(f"Error occurred while searching for process by name '{name}': {e}")
        return []

def search_process_by_pid(pid: int) -> List[Dict[str, str]]:
    """
    Search for a running process by PID.

    Args:
        pid (int): The PID of the process to search for.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing process information.
    """
    try:
        processes = list_all_processes()
        results = [proc for proc in processes if proc['pid'] == pid]
        return results
    except Exception as e:
        print(f"Error occurred while searching for process by PID '{pid}': {e}")
        return []