import os
import sys


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller
        
        Keyword Arguments:
        relative_path: relative path to .ico file
        
        :returns string of relative path
        """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Image is 1 directory above current path
        src_path = os.path.dirname(os.path.realpath(__file__))
        base_path = os.path.relpath(os.path.join(src_path, '..'))
    
    return os.path.join(base_path, relative_path)

# END def resource_path() #
