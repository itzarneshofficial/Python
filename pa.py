a=input("enter the string")
s1=0#null string
s2=0#null string
for i in a :
    if(i.isupper()):
        s1=s1+1
    if(i.islower()):
        s2=s2+1
print("first string=",s1)
print("second string=",s2)            
