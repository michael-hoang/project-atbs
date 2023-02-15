import requests
import subprocess
import sys
import os
import urllib.request
import tkinter as tk
from tkinter import ttk
import time


# # Github repo info
# github_user = 'michael-hoang'
# github_repo = 'project-atbs-work'
# current_version = '4.5'

# # Github API URL for repo's releases
# api_url = f'https://api.github.com/repos/{github_user}/{github_repo}/releases/latest'

# # GET request to API URL
# response = requests.get(api_url)

# # Parse JSON response
# data = response.json()

# # Get latest release version from response
# latest_version = data['tag_name']

# # Compare current version with latest version
# if latest_version != current_version:
#     print('An update is available!')
#     print(f'Current version: {current_version}')
#     print(f'Latest version: {latest_version}')
# else:
#     print('You have the latest version.')

# Download latest files
if getattr(sys, 'frozen', False):
    update_path = os.path.dirname(sys.executable)
else:
    update_path = os.path.dirname(os.path.abspath(__file__))

exe_path = f'{update_path}\main.exe'
url = 'https://github.com/michael-hoang/project-atbs-work/raw/main/dist/main.exe'
# urllib.request.urlretrieve(url, exe_path)

# Download progress bar
window = tk.Tk()
window.title('Download Progress')
progress_bar = ttk.Progressbar(window, orient='horizontal', length=300, mode='determinate')
progress_bar.pack(padx=5, pady=5, fill=tk.X)
response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))
block_size = 1024
progress = 0

with open(exe_path, 'wb') as f:
    for data in response.iter_content(block_size):
        progress += len(data)
        progress_bar['value'] = progress / total_size * 100
        window.update_idletasks()
        # time.sleep(0.1)
        f.write(data)
        
        

# progress_bar['value'] = 0


# Run main.exe once update completes
p = subprocess.Popen(exe_path)
p.wait()
print('The exe file has finished executing.')

window.mainloop()
