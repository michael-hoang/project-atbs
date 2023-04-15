"""This module provides a class that handles critical files necessary for the Main app to operate correctly."""

import json
import os
import requests
import sys

from assetmanager import AssetManager


class ProgramFileManager:
    """
    This class provides methods to retrieve the paths to the running script or
    executable and download all critical files required for the Main app to
    function correctly.
    """

    def __init__(self):
        """Initialize URL attributes."""

        self.latest_version_url = 'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/dist/latest_version/latest_main_version.json'

    def get_latest_version_number(self) -> str:
        """Return the latest version number for the Main app."""
        try:
            response = requests.get(self.latest_version_url)
            if response.status_code == 200:
                data = json.loads(response.content)
                latest_version = data['main']
                return latest_version
        except:
            return None

    def get_program_path(self) -> str:
        """
        Return the absolute path to the running program. The program can be an
        executable or a script.
        """
        if getattr(sys, 'frozen', False):
            path = os.path.abspath(sys.executable)
        else:
            path = os.path.abspath(__file__)
        return path
    
    



if __name__ == '__main__':
    pfm = ProgramFileManager()
    latest_version = pfm.get_latest_version_number()
    print(latest_version)
    print(pfm.get_program_path())
