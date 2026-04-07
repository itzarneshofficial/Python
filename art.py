def triangles(a,b,c):
    if(a+b+c==180 and a>0 and b>0 and c>0 ):
        if(a<90 and b<90 and c<90):
            print("acute angled triangle")
        if(a>90 or b>90 or c>90):
            print("obtuce angled triangle")
        if(a==90 or b==90 or c==90):
            print("right angled triangle")
    else:
        print("triangle not possible")

def sides(x,y,z):
    if(x+y>z and x+z>y and y+z>x):
        if(x==y and y==z):
            print("equiletral triangle")
        if(x!=y and x!=z and y!=x):
            print("scalene triangle")
        if(x==y or y==z or z==x):   
            print("isoscels triangle")

a=eval(input("enter irct side"))
b=eval(input("enter second side"))
c=eval(input("enter thidr side"))
p=eval(input("enter first angle"))
q=eval(input("enter secont angle"))
r=eval (input("enter third angle"))
triangles(p,q,r)
sides(a,b,c)
