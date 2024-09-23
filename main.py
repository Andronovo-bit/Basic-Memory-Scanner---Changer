from src.process.process_list import list_all_processes
from src.process.process_search import search_process_by_name, search_process_by_pid
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
            else:
                print(Config.PROCESS_NOT_FOUND_BY_NAME.format(name))
        
        elif user_input.startswith("search_pid"):
            try:
                _, pid = user_input.split(" ", 1)
                pid = int(pid)
                results = search_process_by_pid(pid)
                if results:
                    print(Config.PROCESS_FOUND_BY_PID.format(results[0]['pid'], results[0]['name']))
                else:
                    print(Config.PROCESS_NOT_FOUND_BY_PID.format(pid))
            except ValueError:
                print(Config.INVALID_PID)
        
        elif user_input == "exit":
            print(Config.EXIT_PROMPT)
            break

        else:
            print(Config.INVALID_COMMAND)

if __name__ == "__main__":
    main()
