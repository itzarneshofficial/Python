l=eval(input("Enter the size of the list: "))
a = []
c=0
for i in range(l):
    n = eval(input("Enter a number in descending order: "))
    a.append(n)
s = eval(input("Enter a number to search: "))
lb = 0
ub = l - 1
while lb <= ub:
    mid = (lb + ub) // 2
    if a[mid] == s:
        c = 1
        print("Number found")
        break
    elif a[mid] > s:
        lb = mid + 1
    else:
        ub = mid - 1
if c == 0:
    print("Number not found in the list.")