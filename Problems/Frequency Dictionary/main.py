# put your python code here
#
# new_one = {key: len(key) for key in input().split()}
#


new_one = {}
for element in input().split():
    if element.lower() in new_one:
        new_one[element.lower()] += 1
    else:
        new_one[element.lower()] = 1


for key, value in new_one.items():
    print(f"{key} {value}")