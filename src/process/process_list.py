from typing import List, Dict
import psutil

def list_all_processes() -> List[Dict[str, str]]:
    """
    List all processes sorted by their name, excluding duplicates.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing process information.
    """
    try:
        seen_names = set()
        processes = sorted(
            (
                proc.info for proc in psutil.process_iter(['pid', 'name'])
                if proc.info['name'] not in seen_names and not seen_names.add(proc.info['name'])
            ),
            key=lambda x: x['name']
        )
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        processes = []

    return processes