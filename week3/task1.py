import csv
import json
import urllib.request
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

def put_district_and_mrt_into_spots(spots, mrts):
    mrt_dict = {mrt["SERIAL_NO"]: mrt for mrt in mrts}

    for spot in spots:
        same_number_key = spot["SERIAL_NO"]
        if same_number_key in mrt_dict:
            mrt = mrt_dict[same_number_key]
            spot["MRT"] = mrt["MRT"]
            spot["district"] = mrt["address"].split(" ")[2][:3]
    return spots

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
        writer.writerow(["景點名稱", "區域", "經度", "緯度", "圖片網址"])
        writer.writerows(result)

def group_spots_by_mrt(spots):
    mrt_group = {}

    for spot in spots:
        mrt = spot["MRT"]
        if mrt not in mrt_group:
            mrt_group[mrt] = []
        mrt_group[mrt].append(spot["stitle"])
    return mrt_group

def retreive_mrt(mrt_data, spot_data):
    mrt_dict = {}
    for item in mrt_data:
        mrt = item['MRT']
        if mrt not in mrt_dict:
            mrt_dict[mrt] = [item['SERIAL_NO']]
        else:
            mrt_dict[mrt].append(item['SERIAL_NO'])

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
        mrt_and_spots = group_spots_by_mrt(spot_data)
        max_spots_count = max(len(spots) for spots in mrt_and_spots.values())
        chinese_num = ["一", "二", "三", "四", "五", "六"]
        fieldnames = ["捷運站"] + [f"景點{chinese_num[i]}" for i in range(max_spots_count)]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for mrt, spots in mrt_and_spots.items():
            row = {'捷運站': mrt}
            for i, spot in enumerate(spots):
                row[f"景點{chinese_num[i]}"] = spot
            for i in range(len(spots), max_spots_count):
                row[f"景點{chinese_num[i]}"] = ""
            writer.writerow(row)

spot_data = fetch_data("https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1")["results"]
mrt_data = fetch_data("https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2")

put_district_and_mrt_into_spots(spot_data, mrt_data)
retrieve_spot(spot_data, mrt_data)
retreive_mrt(mrt_data, spot_data)


