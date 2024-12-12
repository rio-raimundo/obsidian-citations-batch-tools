""" File for the ObsidianNote class. """
import logging

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
        """
        Initialize an ObsidianNote object with the contents of a file.

        Args:
            filepath (str): The path to the file to be loaded.

        Attributes:
            filepath (str): Path to the file associated with this object.
            flat_properties (list[str]): List to store flat properties of the file.
            properties_dict (dict[str, str | list[str]]): Dictionary to store properties in key-value form.
            body_text (list[str]): List of strings representing the body text of the file.

        The method reads the file from the given filepath, splits its contents into
        properties and body text, and initializes the corresponding attributes.
        """

        self._flat_properties: list[str] = []
        self._properties_dict: dict[str, str | list[str]] = {}

        # Access file and store full contents as a list of strings
        self.filepath: str = filepath
        file_contents: list[str] = self._contents_list_from_filepath(filepath)

        # Split contents into properties and body text
        # Note that assigning to self.flat_properties will also update self.properties_dict
        self.flat_properties, self.body_text = self._split_file_contents(file_contents)


    """ USER FUNCTIONS. """    
    def insert_property_at_location(self, property: str, value, location: int = -1):
        """
        Insert a new property into the file. Defaults to the end of the properties. Updates self.properties object.

        Args:
            property (str): Name of the new property.
            value (str | list[str]): Value of the new property. Can be a string or a list of strings.
            location (int, optional): Location in the properties list to insert the new property. Defaults to -1, which is the last element of the list.

        Raises:
            logging.warning: If the property already exists inside dictionary.
        """
        # Check if property already exists inside dictionary, warn and return if so.
        if property in self.properties_dict:
            logging.warning(f"Warning: '{self.filepath}' already has a property named '{property}'.")
            return

        # Convert the dictionary to a list, insert the new property, and convert back to a dictionary
        temp_properties_list = list(self.properties_dict.items())
        temp_properties_list.insert(location, (property, value)) # note when using list.insert, -1 is the last element of the list
        self.properties_dict = dict(temp_properties_list)  # will also update flat properties

    def property_contains_value(self, property: str, value: str) -> bool:
        """
        Identify if a given value is associated with a given property.

        Args:
            property (str): The name of the property to check.
            value (str): The value to check for.

        Returns:
            bool: True if the value is associated with the property, False otherwise.

        Notes:
            - The search is case-insensitive.
            - Returns false if the property does not exist or if the value does not exist for the property.
        """
        if not self.properties_dict: return False
        if self.properties_dict.get(property) is None: return False

        property, value = property.lower(), value.lower()
        if property not in self.properties_dict: return False
        if value not in self.properties_dict[property]: return False
        return True
    
    def reorder_properties_from_list(self, ordered_property_labels: list[str]) -> None:
        """
        Reorders the properties of an Obsidian article in a specified order.

        Args:
            ordered_property_labels (list[str]): An ordered list of property labels.
                - All property labels not in this list will be moved to the end of the properties list, though remain in their order relative to one another.
                - Ordered property labels can contain properties not currently in the file, which will be ignored.

        Returns:
            None
        """
        # Generate dictionaries of ordered properties (listed in ordered_property_labels) and unlisted properties (in their original order)
        ordered_properties = {label: self.properties_dict[label] for label in ordered_property_labels if label in self.properties_dict.keys()}
        unlisted_properties = {label: values for label, values in self.properties_dict.items() if label not in ordered_property_labels}

        # Assign to properties_dict
        self.properties_dict = ordered_properties | unlisted_properties  # self.flat_properties will also be updated

    def write_file(self, copy: bool = False):
        """ Write class contents to file. If copy is True, append '_copy' to the filename. """
        filepath = self.filepath.replace('.md', '_copy.md') if copy else self.filepath
        with open(filepath, 'w', encoding='utf-8') as file:
            file.writelines(self.file_contents_string)


    """ INTERNAL FUNCTIONS AND PROPERTIES. """
    # Define file_contents getter which will return the properties and body text as a single list
    @property
    def file_contents_list(self) -> list[str]: return ['---'] + self.flat_properties + ['---'] + self.body_text
    @property
    def file_contents_string(self) -> str: return ('\n'.join(self.file_contents_list) + '\n')

    # Define setters and getters for flat_properties and properties_dict which will update each other when set
    @property
    def flat_properties(self) -> list[str]: return self._flat_properties
    @flat_properties.setter
    def flat_properties(self, v: list[str]):
        self._flat_properties = v
        self._properties_dict = self._properties_dict_from_flat(v)

    @property
    def properties_dict(self) -> dict[str, str | list[str]]: return self._properties_dict
    @properties_dict.setter
    def properties_dict(self, v: dict[str, str | list[str]]):
        self._properties_dict = v
        self._flat_properties = self._flat_properties_from_dict(v)

    # Define internal methods, mostly related to the processing of the file properties
    def _contents_list_from_filepath(self, filepath: str) -> list:
        """
        Read and return the contents of a file as a list of strings.

        Args:
            filepath (str, optional): The path to the file to be read.

        Returns:
            list: A list of strings representing the lines of the file, with trailing newline characters removed.

        Raises:
            FileNotFoundError: If the file specified by filepath does not exist.
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            return [line.rstrip('\n') for line in file.readlines()]

    def _split_file_contents(self, file_contents: list[str]) -> tuple[list, list]:
        """
        Splits the contents of the file into a list of 'flat' properties and a list of body text.

        Args:
            file_contents (list[str]): The contents of the file as a list of strings.

        Returns:
            tuple[list, list]: A tuple containing two lists. The first list contains the 'flat' properties
                and the second list contains the body text.
        """
        default = ([], [])  # default return value
        if not file_contents or not file_contents[0].startswith("---"): return default

        # Find indexes for first two instances of '---' line to identify properties
        for line_idx, line in enumerate(file_contents):
            if line_idx == 0: continue
            if line.startswith("---"): break
        else: 
            return default  # return default if properties are not found (no closing '---' line)
        
        # If properties found, return the properties and body text (excluding '---' lines)
        return file_contents[1: line_idx], file_contents[line_idx+1:]
    
    def _properties_dict_from_flat(self, flat_properties: list[str]) -> dict[str, str | list[str]]:
        # Initialise properties dictionary
        """ Converts a list of 'flat' properties into a dictionary of properties.

        Args:
            flat_properties (list[str], optional): The list of flat properties to convert.

        Returns:
            dict[str, str | list[str]]: A dictionary of properties, where each key is a property label and each value is either a single string (if the property has a single value) or a list of strings (if the property has multiple values).
        """
        properties_dict: dict[str, str | list[str]] = {}

        # Iterate through each line in the flat properties and assign to dictionary
        # There are two main types of properties: 'string' properties (for single values) and 'list' properties (for multiple values)
        for line in flat_properties:
            line: str

            # If the line contains a property label...
            if line.endswith(':') or ': ' in line:
                propery_label, text_overflow = line.split(':', 1)
                current_property_label = propery_label.lower()  # note that all labels are stored (and assigned) in lowercase

                # If overflow has non-whitespace characters, assign it as the value of the current property
                # Otherwise, assume it is an empty property and assign None
                if text_overflow.strip(): properties_dict[current_property_label] = text_overflow.lstrip()
                else: properties_dict[current_property_label] = None

            # If the line does not contain a property label, assume it is a value for the current property
            else:
                # If another value is given for a 'string' property, log a warning and skip
                if type(properties_dict[current_property_label]) == str:
                    logging.warning(f"Warning: {self.filepath} has multiple values for non-list property {current_property_label}... skipping.")
                    continue
                    
                # Otherwise, append the value to the list of values for the current property
                # If this is the first value being appended, the property should be converted to a list
                if properties_dict[current_property_label] is None: properties_dict[current_property_label] = []
                properties_dict[current_property_label].append(line.lstrip('- '))

        return properties_dict

    def _flat_properties_from_dict(self, properties_dict: dict[str, str | list[str]]) -> list[str]:
        """Converts a properties dictionary to a list of 'flat' properties.

        Args:
            properties_dict (dict[str, str | list[str]]): The dictionary of properties to convert.

        Returns:
            list[str]: A list of 'flat' properties where each property is represented as a string.
        """
        flat_properties = []
        
        # Iterate through each property in the dictionary and append to the flat properties list
        for property, values in properties_dict.items():
            property: str

            # If the property has no values, assume it is an empty property
            if values is None:
                flat_properties.append(f"{property}: ")

            # If the property has a single value, append on same line as a string
            elif type(values) == str:
                flat_properties.append(f"{property}: {values}")

            # If the property has multiple values, append each value on a new line with a preceding indented dash
            else:
                flat_properties.append(f"{property}:")
                for value in values:  flat_properties.append(f"  - {value}")
        
        return flat_properties