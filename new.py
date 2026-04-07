s=eval(input("Enter a Number to be searched:"))
a=0
b=1
l=0
while l==0:
    c=a+b
    if s==a:
        l=l+1
        break
    else:
        break
    a=b
    b=c
if l==1:
    print("Present")
else:
    print("Not present")