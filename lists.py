a = [3,6,4,4,2,5,6,4,2,8,6,9,0]
se = 0
so = 0
for i in a:
    if i%2==0:
        se = se + i
    else:
        so = so + i
print("Even Sum:",se)
print("Odd Sum:",so)