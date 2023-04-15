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
        the Main app.
        """
        assets_dir = os.path.join(self.root_path, 'assets')
        form_dir = os.path.join(assets_dir, 'form')
        img_dir = os.path.join(assets_dir, 'img')
        dist_dir = os.path.join(self.root_path, 'dist')
        current_version_dir = os.path.join(dist_dir, 'current_version')
        directories = (
            assets_dir, form_dir, img_dir, dist_dir, current_version_dir
        )
        for directory in directories:
            if not os.path.exists(directory):
                os.mkdir(directory)

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
