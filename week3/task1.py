import csv
import urllib.request
import json
import re

def fetch_data(url):
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())["data"]
    return data

def find_first_image(filelist):
    pattern = r'https?://[^"]+?\.jpe?g'
    match = re.search(pattern, filelist, re.IGNORECASE)
    if match:
        return match.group()
    else:
        return None

def find_district(data, serial_no):
    for item in data:
        if item["SERIAL_NO"] == serial_no:
            return item["address"][5:8:]
    return None

def retrieve_spot(spot_data, mrt_data):
    result = []
    for item in spot_data:
        result.append([
                    item["stitle"],
                    find_district(mrt_data, item["SERIAL_NO"]),
                    item["longitude"],
                    item["latitude"],
                    find_first_image(item["filelist"])
                    ])

    with open("spot.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(result)

def retreive_mrt(mrt_data, spot_data):
    mrt_dict = {}
    for item in mrt_data:
        """如果站名沒在dict上就新增站名與SERIAL_NO。如果站名在dict上就只新增SERIAL_NO"""
        mrt = item['MRT']
        if mrt not in mrt_dict:
            mrt_dict[mrt] = [item['SERIAL_NO']]
        else: mrt_dict[mrt].append(item['SERIAL_NO'])

    result = []
    for key, serial_numbers in mrt_dict.items():
        stitle_list = []
        for serial_number in serial_numbers:
            for item in spot_data:
                if item['SERIAL_NO'] == serial_number:
                    stitle_list.append(item['stitle'])
                    break
        result.append([key] + stitle_list)

    with open("mrt.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(result)

spot_data = fetch_data("https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1")["results"]
mrt_data = fetch_data("https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2")

retrieve_spot(spot_data, mrt_data)
retreive_mrt(mrt_data, spot_data)