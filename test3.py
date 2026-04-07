

# class Person:
#     name = "God"
#     occ = "Protector"
    
#     def __init__(self):
#         print("A function has Been called")
    

#     def info(self):
#         print(f"{self.name} is a {self.occ}")
        
# a=Person()
# a.name="Good"
# a.occ="Feeling of Hapiness"
# a.info()

# def greet(fx):
#     def mfx(args,kwargs):    
#         print("Starting a Function")
#         fx(args,kwargs)
#         print("Ended a Function")
#     return mfx    

# @greet

# def hello(a,b):
#     print("The is a Function")
#     print(a+b)

# hello(1,2)    

# class MyClass:
    
#     def __init__(self,value):
#         self._value = value
        
#     def show(self):
#         print(f"value is {self._value}")
    
#     @property
#     def ten_value(self):
#         return 10* self._value
    
#     @ten_value.setter
#     def ten_value(self,new_value):
#         self._value = new_value/10
#         return 10* self._value

# obj=MyClass(10)
# obj.ten_value=67
# print(obj.ten_value)
# obj.show()
