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

    def get_program_path(self):
        """
        Create an attribute for the absolute path to the running program (root 
        path). The program can be an executable or a script.
        """
        if getattr(sys, 'frozen', False):
            path = os.path.abspath(sys.executable)
        else:
            path = os.path.abspath(__file__)
        self.root_path = path

    def create_required_directories(self):
        """
        Create all the necessary directories that contain essential files for
        the Main app. The paths are stored in a Python dictionary as an attribute.
        """
        directories = {
            'assets': os.path.join(self.root_path, 'assets'),
            'form': os.path.join(self.root_path, 'assets', 'form'),
            'img': os.path.join(self.root_path, 'assets', 'img'),
            'dist': os.path.join(self.root_path, 'dist'),
            'current_version': os.path.join(self.root_path, 'dist', 'current_version')
        }
        for directory in directories.values():
            if not os.path.exists(directory):
                os.mkdir(directory)

        self.directories = directories

    def create_current_version_json(self, current_version_number: str):
        """Create current_main_version.json file if it doesn't exist."""
        json_path = os.path.join(
            self.directories['current_version'], 'current_main_version.json'
        )
        if not os.path.exists(json_path):
            with open(json_path, 'w') as f:
                json.dump({'main': current_version_number}, f, indent=4)

    def download_essential_files(self):
        """
        Download all essential files required for the Main app to run properly.
        Instantiates an object called AssetManager to look for required files.
        """
        am = AssetManager()
        self.get_program_path()
        self.create_required_directories()


if __name__ == '__main__':
    pfm = ProgramFileManager()
    latest_version = pfm.get_latest_version_number()
    print(latest_version)
    print(pfm.get_program_path())
