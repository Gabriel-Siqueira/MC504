import math

class BuddyBlock:

    """ Tree structure for the buddy system algorithm. """
    
    def __init__(self, power_size):
        self.whole = True # Indicate whether is a entire block or not.
        self.id    = -1   # Id of the process in this space, -1 if the node has no process.
        self.empty = True # Indicate whether is a empty block or not.
        self.power_size  = power_size # Exponent of the memory size.
        self.size  = 2**power_size    # Size of memory (in memory blocks).
        self.left  = None # Left half of the block.
        self.right = None # Right half of the block.

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

        """ Split a bigger block in two smaller halves. """

        # Does not split the smaller block size.
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

        """ Merge empty 'buddy blocks'. """

        # A whole block is already merged. 
        if self.whole:
            return 1
        # Check if both halves are empty. 
        if self.left.empty and self.right.empty:
            self.left = None
            self.right = None
            self.empty = True
            self.whole = True
            return 1
        else:
            return -1
        
    def fill(self, id):

        """ Fill a block with a process. """
        
        if(self.empty):
            self.id = id
            self.empty = False
            return 1
        else:
            return -1

    def fit(self, id, size, time):

        """ Find a block to insert the process. """

        # Count time for analysis.
        self.time = time

        # Check if this block can be used
        if size > self.size:
            return -1
        # If the block is not whole check the halves.
        elif not self.whole:
            if(self.left.fit(id, size, time + 1) == -1):
                r = self.right.fit(id, size, time + 1)
                # Count time for analysis.
                self.time = self.right.time
                return r
            else:
                # Count time for analysis.
                self.time = self.left.time
                return 1
        elif not self.empty:
            return -1
        # This is the right block size.
        elif size > self.size / 2:
            return self.fill(id)
        # Block is too big.
        else:
            if self.split() == -1:
                return -1
            else:
                self.left.fit(id, size, time + 1)

    def remove(self, id, time):

        """ Remove process with specific id. """
        
        # Count time for analysis.
        self.time = time
        # For whole blocks check if the id is the one to be removed.
        if self.whole:
            if (not self.empty) and (self.id == id):
                self.empty = True
                self.id = -1
                return 1
            else:
                return -1
        # For not whole blocks check the halves.
        else:
            self.left.remove(id, time + 1)
            # Count time for analysis.
            time = self.left.time
            self.right.remove(id, time + 1)
            # Count time for analysis.
            self.time = self.right.time
            # Merge if possible.
            self.merge()

    def segmentation(self):

        """ Calculate values to estimate segmentation. """

        if self.whole:
            if self.empty:
                return(1,self.size)
            else:
                return(0,0)
        else:
            (blocksl,spacesl) = self.left.segmentation()
            (blocksr,spacesr) = self.right.segmentation()
            return (blocksl + blocksr, spacesl + spacesr)
            
class BuddySystem:

    """ Acts like a interface between Operations and the structure. """
    
    def __init__(self, size):
        self.memory = BuddyBlock(math.floor(math.log(size,2)))

    def __str__(self):
        return str(self.memory)
    
    def __repr__(self):
        return repr(self.memory)

    def buddy_system(self, id, size):

        """ Performs the buddy system algorithm. """
        
        r = self.memory.fit(id,size,1)
        self.time = self.memory.time
        return r
        
    def free(self, id):

        """ Free memory used for some process. """
        
        r = self.memory.remove(id,1)
        self.time = self.memory.time
        return r

    def segmentation(self):

        """ Calculate values to estimate segmentation. """

        return self.memory.segmentation()
