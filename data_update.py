from datetime import datetime, timedelta
import pytz
import os
import csv
from download_data import download_data
from str2datetime import *

def data_update(stock):

    ## check if the data exist
    filename = 'data/'+stock+'.csv'
    file_exists = os.path.isfile(filename)
    ## print(file_exists)

    ## if the file exist, check the time first
    if file_exists:

        # this part check the time
        timezone = pytz.timezone('Asia/Singapore')  # GMT+8
        local_time = datetime.now(timezone)
        # for attempt in range(3):
        #     try:
        #         response = requests.get("http://worldtimeapi.org/api/timezone/Etc/GMT-8", timeout=5)
        #         if response.status_code == 200:
        #             data_time = response.json()
        #             local_time = data_time["datetime"]
        #     except requests.exceptions.RequestException as e:
        #         print(f"Attempt {attempt + 1} failed")
        #         time.sleep(3)  # Wait before retrying

        # this part obtain date in tickername data
        with open('data/tickername.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        ## get the last_update time
        # Assume the first row is the header
        csv_data_rows = rows[1:]
        
        # Check for a row with matching first column
        for i, row in enumerate(csv_data_rows):
            # Ensure the row has at least first columns before comparing, and also check if its match
            if len(row) >= 1 and row[0] == stock:
                # If the row has a third column, take it
                if len(row) >= 3:
                    latest_time = row[2]
                    row_id = i
                break

        latest_time = str2datetime(latest_time)
        
        # print("Local date:", local_time)
        # print("Lastest date:", latest_time)

        difference = local_time - latest_time
        # print(difference)
        # print("Difference:", difference_days)
        target = timedelta(days=1)

        # print("Time in GMT+8:", local_date)
        if (difference >= target): # used to be have hour based filter here
            print('download data now')
            download_data(stock)
        else: # else, just update last_update data
            print('no download data')
            t_row = rows[row_id+1] #+1 since we have header
            t_row[2] = local_time # update last update
            rows[row_id+1] = t_row #update entire row

            # Write the updated rows back to the CSV file
            with open('data/tickername.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

        # # pass
        
    ## if the file does not exist, download it immediately
    else: 
        download_data(stock)