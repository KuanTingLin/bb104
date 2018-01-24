

import RPi.GPIO as GPIO
import time
import spidev
import csv
from datetime import datetime
from pymongo import MongoClient
import json

spi = spidev.SpiDev()
spi.open(0, 0)

def ReadChannel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

data_channel = 0
threshold = 100
def main():
    print("heart is beating")
    # client link into mongo
    # client = MongoClient('10.120.37.23', 27017)
    # db = client['raspberry-data']

    # input data as a csv file
    csvfile = csv.writer(open('./heart.csv', 'w'))
    csvfile.writerow(['Timestamp_RPI', 'heart_beat'])
    try:
        while True:
            csvfile.writerow([datetime.now().isoformat(), ReadChannel(data_channel)])
            HB = {"time":datetime.now().isoformat(),"beats":ReadChannel(data_channel)}
            # db.HeartBeat.insert_one(HB)
            with open('.\HeartBeat_Data', 'w', encoding="utf-8") as f:
                f.write(json.dumps(HB, ensure_ascii=False, indent=4))
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exception: KeyboardInterrupt")

    finally:
        GPIO.cleanup()
        # clear

# call main
if __name__ == '__main__':
   main()