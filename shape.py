radius = int(input("Enter Radius: \n"))
num = int(input("Enter 1 for Circle Area,\nEnter 2 for Sqaure Area,\nEnter 3 for Triangle Area : \n"))
pi = 3.14159;
if num == 1:
  area = pi * radius * radius;
if num == 2:
  area = radius * radius;

if num == 3:
 area = radius * radius * 0.5;
 
print("Area: " + str(area));