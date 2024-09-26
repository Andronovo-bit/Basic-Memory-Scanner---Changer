# Memory Analyzer

Memory Analyzer is a Python-based tool for analyzing and manipulating the memory of running processes on a Windows system. It allows you to list processes, search for processes by name or PID, scan memory for specific values, write values to memory, and check for changes in memory values.

## Features

- List all running processes
- Search for processes by name or PID
- Scan memory for specific values
- Write values to specific memory addresses
- Check for changes in memory values

## Project Structure

```
.gitignore
main.py
src/
    config/
        config.py
    memory/
        memory_reader.py
        memory_scanner.py
        memory_writer.py
    process/
        process_list.py
        process_search.py
```

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/memory_analyzer.git
    cd memory_analyzer
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the main script to start the Memory Analyzer:
```sh
python main.py
```

### Main Menu Options

1. **List Processes**: Lists all running processes.
2. **Search Process by Name**: Searches for processes by name.
3. **Search Process by PID**: Searches for a process by PID.
4. **Scan Memory**: Scans the memory of a process for a specific value.
5. **Write Memory**: Writes a value to a specific memory address of a process.
6. **Check for Memory Changes**: Checks for changes in memory values of a process.
7. **Exit**: Exits the Memory Analyzer.

### Example Usage

1. **List Processes**:
    - Select option [`1`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fe%3A%2FProjects%2FPython%2Fmemory_analyzer%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A9%2C%22character%22%3A11%7D%7D%5D%2C%2266ab22f5-0029-4c68-ba8b-ec2b26cc2e5e%22%5D "Go to definition") to list all running processes.

2. **Search Process by Name**:
    - Select option [`2`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fe%3A%2FProjects%2FPython%2Fmemory_analyzer%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A10%2C%22character%22%3A11%7D%7D%5D%2C%2266ab22f5-0029-4c68-ba8b-ec2b26cc2e5e%22%5D "Go to definition") and enter the process name to search for.

3. **Search Process by PID**:
    - Select option [`3`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fe%3A%2FProjects%2FPython%2Fmemory_analyzer%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A11%2C%22character%22%3A11%7D%7D%5D%2C%2266ab22f5-0029-4c68-ba8b-ec2b26cc2e5e%22%5D "Go to definition") and enter the PID of the process to search for.

4. **Scan Memory**:
    - Select option [`4`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fe%3A%2FProjects%2FPython%2Fmemory_analyzer%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A12%2C%22character%22%3A11%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fe%3A%2FProjects%2FPython%2Fmemory_analyzer%2Fsrc%2Fmemory%2Fmemory_scanner.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A76%2C%22character%22%3A64%7D%7D%5D%2C%2266ab22f5-0029-4c68-ba8b-ec2b26cc2e5e%22%5D "Go to definition"), enter the PID of the process to scan, and enter the value to search for.

5. **Write Memory**:
    - Select option [`5`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fe%3A%2FProjects%2FPython%2Fmemory_analyzer%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A13%2C%22character%22%3A11%7D%7D%5D%2C%2266ab22f5-0029-4c68-ba8b-ec2b26cc2e5e%22%5D "Go to definition"), enter the PID of the process, the memory address (in hex format), and the new value to write.

6. **Check for Memory Changes**:
    - Select option [`6`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fe%3A%2FProjects%2FPython%2Fmemory_analyzer%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A14%2C%22character%22%3A11%7D%7D%5D%2C%2266ab22f5-0029-4c68-ba8b-ec2b26cc2e5e%22%5D "Go to definition") and enter the PID of the process to check for memory changes.

## Configuration

The configuration settings are located in [`src/config/config.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fe%3A%2FProjects%2FPython%2Fmemory_analyzer%2Fsrc%2Fconfig%2Fconfig.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%2266ab22f5-0029-4c68-ba8b-ec2b26cc2e5e%22%5D "e:\Projects\Python\memory_analyzer\src\config\config.py"). You can modify the configuration settings as needed.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [psutil](https://github.com/giampaolo/psutil) - A cross-platform library for retrieving information on running processes and system utilization.
- [ctypes](https://docs.python.org/3/library/ctypes.html) - A foreign function library for Python.