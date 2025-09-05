class Rectangle:
    def __init__(self, width, length):
        self.width = width
        self.length = length
        
    def calc_area(self):
        return (self.width*self.length)

area = Rectangle(3, 5)

print ("area of rectangle: ", area.calc_area())