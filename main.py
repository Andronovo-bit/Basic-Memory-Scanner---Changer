from src.process.process_list import list_all_processes
from src.process.process_search import search_process_by_name
from src.memory.memory_reader import open_process, read_memory, close_process
from src.config.config import Config

def main():
    print(Config.WELCOME_MESSAGE)
    print(Config.LIST_COMMAND_INFO + "\n")

    while True:
        user_input = input(Config.ENTER_COMMAND).strip()

        if user_input == "list":
            processes = list_all_processes()
            print(Config.TOTAL_PROCESSES_FOUND.format(len(processes)))
            for process in processes:
                print(f"PID: {process['pid']}, Name: {process['name']}")
        
        elif user_input.startswith("search_name"):
            _, name = user_input.split(" ", 1)
            results = search_process_by_name(name)
            if results:
                print(Config.PROCESS_FOUND_BY_NAME.format(len(results)))
                for process in results:
                    print(f"PID: {process['pid']}, Name: {process['name']}")

                # Kullanıcıdan seçilecek process'in PID'ini iste
                pid_input = input("İşlem için PID girin: ").strip()
                try:
                    pid = int(pid_input)
                    process_handle = open_process(pid)
                    
                    # RAM adresi girişi iste
                    address = input("Bellek adresini girin (hex formatında): ")
                    address = int(address, 16)

                    # Belleği oku (örneğin 8 byte)
                    size = 8
                    memory_value = read_memory(process_handle, address, size)

                    print(f"Adres {hex(address)} üzerindeki bellek değeri: {memory_value}")
                    close_process(process_handle)
                except ValueError:
                    print(Config.INVALID_PID)
                except Exception as e:
                    print(f"Bellek okuma hatası: {e}")
            else:
                print(Config.PROCESS_NOT_FOUND_BY_NAME.format(name))
        
        elif user_input == "exit":
            print(Config.EXIT_PROMPT)
            break

        else:
            print(Config.INVALID_COMMAND)

if __name__ == "__main__":
    main()
