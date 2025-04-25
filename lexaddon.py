import os
import re

class LexHandler:
    def __init__(self):
        self.event_handlers = {}
        self.loaded_files = set()  # Track loaded .lex files
        self.file_event_map = {}  # Track which file registered which handlers

    def load_addon(self, filepath):
        """
        Load a .lex addon file and register its event handlers.
        """
        if filepath in self.loaded_files:
            return  # Skip if the file has already been loaded

        self.loaded_files.add(filepath)  # Mark the file as loaded
        self.file_event_map[filepath] = []  # Initialize file-specific handlers

        with open(filepath, 'r') as file:
            content = file.read()

        # Parse the .lex file
        blocks = re.findall(r'when (.+?):\n(.*?)\nend', content, re.DOTALL)
        for event, code in blocks:
            event = event.strip()
            code = code.strip()
            if event not in self.event_handlers:
                self.event_handlers[event] = []
            if code not in self.event_handlers[event]:  # Avoid duplicate code blocks
                self.event_handlers[event].append(code)
                self.file_event_map[filepath].append((event, code))
            self.cleanup()  # Clean up after adding handlers

    def broadcast(self, event_name, run_function):
        """
        Broadcast an event and execute all associated code blocks.
        """
        if event_name in self.event_handlers:
            for code in self.event_handlers[event_name]:
                run_function(code)

    def scan_addons(self, dir, load=True):
        """
        Scan all .lex addon files in a directory. If load is True, load them.
        Otherwise, return a list of .lex files found.
        """
        if not os.path.isdir(dir):
            raise ValueError(f"'{dir}' is not a valid directory.")

        lex_files = [os.path.join(dir, f) for f in os.listdir(dir) if f.endswith('.lex')]

        if load:
            self.clear_all()
            for filepath in lex_files:
                self.load_addon(filepath)
            self.cleanup()
        else:
            return lex_files

    def cleanup(self):
        """
        Remove duplicate entries in the event_handlers dictionary.
        """
        for event, handlers in self.event_handlers.items():
            unique_handlers = list(dict.fromkeys(handlers))
            self.event_handlers[event] = unique_handlers

    def unload_addon(self, filepath):
        """
        Unload an addon and remove its event handlers.
        """
        if not filepath.endswith('.lex'):
            raise ValueError(f"'{filepath}' is not a valid .lex file.")

        if filepath not in self.file_event_map:
            return

        for event, code in self.file_event_map[filepath]:
            if event in self.event_handlers and code in self.event_handlers[event]:
                self.event_handlers[event].remove(code)
                if not self.event_handlers[event]:
                    del self.event_handlers[event]

        del self.file_event_map[filepath]
        self.loaded_files.discard(filepath)

    def clear_all(self):
        """
        Clear all loaded addons and event handlers.
        """
        self.event_handlers.clear()
        self.loaded_files.clear()
        self.file_event_map.clear()