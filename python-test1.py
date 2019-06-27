#!/usr/bin/python3
print("Program to print half pyramid: ");
rows = input("Enter number of rows: ") or 6
rows = int(rows)    
list1 = []
start = 1
count = 1
while rows > 0:
    list1.append(start)
    if count % 2 == 0:
        start = start + 1
        count += 1
    else:
        start = start + 2
        count += 1
    rows = rows - 1    
# This of number to be printed in '*' pattern.
#print(list1)
for i in list1:
    for j in range(0, i):
        print("*", end=' ')
    print("\r")
