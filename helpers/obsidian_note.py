""" File for the ObsidianNote class. """

class ObsidianNote():
    """
    Class to store data about a single obsidian file.
    Functions beginning with an underscore are intended for internal use only.
    
    Properties:
        - The class is largely used to store data about the 'properties' section of an Obsidian file, a YAML-like section at the top of the file separated by triple dashes ('---').
        - Properties are stored both in 'flat' form (as a list of strings), which can be written directly to a the Obsidian document, and in 'dictionary' form, which can be accessed and modified more easily. Getters and setters are used to make sure that both representations are consistent with one another, allowing either to be changed and updated.
    
    Body text:
        - The body text of the file (everything following the properties) is stored as a list of strings, and can be accessed and modified directly.
    """

    def __init__(self, filepath: str):
        self._flat_properties: list[str] = []
        self._properties_dict: dict[str, str | list[str]] = {}

        # Access file and store full contents as a list of strings
        self.filepath: str = filepath
        file_contents: list[str] = self.contents_list_from_filepath(filepath)

        # Split contents into properties and body text
        # Note that assigning to self.flat_properties will also update self.properties_dict
        self.flat_properties, self.body_text = self._split_file_contents(file_contents)
    
    # Define setters and getters for flat_properties and properties_dict which will update each other when set
    @property
    def flat_properties(self) -> list[str]: return self._flat_properties
    @flat_properties.setter
    def flat_properties(self, value: list[str]):
        self._flat_properties = value
        self._properties_dict = self._properties_dict_from_flat()

    @property
    def properties_dict(self) -> dict[str, str | list[str]]: return self._properties_dict
    @properties_dict.setter
    def properties_dict(self, value: dict[str, str | list[str]]):
        self._properties_dict = value
        self._flat_properties = self.flat_properties_from_dict()

    def _split_file_contents(self, file_contents: list[str]) -> list:
        """ Splits the contents of the file into a list of 'flat' properties and a list of body text. """
        default = ([], [])  # default return value
        if not file_contents or not file_contents[0].startswith("---"): return default

        # Find indexes for first two instances of '---' line to identify properties
        for line_idx, line in enumerate(file_contents):
            if line.startswith("---"): break
        else: 
            return default  # return default if properties are not found (no closing '---' line)
        
        # If properties found, return the properties and body text (excluding '---' lines)
        return file_contents[1: line_idx], file_contents[line_idx+1:]
    
    def _properties_dict_from_flat(self, flat_properties: list[str] = None) -> dict:
        # Initialise properties dictionary
        properties_dict: dict[str, str | list[str]] = {}

        # Iterate through each line in the flat properties and assign to dictionary
        for line in flat_properties:
            line: str

            # If the line contains a property label...
            if line.endswith(':') or ': ' in line:
                propery_label, text_overflow = line.split(':', 1)
                current_property_label = propery_label.lower()  # note that all labels are stored (and assigned) in lowercase

                # If overflow has non-whitespace characters, assign it as the value of the current property
                if text_overflow.strip(): properties_dict[current_property_label] = text_overflow.lstrip()
                else: properties_dict[current_property_label] = None

            # If 'value' line, append it to list if it is one
            else:
                if type(properties_dict[current_property_label]) == str:
                    print(f"Warning: {self.filepath} has multiple values for non-list key {current_property_label}.")
                    continue
                    
                # Check if set to default null value
                if properties_dict.get(current_property_label) is None:
                    properties_dict[current_property_label] = []
                properties_dict[current_property_label].append(line.lstrip('- '))
        return properties_dict
    
    def insert_property(self, prop: str, value, location: int = -1):
        """ Insert a new property into the file. Defaults to the end of the properties. Updates self.properties object. """
        # Check if property already exists inside dictionary
        if prop in self.properties_dict:
            print(f"Warning: '{self.filepath}' already has a property named '{prop}'.")
            return

        # Convert the dictionary to a list, insert the new property, and convert back to a dictionary
        proplist = list(self.properties_dict.items())
        # Note, when using list.insert, -1 is the last element of the list
        proplist.insert(location, (prop, value))
        self.properties_dict = dict(proplist)

    def flat_properties_from_dict(self):
        """ Update flat properties class value from properties dictionary. Does not return anything. """
        flat_properties = []

        for property, values in self.properties_dict.items():
            if values is None:
                flat_properties.append(f"{property}: ")
            elif type(values) == str:
                flat_properties.append(f"{property}: {values}")
            else:
                flat_properties.append(f"{property}:")
                for value in values: flat_properties.append(f"  - {value}")
        self.flat_properties = flat_properties
    
    def make_properties_lowercase(self):
        if not self.property_idxs: return

        for idx, line in enumerate(self.flat_properties):
            line: str

            if line.endswith(':') or ': ' in line:
                key, _ = line.split(':', 1)

                # Make all property names in modified files lowercase.
                self.flat_properties[idx] = line.replace(key, key.lower())

    def property_contains_value(self, prop: str, value: str) -> bool:
        """ Identify if a given value is associated with a given value. """
        if not self.properties_dict: return False
        if self.properties_dict.get(prop) is None: return False

        prop, value = prop.lower(), value.lower()
        if prop not in self.properties_dict: return False
        if value not in self.properties_dict[prop]: return False
        return True
    
    def return_property_values(self, prop: str) -> list:
        """ Returns the values for a given tag. """
        return self.properties_dict[prop.lower()]
    
    def replace_property_value(self, old_value: str, new_value: str):
        # Update flat properties
        for idx, line in enumerate(self.flat_properties):
            if old_value in line:
                line: str
                self.flat_properties[idx] = line.replace(old_value, new_value)
                break

        # Recalculate properties dictionary and update contents
        self.properties_dict = self._properties_dict_from_flat()
        self.update_properties_in_contents()  # Update contents after recalculating properties
    
    def update_properties_in_contents(self):
        """ Function to update the properties in the contents using flat properties. """
        self.contents[self.property_idxs[0]+1: self.property_idxs[1]] = self.flat_properties
    
    def __iter__(self):
        return iter(self.contents)
    def __getitem__(self, index):
        return self.contents[index]
    def __setitem__(self, index, value):
        self.contents[index] = value

    def contents_list_from_filepath(self, filepath: str = None) -> list:
        """ Returns the contents of a file as a list."""
        with open(filepath, 'r', encoding='utf-8') as file:
            # Remove trailing newline
            return [line.rstrip('\n') for line in file.readlines()]

    def write_file(self, copy: bool = False):
        """ Write class contents to file. If copy is True, append '_copy' to the filename. """
        self.update_properties_in_contents()  # update contents before writing
        filepath = self.filepath.replace('.md', '_copy.md') if copy else self.filepath
        with open(filepath, 'w', encoding='utf-8') as file:
            file.writelines('\n'.join(self.contents) + '\n')