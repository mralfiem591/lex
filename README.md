# Lex Addon System

> The addon manager of all time.

The **Lex Addon System** is a Python-based framework that allows developers to create and manage addons for their applications. Addons are stored in `.lex` files and can define event-based code blocks that are executed when specific events are broadcasted by the main application.

---

## Features

- **Event-Based Addons**: Addons define `when` blocks that execute code when specific events are triggered.
- **Dynamic Addon Loading**: Load `.lex` files dynamically at runtime.
- **Duplicate Prevention**: Automatically removes duplicate event handlers.
- **Addon Management**: Includes functions to unload specific addons and clear all loaded addons.
- **Easy Integration**: Simple API for broadcasting events and managing addons.

---

## Installation

Clone the repository or copy the `lexaddon.py` file into your project directory.

```bash
git clone https://github.com/mralfiem591/lex.git
```

Ensure your project structure includes the following:

```plaintext
project/
│
├── lexaddon.py
├── main.py
└── addons/
    └── example.lex
```

---

## Usage

### 1. Import the LexHandler

Import the `LexHandler` class from `lexaddon.py` into your main application.

```python
from lexaddon import LexHandler
```

### 2. Define a `run_function`

Define a `run_function` in your main application to execute code from addons.
Copy-paste the following function into your code that is using Lex:

```python
def run_function(code):
    exec(code)
```

This code should not be in any class, as the Lex system is not adjusted for classes. If it is in a class, you will get a NameError.

### 3. Load Addons

Use the `scan_addons` method to load all `.lex` files from a directory.

```python
lex = LexHandler()
lex.scan_addons("addons", load=True)
```

### 4. Broadcast Events

Broadcast events to execute the corresponding code blocks in the loaded addons.

```python
lex.broadcast("on_start", run_function)
```

---

## Lex File Format

`.lex` files define event-based code blocks using the following structure:

```code
when {event_name}:
# Code to execute when the event is broadcasted
end
```

> Note: Despite `.py` using indents, `when` and `end` should not be indented. Any python code between these blocks uses normal python indenting.

### Example `.lex` File

```code
when on_start:
greet()
print("Welcome to the Lex Addon System!")
end

when on_test:
for i in range(3):
    print(f"Test{i}")
end
```

---

## API Reference

### `class LexHandler`

The main class for managing addons and broadcasting events.

#### Methods

1. **`load_addon(filepath)`**
   - Loads a single `.lex` file and registers its event handlers.
   - **Parameters**:
     - `filepath` (str): Path to the `.lex` file.

2. **`broadcast(event_name, run_function)`**
   - Broadcasts an event and executes all associated code blocks.
   - **Parameters**:
     - `event_name` (str): The name of the event to broadcast.
     - `run_function` (function): A function to execute the code blocks.

3. **`scan_addons(dir, load=True)`**
   - Scans a directory for `.lex` files and optionally loads them.
   - **Parameters**:
     - `dir` (str): Path to the directory containing `.lex` files.
     - `load` (bool): Whether to load the addons or just return the list of files.

4. **`cleanup()`**
   - Removes duplicate event handlers from the system.

5. **`unload_addon(filepath)`**
   - Unloads a specific `.lex` file and removes its event handlers.
   - **Parameters**:
     - `filepath` (str): Path to the `.lex` file to unload.

6. **`clear_all()`**
   - Clears all loaded addons and event handlers.

---

## Examples

### Example 1: Basic Usage

```python
from lexaddon import LexHandler

def run_function(code):
    exec(code)

def greet():
    print("Hello from the main script!")

lex = LexHandler()
lex.scan_addons("addons", load=True)

lex.broadcast("on_start", run_function)

### Example 2: Unloading an Addon

lex.unload_addon("addons/example.lex")

### Example 3: Clearing All Addons

lex.clear_all()
print("All addons have been cleared.")
```
---

## Debugging

### The Lex handler is not linked to my code, or I get an ImportError:
#### Your file is **NOT** named `main.py`:
Lex expects your code file to be named `main.py`. Open the Lex handler script, and change the import to your script name.

#### Your file **IS** named `main.py`:
Check for errors with your code, and ensure the lex handler is in the same dir as your file.
If you cannot find why the error is happening, open a **GitHub Issue**.

---

## Contributing

Contributions are welcome! If you have ideas for new features or improvements, feel free to open an issue or submit a pull request.

---

## License

Refer to the [LICENSE](LICENSE) file for licensing information.
