# dic={1:"apple",2:"banana"}
# dic[3]="cherry"
# print(dic)


# a=33000
# b=3333
# print("a") if a>b else ("=") if a==b else print("b")


# def f(n):
#     if n==0 or n==1:
#         return 1
#     else:
#         return n * f(n-1)
# print(f(5))


# import matplotlib.pyplot as plt

# x=[1,2,3,4,5,6,7,8,9]
# y=[9,8,7,6,5,4,3,2,1]
# plt.bar(x,y)
# plt.show()

# s=1
# for i in range(1,8,2):
#     for j in range(1,i+1):
#         if s % 2 != 0:    
#             print("#",end=" ")
#         else:
#             print("*",end=" ")
#     s+=1
#     print()


# for i in range(1,8,2):
#     for j in range(1,i+1):
#         if i % 2 == 0:    
#             print("#",end=" ")
#         else:
#             print("*",end=" ")
#     print()

# import matplotlib.pyplot as plt

# x=[" Samsung " , " Mi " , " Vivo " , " Nokia " , " Apple "]
# y=[" 10000 " , " 900 " , " 10 " , " 300 " , " 1000 "]
# plt.pie(y,labels=x)
# plt.show()


# ch = 'd'  
# n = ord(ch) - 35;  
# print (n);  
# print(chr(n))


# m=4  
# n=8  
# for i in range(5):  
#         pass  
# print(m+n+i  )
# print("p=",p)  


# a = 1  
# while (a < 50):  
#     if a%5==0:  
#         break  
#     else:  
#         print(a)  
#     a += 8  


# x = {3:"Apple", -1:"Banana", 1:"Mango",-2:"Orange"}  
# x [2] = "Cherry"  
# print (x)  



# def isDudney(n):
#     m=n;s=0
#     while m > 0:
#         d=m%10
#         s=s+d
#         m=m//10
#     if s**3 == n:
#         return True
#     else:
#         return False
# n=eval(input("Enter a Number:"))
# p=isDudney(n)
# if p == True:
#     print("Dudney Number")
# else:
#     print("Not a Dudney Number")


# p=eval(input("Enter the Price:"))
# d=0
# if p>75000:
#     d=(10/100)*p
# elif p>45000:
#     d=(7.5/100)*p
# elif p>20000:
#     d=(5/100)*p
# else:
#     d=0
# print("The Amount to be Paid:",(p-d))


# a=[1,2,3,4,5,6,7,8,9,10]
# a.insert(6,400)
# a.append(800)
# a.sort()
# for i in a:
#     if i==500:
#         print(a.index(i))
#         break
#     else:
#         o=1
# if o==1:
#     print("Not Present")
# print(a)


# l=[1,2,"a","b"]
# t=tuple(l)
# print(t)
# for i in t:
#     print(i)



# s=input("Enter a String:")
# a=0
# v=0
# r=" "
# d=s
# d=d.upper()
# for i in d:
#     if i.isalpha():
#         if i=="A" or i=="E" or i=="I" or i=="O" or i=="U":
#             v=v+1
#         a=a+1
# for j in s:
#     if j.isalpha():
#         if j.isupper():
#             j=j.lower()
#             r=r+j
#         else:
#             j=j.upper()
#             r=r+j
#     else:
#         r=r+j
# print("No. of Alphabets",a)
# print("No. of Vovels:",v)
# print(r)



# s=input("Enter A String:")
# s=s.upper()
# o=0
# n=""
# for i in s:
#     if i.isalpha():
#         if i=="A" or i=="E" or i=="O" or i=="I" or i=="U":
#             o=ord(i)
#             c=o+1
#             n=n+chr(c)
#         else:
#             o=ord(i)
#             c=o-1
#             n=n+chr(c)
#     else:
#         n=n+i
#     o=0
# print(n)



# s="BOARDS EXAMINATION"
# print(s[0:4:2])


