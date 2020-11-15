class rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def doesIntersect(self, pos):
        x = pos[0]
        y = pos[1]
        return (x >= self.x and x <= (self.x + self.w)) and (y >= self.y and y <= (self.y + self.h))

    def __repr__(self):
         return str(self.x) + "," + str(self.y) + "," + str(self.w) + "," + str(self.h)
