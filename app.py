import time,filter,sys

#####Uncomment to run on simulation##################
# file1 = open('./ten_min_data.txt', 'r')
# Lines = file1.readlines()

# for line in Lines:
#     filter.check_line(line)
#     filter.writedata()
#     time.sleep(0.05)
#####################################################

for line in sys.stdin:
    # print(f'Input{i} : {line}', flush=True)
    filter.check_line(line)
    filter.writedata()