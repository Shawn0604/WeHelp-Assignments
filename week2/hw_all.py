print("==========task1==========")
# 定義捷運站和消息字典
stations = [
    "Songshan",
    "Nanjing Shanmin",
    "Taipei Arena",
    "Nanjing Fuxing",
    "Songjiang Nanjing",
    "Zhongshan",
    "Beimen",
    "Ximen",
    "Xiaonanmen",
    "Chiang Kai-Shek Memorial Hall",
    "Guting",
    "Taipower Building",
    "Gongguan",
    "Wanlong",
    "Jingmei",
    "Dapinglin",
    "Qizhang",
    "Xiaobitan",
    "Xindian City Hall",
    "Xindian"
]

messages = {
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Leslie": "I'm at home near Xiaobitan station.",
    "Vivian": "I'm at Xindian station waiting for you."
}

# 函數：獲取捷運站的索引
def get_station(station_name):
    # 返回捷運站的索引，如果找不到，則返回None
    if station_name == "Xiaobitan":
        return stations.index(station_name)
    elif station_name in stations:
        return stations.index(station_name)
    else:
        return None


def find_and_print(messages, current_station):
    # 返回在messages字典中，與當前車站最近的朋友的姓名，如果沒有找到則返回None。
    current_station_index = get_station(current_station)
    if current_station_index is None:
        return None

    nearest_friend = []
    min_distance = float('inf')

    # 尋找每個朋友的位置並計算與當前車站的距離
    for name, message in messages.items():
        station_name = None
        for station in stations:
            if station in message:
                station_name = station
                break

        # 如果找到了捷運站名稱，則計算距離並更新最近朋友列表
        if station_name is not None:
            friend_station_index = get_station(station_name)
            if friend_station_index is not None:
                distance = abs(current_station_index - friend_station_index)
                if distance<min_distance:
                    min_distance = distance
                    nearest_friend = [name]
                elif distance==min_distance:
                    nearest_friend.append(name)
    print(" ".join(nearest_friend))

# 測試函數
find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian


print("==========task2==========")
def book(consultants, hour, duration, criteria):
    # 根據標準對顧問進行排序
    if criteria == "price":
        sorted_consultants = sorted(consultants,key=lambda x: x["price"])
    elif criteria == "rate":
        sorted_consultants = sorted(consultants,key=lambda x: x["rate"], reverse=True)
    else:
        print("Invalid criteria")
        return
    
    # 遍歷排序後的顧問
    for consultant in sorted_consultants:
        # 檢查時間是否可用
        available = True
        for t in range(hour, hour + duration):
            if t in consultant.get("schedule", {}):
                available=False
                break
        
        # 如果時間可用，設置時間表並返回
        if available:
            for t in range(hour, hour + duration):
                consultant.setdefault("schedule", {})[t] = 1
            print(consultant["name"])
            return
    
    # 所有顧問都不可用
    print("No Service")

consultants = [
    {"name": "John", "rate": 4.5, "price": 1000},
    {"name": "Bob", "rate": 3, "price": 1200},
    {"name": "Jenny", "rate": 3.8, "price": 800}
]

# 測試資料
book(consultants, 15, 1, "price")  # Jenny
book(consultants, 11, 2, "price")  # Jenny
book(consultants, 10, 2, "price")  # John
book(consultants, 20, 2, "rate")   # John
book(consultants, 11, 1, "rate")   # Bob
book(consultants, 11, 2, "rate")   # No Service
book(consultants, 14, 3, "price")  # John

print("==========task3==========")
def func(*names):
    if not names:
        print("沒有資料")
        return

    middle_name_count = {}  # 用於統計中間名出現次數

    # 收集並統計每個名字的中間名
    for name in names:
        middle_index = len(name) // 2
        middle_name = name[middle_index]
        middle_name_count[middle_name] = middle_name_count.get(middle_name, 0) + 1

    # 找出只出現一次的中間名
    unique_middle_names = [name for name, count in middle_name_count.items() if count == 1]

    # 找到對應的名字並印出
    for name in names:
        middle_index = len(name) // 2
        if name[middle_index] in unique_middle_names:
            print(name)
            return

    print("沒有")



func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安


print("==========task4==========")
def get_number(index):
    if index % 3 == 0:
        number = 7 * (index // 3)
    elif index % 3 == 1:
        number = 7 * ((index + 2) // 3) - 3
    else:  
        number = 7 * ((index + 1) // 3) + 1
    print(number)


get_number(1)   # print 4
get_number(5)   # print 15
get_number(10)  # print 25
get_number(30)  # print 70
