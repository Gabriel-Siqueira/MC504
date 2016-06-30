import math

class BuddyBlock:

    def __init__(self, power_size):
        self.whole = True
        self.id    = -1
        self.empty = True
        self.power_size  = power_size
        self.size  = 2**power_size
        self.left  = None
        self.right = None

    def __str__(self):
        s = "  ["
        if self.left != None:
            s += str(self.left)
        if self.whole:
            s += "  " + repr(self.id) + " (" + repr(self.size) + ")"
        if self.right != None:
            s += str(self.right)
        s += "  ]"
        return s

    def __repr__(self):
        return str(self)
        
    def split(self):
        if (self.size == 2) or not self.empty:
            return -1
        else:
            self.id    = -1
            self.whole = False
            self.empty = False
            self.left  = BuddyBlock(self.power_size - 1)
            self.right = BuddyBlock(self.power_size - 1)
            return 1

    def merge(self):
        if self.whole:
            return 1
        if self.left.empty and self.right.empty:
            self.left = None
            self.right = None
            self.empty = True
            self.whole = True
            return 1
        else:
            return -1
        
    def fill(self, id):
        if(self.empty):
            self.id = id
            self.empty = False
            return 1
        else:
            return -1

    def fit(self, id, size, time):
        self.time = time
        if size > self.size:
            return -1
        elif not self.whole:
            if(self.left.fit(id, size, time + 1) == -1):
                r = self.right.fit(id, size, time + 1)
                self.time = self.right.time
                return r
            else:
                self.time = self.left.time
                return 1
        elif not self.empty:
            return -1
        elif size > self.size / 2:
            return self.fill(id)
        else:
            if self.split() == -1:
                return -1
            else:
                self.left.fit(id, size, time + 1)

    def remove(self, id, time):
        self.time = time
        if self.whole:
            if (not self.empty) and (self.id == id):
                self.empty = True
                self.id = -1
                return 1
            else:
                return -1
        else:
            self.left.remove(id, time + 1)
            time = self.left.time
            self.right.remove(id, time + 1)
            self.time = self.right.time
            self.merge()

    def segmentation(self):
        if self.whole = True:
        
        return ()
            
class BuddySystem:
    def __init__(self, size):
        self.memory = BuddyBlock(math.floor(math.log(size,2)))

    def __str__(self):
        return str(self.memory)
    
    def __repr__(self):
        return repr(self.memory)

    def buddy_system(self, id, size):
        r = self.memory.fit(id,size,1)
        self.time = self.memory.time
        return r
        
    def free(self, id):
        r = self.memory.remove(id,1)
        self.time = self.memory.time
        return r

    def segmentation(self):
        return self.memory.segmentation()
