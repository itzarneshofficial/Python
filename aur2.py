c=65
n=1
for i in range (2,9,2):
    for j in range(1,i+1):
        if j%2==0:
            print(chr(c),end=" ")
            c+=1
        else:
            print(n,end=" ")
            n+=1
    print()