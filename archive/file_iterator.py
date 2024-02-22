class FileIterator():
    """
    Iterate through file and make list of lines with start and stop criteria.

    Args:
        start (str): The start criteria for iterating through the file.
        stop (str): The stop criteria for iterating through the file.
        iter_once (bool): Whether to iterate through the file only once.
        ignore (int): Number of lines to ignore before starting the iteration.

    Attributes:
        start (str): The start criteria for iterating through the file.
        stop (str): The stop criteria for iterating through the file.
        iter_once (bool): Whether to iterate through the file only once.
        ignore (int): Number of lines to ignore before starting the iteration.
        text (list): List of lines that meet the start and stop criteria.
        is_started (bool): Flag to indicate if the iteration has started.
        n_stops (int): Number of times the iteration has stopped.

    Methods:
        feed(self, line: str) -> bool: Takes in a line according to start/stop conditions. If it meets the stopping criteria on this line, returns True.
    """

    def __init__(self, start: str = "", stop: str = "", ignore: int = 0, include_first: bool = True):
        self.start = start
        self.stop = stop
        self.ignore = ignore
        self.include_first = include_first

        self.text = []
        self.is_started = False
    
    def feed_all(self, content: list[str]):
        """ Iterative function to feed all content at once. """
        for line in content:
            self.feed(line)
        return self.text

    def feed(self, line: str) -> bool:
        """
        Takes in a line according to start / stop conditions. If has met stopping criteria on this line, returns True.
        
        Args:
            line (str): The line to be processed.

        Returns:
            bool: True if the line meets the stopping criteria, otherwise False.
        """
        just_started, just_stopped = False, False

        if self.is_started == False and (not self.start or self.start in line):
            # If set to ignore, skip this line
            if self.ignore > 0:
                self.ignore -= 1
                return
            # Don't feed more than once if set
            self.is_started = True  # start feeding
            just_started = True
        elif self.stop and self.stop in line:
            self.is_started = False
            just_stopped = True

        if self.is_started and (self.include_first or not just_started):
            self.text.append(line)
        return just_stopped
