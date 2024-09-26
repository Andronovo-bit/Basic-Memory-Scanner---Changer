class Config:
    """
    Configuration class for storing application messages and constants.
    """
    WELCOME_MESSAGE = "Welcome to the Process Search Tool!"
    LIST_COMMAND_INFO = (
        "To list all processes, type 'list'. "
        "To search by process name, type 'search_name'. "
        "To search by PID, type 'search_pid'."
    )
    EXIT_PROMPT = "Exiting the program."
    INVALID_COMMAND = "Invalid command, please try again."
    TOTAL_PROCESSES_FOUND = "Total {} processes found:\n"
    PROCESS_FOUND_BY_NAME = "{} processes found:"
    PROCESS_NOT_FOUND_BY_NAME = "No processes found with the name '{}'."
    PROCESS_FOUND_BY_PID = "PID: {}, Name: {}"
    PROCESS_NOT_FOUND_BY_PID = "No process found with PID {}."
    ENTER_COMMAND = "Enter a command (type 'exit' to quit): "
    INVALID_PID = "Please enter a valid PID."