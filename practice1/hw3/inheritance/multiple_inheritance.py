class Father:
    def skill(self):
        print("Can fix things")


class Mother:
    def hobby(self):
        print("Can cook well")


class Child(Father, Mother):
    def play(self):
        print("Can play games")


c = Child()

c.skill()   # от Father
c.hobby()   # от Mother
c.play()    # свой метод