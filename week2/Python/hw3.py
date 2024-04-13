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


# 測試資料
func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安



