from src.process.process_list import list_all_processes

def search_process_by_name(name):
    """İşlem adı ile çalışan işlemleri ara"""
    processes = list_all_processes()
    results = [proc for proc in processes if name.lower() in proc['name'].lower()]
    return results

def search_process_by_pid(pid):
    """PID ile çalışan işlemi ara"""
    processes = list_all_processes()
    results = [proc for proc in processes if proc['pid'] == pid]
    return results
