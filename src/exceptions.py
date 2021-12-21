class ToolException(Exception):
    pass

class ToolNotComplete(ToolException):
    def __init__(self, tool_name: str, functionality: str='', message='Tool has not implemented essential functionalities'):
        super().__init__(message)
        self.message = message
        self.functionality = functionality
        self.tool_name = tool_name

    def __str__(self):
        if self.functionality:
            return f'Tool {self.tool_name} has not implemented {self.functionality}'
        else:
            return f'Tool {self.tool_name} has not implemented essential functionalities'
