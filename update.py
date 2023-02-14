import tkinter as tk
import requests
import subprocess
import sys
import os


# Github repo info
github_user = 'michael-hoang'
github_repo = 'project-atbs-work'
current_version = '4.5'

# Github API URL for repo's releases
api_url = f'https://api.github.com/repos/{github_user}/{github_repo}/releases/latest'

# GET request to API URL
response = requests.get(api_url)

# Parse JSON response
data = response.json()

# Get latest release version from response
latest_version = data['tag_name']

# Compare current version with latest version
if latest_version != current_version:
    print('An update is available!')
    print(f'Current version: {current_version}')
    print(f'Latest version: {latest_version}')
else:
    print('You have the latest version.')


# Run main.exe once update completes
if getattr(sys, 'frozen', False):
    update_path = os.path.dirname(sys.executable)
else:
    update_path = os.path.dirname(os.path.abspath(__file__))

exe_path = f'{update_path}\main.exe'
p = subprocess.Popen(exe_path)
p.wait()
print('The exe file has finished executing.')
