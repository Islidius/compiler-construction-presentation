class Error(Exception):
    """base class for all the errors"""
    pass

class ParseError(Error):
    """error for syntax errors"""

    def __str__(self):
        return "the code contains invalid syntax"

class LexerError(Error):
    """error for lexical errors"""

    def __str__(self):
        return "the code contains invalid characters"


class NameNotFoundError(Error):
    """error when a variable is not in the environment"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "The name \"%s\" was not found" % (self.name)

class FileCouldNotBeLoaded(Error):
    """error when load does not find the filename"""
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "The file \"%s\" was not found" % (self.name)