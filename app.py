import time,filter,threading

file1 = open('./ten_min_data.txt', 'r')
Lines = file1.readlines()

# def set_interval(func, sec):
#     def func_wrapper():
#         set_interval(func, sec)
#         func()
#     t = threading.Timer(sec, func_wrapper)
#     t.start()
#     return t


for line in Lines:
    filter.check_line(line)
    filter.writedata()
    time.sleep(0.05)
