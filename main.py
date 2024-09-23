from src.process.process_list import list_all_processes
from src.process.process_search import search_process_by_name, search_process_by_pid
from src.memory.memory_reader import open_process, close_process
from src.memory.memory_writer import write_memory
from src.memory.memory_scanner import scan_memory, save_addresses_to_json, check_for_changes
from src.config.config import Config

def main_menu():
    """Display the main menu and get user choice."""
    print("1. List Processes")
    print("2. Search Process by Name")
    print("3. Search Process by PID")
    print("4. Scan Memory")
    print("5. Write Memory")
    print("6. Check for Memory Changes")
    print("7. Exit")
    return input("Choose an option: ").strip()

def list_processes():
    """List all running processes."""
    processes = list_all_processes()
    print(f"Total {len(processes)} processes found:\n")
    for process in processes:
        print(f"PID: {process['pid']}, Name: {process['name']}")

def search_process_by_name_menu():
    """Search for processes by name."""
    name = input("Enter the process name to search: ").strip()
    results = search_process_by_name(name)
    if results:
        print(f"{len(results)} processes found:")
        for process in results:
            print(f"PID: {process['pid']}, Name: {process['name']}")
    else:
        print("No processes found.")

def search_process_by_pid_menu():
    """Search for a process by PID."""
    pid_input = input("Enter the PID of the process to search: ").strip()
    try:
        pid = int(pid_input)
        results = search_process_by_pid(pid)
        if results:
            print(f"PID: {results[0]['pid']}, Name: {results[0]['name']}")
        else:
            print("No process found.")
    except ValueError:
        print(Config.INVALID_PID)

def scan_memory_menu():
    """Scan the memory of a process."""
    pid_input = input("Enter the PID of the process to scan memory: ").strip()
    try:
        pid = int(pid_input)
        process_handle = open_process(pid)

        search_value = input("Enter the value to search for: ").strip()
        search_value = int(search_value)
        print(f"Searching for value: {search_value}")

        found_addresses = scan_memory(process_handle, search_value)
        save_addresses_to_json(found_addresses)

        close_process(process_handle)
    except ValueError:
        print(Config.INVALID_PID)
    except Exception as e:
        print(f"Memory read error: {e}")

def write_memory_menu():
    """Write a value to a specific memory address of a process."""
    pid_input = input("Enter the PID of the process to write memory: ").strip()
    try:
        pid = int(pid_input)
        process_handle = open_process(pid)

        address = input("Enter the memory address to change (in hex format): ").strip()
        address = int(address, 16)
        new_value = input("Enter the new value: ").strip()
        new_value = int(new_value)

        write_memory(process_handle, address, new_value, 4)
        print(f"Value at address {hex(address)} changed to {new_value}.")

        close_process(process_handle)
    except ValueError:
        print(Config.INVALID_PID)
    except Exception as e:
        print(f"Memory write error: {e}")

def check_memory_changes_menu():
    """Check for changes in memory values of a process."""
    pid_input = input("Enter the PID of the process to check memory changes: ").strip()
    try:
        pid = int(pid_input)
        process_handle = open_process(pid)

        check_for_changes(process_handle)

        close_process(process_handle)
    except ValueError:
        print(Config.INVALID_PID)
    except Exception as e:
        print(f"Memory read error: {e}")

def main():
    """Main function to run the memory analyzer."""
    print(Config.WELCOME_MESSAGE)

    while True:
        choice = main_menu()

        if choice == "1":
            list_processes()
        elif choice == "2":
            search_process_by_name_menu()
        elif choice == "3":
            search_process_by_pid_menu()
        elif choice == "4":
            scan_memory_menu()
        elif choice == "5":
            write_memory_menu()
        elif choice == "6":
            check_memory_changes_menu()
        elif choice == "7":
            print(Config.EXIT_PROMPT)
            break
        else:
            print(Config.INVALID_COMMAND)

if __name__ == "__main__":
    main()