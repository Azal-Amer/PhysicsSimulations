# Even though there are multiple objects, we still only need one class. 
# No matter how many cookies we make, only one cookie cutter is needed.
class Car(object):
# The Constructor is defined with arguments.
    def __init__(self, c, xpos, ypos, zpos, xspeed):
        self.c = c
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
        self.xspeed = xspeed
        
    def display(self):
        stroke(0)
        fill(self.c)
        rectMode(CENTER)
        box(100, 100,100)
        translate(self.xpos, self.ypos, self.zpos);
        
    def drive(self):
        self.xpos = self.xpos + self.xspeed;
        if self.xpos > width:
            self.xpos = 0
myCar2 = Car(color(0, 0, 255), 0, 100, 5, 3)

myCar1 = Car(color(255, 0, 0), 0, 100, 5, 4)

def setup():
    size(200,200,P3D)
    
def draw(): 
  background(255)
  myCar1.drive()
  myCar1.display()
  myCar2.drive()
  myCar2.display()
