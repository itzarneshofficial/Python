import matplotlib.pyplot as plt
x=["Samsung","Apple","Nokia","Motorola","Mi","Vivo","OnePlus","Realme","Oppo","Lenovo","HTC","LG","Sony"]
y=[10000,800,5000,3000,2000,1500,1200,1100,900,700,600,400,300]
plt.figure(figsize=(10,5))
plt.pie(y,labels=x,shadow=True,startangle=0)
# plt.xlabel("Price in INR")
# plt.ylabel("Brands")
# plt.title("Mobile Brands and their Prices")
plt.show()