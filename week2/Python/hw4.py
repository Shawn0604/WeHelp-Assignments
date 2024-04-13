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


