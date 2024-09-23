from src.process.process_list import list_all_processes
from src.process.process_search import search_process_by_name
from src.memory.memory_reader import open_process, close_process
from src.memory.memory_writer import write_memory
from src.memory.memory_scanner import scan_memory
from src.config.config import Config

def main_menu():
    print("\n=== Ana Menü ===")
    print("1. Process'leri listele")
    print("2. Process adı ile ara")
    print("3. Process ID ile ara")
    print("4. Bellek taraması yap ve JSON dosyasına kaydet")
    print("5. Bellekte değer değiştir")
    print("6. Çıkış")
    return input("Bir seçenek girin: ")

def list_processes():
    processes = list_all_processes()
    print(Config.TOTAL_PROCESSES_FOUND.format(len(processes)))
    for process in processes:
        print(f"PID: {process['pid']}, Name: {process['name']}")
    return

def search_process_by_name_menu():
    name = input("Aramak istediğiniz işlem adını girin: ").strip()
    results = search_process_by_name(name)
    if results:
        print(Config.PROCESS_FOUND_BY_NAME.format(len(results)))
        for process in results:
            print(f"PID: {process['pid']}, Name: {process['name']}")
    else:
        print(Config.PROCESS_NOT_FOUND_BY_NAME.format(name))
    return

def search_process_by_pid_menu():
    pid_input = input("İşlem için PID girin: ").strip()
    try:
        pid = int(pid_input)
        process_handle = open_process(pid)
        print(f"Process {pid} açıldı.")
        close_process(process_handle)
    except ValueError:
        print(Config.INVALID_PID)
    except Exception as e:
        print(f"Process açma hatası: {e}")
    return

def scan_memory_menu():
    pid_input = input("Bellek taraması için işlem PID'sini girin: ").strip()
    try:
        pid = int(pid_input)
        process_handle = open_process(pid)

        search_value = input("Aramak istediğiniz değeri girin: ")
        search_value = int(search_value)
        print(f"Aranan değer: {search_value}")

        # Bellek taraması ve JSON dosyasına kaydetme
        scan_memory(process_handle, search_value)

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
            print(Config.EXIT_PROMPT)
            break
        else:
            print(Config.INVALID_COMMAND)

if __name__ == "__main__":
    main()
