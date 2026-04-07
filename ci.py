p=eval(input("enter the principle"))
r=eval(input("enter the rate of interest"))
t=eval(input("enter the time in years"))
a=p[(1+r/100)**t]
print("The compound interest is",(a-p))