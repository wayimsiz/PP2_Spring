class Animal:
    def sound(self):
        print("Animal makes a sound")


class Dog(Animal):
    def sound(self):
        print("Dog barks")


class Cat(Animal):
    def sound(self):
        print("Cat meows")


a = Animal()
a.sound()

d = Dog()
d.sound()

c = Cat()
c.sound()