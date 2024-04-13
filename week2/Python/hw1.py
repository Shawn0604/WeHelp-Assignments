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
    "Gongguan", "Wanlong", 
    "Jingmei", "Dapinglin",
    "Qizhang", "Xiaobitan", 
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
        return stations.index("Qizhang")
    elif station_name in stations:
        return stations.index(station_name)
    else:
        return None

# 函數：找到最近的朋友
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
                if distance < min_distance:
                    min_distance = distance
                    nearest_friend = [name]
                elif distance == min_distance:
                    nearest_friend.append(name)
    print(" ".join(nearest_friend))

# 測試函數
find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivia



