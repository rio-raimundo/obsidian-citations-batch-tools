""" File for the ObsidianFile class. """

class ObsidianFile():
    """ Class to store data about a single obsidian file. """

    def __init__(self, filepath: str):
        self.filepath: str = filepath
        self.contents: list[str] = self.contents_list_from_filepath()

        # Properties
        self.property_idxs, self.flat_properties = self.create_flat_properties()
        self.properties = self.create_property_dict_from_flat_properties()
    
    def __iter__(self):
        return iter(self.contents)
    def __getitem__(self, index):
        return self.contents[index]
    def __setitem__(self, index, value):
        self.contents[index] = value

    def contents_list_from_filepath(self) -> list:
        """ Returns the contents of a file as a list."""
        with open(self.filepath, 'r', encoding='utf-8') as file:
            # Remove trailing newline
            return [line.rstrip('\n') for line in file.readlines()]
        
    def create_flat_properties(self) -> list:
        """ Returns idxs for start and end of properties, and list of flat properties. """
        empty = ((), ())
        contents = self.contents
        # Find idxs for first two instances of '---' line to identify properties
        if not contents or not contents[0].startswith("---"): return empty
        for line_idx in range(1, len(contents)):
            if contents[line_idx].startswith("---"): break
        else: 
            return empty  # return empty if no properties
        return (0, line_idx), contents[1: line_idx]
    
    def create_property_dict_from_flat_properties(self) -> dict:
        if not self.property_idxs: return {}  # return empty

        # Create grouped properties from flat property list
        property_dict: dict[str, str | list[str]] = {}
        current_key = ""
        for line in self.flat_properties:
            line: str

            # If 'key' line
            if line.endswith(':') or ': ' in line:
                key, spillover = line.split(':', 1)
                current_key = key.lower()

                if spillover.strip(): property_dict[current_key] = spillover.lstrip()
                else: property_dict[current_key] = None

            # If 'value' line, append it to list if it is one
            else:
                if type(property_dict[current_key]) == str:
                    print(f"Warning: {self.filepath} has multiple values for non-list key {current_key}.")
                    continue
                    
                # Check if set to default null value
                if property_dict.get(current_key) is None:
                    property_dict[current_key] = []
                property_dict[current_key].append(line.lstrip('- '))
        return property_dict
    
    def insert_property(self, prop: str, value, location: int = -1):
        """ Insert a new property into the file. Defaults to the end of the properties. Updates self.properties object. """
        # Check if property already exists inside dictionary
        if prop in self.properties:
            print(f"Warning: '{self.filepath}' already has a property named '{prop}'.")
            return

        # Convert the dictionary to a list, insert the new property, and convert back to a dictionary
        proplist = list(self.properties.items())
        # Note, when using list.insert, -1 is the last element of the list
        proplist.insert(location, (prop, value))
        self.properties = dict(proplist)

    def update_flat_properties_from_properties_dict(self):
        """ Update flat properties class value from properties dictionary. Does not return anything. """
        flat_properties = []

        for property, values in self.properties.items():
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
        if not self.properties: return False
        if self.properties.get(prop) is None: return False

        prop, value = prop.lower(), value.lower()
        if prop not in self.properties: return False
        if value not in self.properties[prop]: return False
        return True
    
    def return_property_values(self, prop: str) -> list:
        """ Returns the values for a given tag. """
        return self.properties[prop.lower()]
    
    def replace_property_value(self, old_value: str, new_value: str):
        # Update flat properties
        for idx, line in enumerate(self.flat_properties):
            if old_value in line:
                line: str
                self.flat_properties[idx] = line.replace(old_value, new_value)
                break

        # Recalculate properties dictionary and update contents
        self.properties = self.create_property_dict_from_flat_properties()
        self.update_properties_in_contents()  # Update contents after recalculating properties
    
    def update_properties_in_contents(self):
        """ Function to update the properties in the contents using flat properties. """
        self.contents[self.property_idxs[0]+1: self.property_idxs[1]] = self.flat_properties

    def write_file(self, copy: bool = False):
        """ Write class contents to file. If copy is True, append '_copy' to the filename. """
        self.update_properties_in_contents()  # update contents before writing
        filepath = self.filepath.replace('.md', '_copy.md') if copy else self.filepath
        with open(filepath, 'w', encoding='utf-8') as file:
            file.writelines('\n'.join(self.contents) + '\n')