import datetime
import os
import time

DAYS_UNTIL_EXPIRATION = 7
SECONDS_PER_DAY = 86400
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60

FILES_PATH = '.files/'


epoch_current_time = time.time()

# Iterate through .files directory and get metadata
for file in os.listdir(FILES_PATH):
    file_path = os.path.join(FILES_PATH, file)
    epoch_creation_time = os.path.getctime(file_path)

    epoch_exp_time = epoch_creation_time + (
        DAYS_UNTIL_EXPIRATION * SECONDS_PER_DAY
    )
    remaining_epoch_time = epoch_exp_time - epoch_current_time
    remaining_days = int(remaining_epoch_time // SECONDS_PER_DAY)
    remaining_epoch_sec = remaining_epoch_time % SECONDS_PER_DAY
    remaining_hours = int(remaining_epoch_sec // SECONDS_PER_HOUR)
    remaining_epoch_sec %= SECONDS_PER_HOUR
    remaining_minutes = int(remaining_epoch_sec // SECONDS_PER_MINUTE)

    print(f'{remaining_days}d')
    print(f'{remaining_hours}h')
    print(f'{remaining_minutes}m')
