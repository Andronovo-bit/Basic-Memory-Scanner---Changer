from src.process.process_list import list_all_processes
from src.process.process_search import search_process_by_name, search_process_by_pid
from src.memory.memory_reader import open_process, close_process
from src.memory.memory_writer import write_memory
from src.memory.memory_scanner import scan_memory, save_addresses_to_json, check_for_changes
from src.config.config import Config

def main_menu():
    print("1. List Processes")
    print("2. Search Process by Name")
    print("3. Search Process by PID")
    print("4. Scan Memory")
    print("5. Write Memory")
    print("6. Check for Memory Changes")
    print("7. Exit")
    return input("Choose an option: ").strip()

def list_processes():
    processes = list_all_processes()
    print(f"Toplam {len(processes)} process bulundu:\n")
    for process in processes:
        print(f"PID: {process['pid']}, Name: {process['name']}")

def search_process_by_name_menu():
    name = input("Aramak istediğiniz işlem adını girin: ").strip()
    results = search_process_by_name(name)
    if results:
        print(f"{len(results)} işlem bulundu:")
        for process in results:
            print(f"PID: {process['pid']}, Name: {process['name']}")
    else:
        print("İşlem bulunamadı.")

def search_process_by_pid_menu():
    pid_input = input("Aramak istediğiniz işlem PID'sini girin: ").strip()
    try:
        pid = int(pid_input)
        results = search_process_by_pid(pid)
        if results:
            print(f"PID: {results[0]['pid']}, Name: {results[0]['name']}")
        else:
            print("İşlem bulunamadı.")
    except ValueError:
        print(Config.INVALID_PID)

def scan_memory_menu():
    pid_input = input("Bellek taraması için işlem PID'sini girin: ").strip()
    try:
        pid = int(pid_input)
        process_handle = open_process(pid)

        search_value = input("Aramak istediğiniz değeri girin: ")
        search_value = int(search_value)
        print(f"Aranan değer: {search_value}")

        # Bellek taraması ve JSON dosyasına kaydetme
        found_addresses = scan_memory(process_handle, search_value)
        save_addresses_to_json(found_addresses)

        close_process(process_handle)
    except ValueError:
        print(Config.INVALID_PID)
    except Exception as e:
        print(f"Bellek okuma hatası: {e}")
    return

def write_memory_menu():
    pid_input = input("Bellek değeri değiştirmek için işlem PID'sini girin: ").strip()
    try:
        pid = int(pid_input)
        process_handle = open_process(pid)

        # Kullanıcıdan adresi ve yeni değeri iste
        address = input("Değeri değiştirmek istediğiniz bellek adresini girin (hex formatında): ").strip()
        address = int(address, 16)
        new_value = input("Yeni değer girin: ").strip()
        new_value = int(new_value)

        # Bellekte yazma işlemi
        write_memory(process_handle, address, new_value, 4)
        print(f"Değer {hex(address)} adresinde {new_value} olarak değiştirildi.")

        close_process(process_handle)
    except ValueError:
        print(Config.INVALID_PID)
    except Exception as e:
        print(f"Bellek yazma hatası: {e}")
    return

def check_memory_changes_menu():
    pid_input = input("Bellek değişikliklerini kontrol etmek için işlem PID'sini girin: ").strip()
    try:
        pid = int(pid_input)
        process_handle = open_process(pid)

        # Bellek değişikliklerini kontrol etme
        check_for_changes(process_handle)

        close_process(process_handle)
    except ValueError:
        print(Config.INVALID_PID)
    except Exception as e:
        print(f"Bellek okuma hatası: {e}")
    return

def main():
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