a=[]
c=0
for i in range(10):
    n=eval(input("Enter a Numbre in Ascending order:"))
    a.append(n)
s=eval(input("Enter a number to search:"))
lb=0
ub=9
while lb<=ub:
    mid=(lb+ub)//2
    if a[mid]==s:
        c=1
        print("Number found ")
        break
    elif a[mid]<s:
        lb=mid+1
    else:
        ub=mid-1
if c==0:
    print("Number not found in the list.")