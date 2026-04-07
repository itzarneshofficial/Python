n=eval(input("Enter a number:"))
s=0
for i in range(1,n):
    if n%i==0:
        s=s+i
        # else:
        #     break
if n>s:
    print("Perfect Number")
else:
    print("Not Perfect Number")