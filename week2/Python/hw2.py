def book(consultants, hour, duration, criteria):
    # 根據標準對顧問進行排序
    if criteria == "price":
        sorted_consultants = sorted(consultants, key=lambda x: x["price"])
    elif criteria == "rate":
        sorted_consultants = sorted(consultants, key=lambda x: x["rate"], reverse=True)
    else:
        print("Invalid criteria")
        return
    
    # 遍歷排序後的顧問
    for consultant in sorted_consultants:
        # 檢查時間是否可用
        available = True
        for t in range(hour, hour + duration):
            if t in consultant.get("schedule", {}):
                available = False
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





