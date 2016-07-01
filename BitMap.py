"""
    Defines structure of bit map to handle all the blocks of memory
"""


class BitMap:
    """
        Constructor:
            size: Is the total number of memory blocks
    """
    def __init__(self, size):
        self.size = size
        # Starts all bits with zero
        self.bitMap = [0] * size
        # Last address for the next fit
        self.add = 0
        # Virtual time counter of each operation
        self.time = 0

    def __str__(self):
        s = ""
        for bit in self.bitMap:
            s += str(bit)

        return s + "\n"

    def __repr__(self):
        return str(self)
    """
        It tries to allocate in the first set of congruent free blocks that fits the requisition
            alloc_size: Requested size to allocate
    """
    def first_fit(self, alloc_size):
        # Starts to count the virtual time
        self.time = 0
        # Initialization of the address that will iterate through all the bits in the Bit Map
        add = 0
        # Condition of iteration
        while add < self.size:
            # For each access in the memory that will be made in the comparison of the if right below
            self.time += 1
            # If the first block is free
            if self.bitMap[add] == 0:
                # Tries to find a set of alloc_size congruent free blocks
                i = 0
                # While only less then alloc_size valid free blocks are found
                while i < alloc_size and add + i < self.size and self.bitMap[add + i] == 0:
                    # Counts an access in the structure
                    self.time += 1
                    # Increment the size already found
                    i += 1
                # If a set of alloc_size blocks is found
                if i == alloc_size:
                    # Allocate that block
                    i = 0
                    while i < alloc_size:
                        self.time += 1
                        self.bitMap[add + i] = 1
                        i += 1
                    return add
                # Else, jumps that set of blocks
                else:
                    add += i
            # Else tries the next block
            else:
                add += 1
        # If address found is out of range returns error
        if add >= self.size:
            return -1

    def next_fit(self, alloc_size):
        # Starts to count the virtual time
        self.time = 0
        # Save initial address
        add_begin = self.add
        # Continue where stops last time
        add = self.add
        second = False
        
        
        if alloc_size == 0:
            return self.add

        # Just stops in the socond time the address is the initial address
        while not second or add != add_begin:
            
            second = True
    
            # For each access in the memory that will be made in the comparison of the if right below
            self.time += 1
            # If the first block is free
            if self.bitMap[add] == 0:
                # Tries to find a set of alloc_size congruent free blocks
                i = 0
                # While only less then alloc_size valid free blocks are found
                while i < alloc_size and add + i < self.size and self.bitMap[add + i] == 0:
                    # Counts an access in the structure
                    self.time += 1
                    # Increment the size already found
                    i += 1
                # If a set of alloc_size blocks is found
                if i == alloc_size:
                    # Allocate that block
                    i = 0
                    while i < alloc_size:
                        
                        self.time += 1
                        self.bitMap[add + i] = 1
                        i += 1

                    self.add = (add + alloc_size) % self.size
                    return add
                # Else, jumps that set of blocks
                else:
                    # already pass through all the bits
                    if add < add_begin and add + i >= add_begin:
                        return -1
                    # back to begin
                    elif(add + i >= self.size):
                        add = 0
                    else:
                        add = add + i
            # Else tries the next block
            else:
                add = (add + 1) % self.size
        return -1
        
    def best_fit(self, alloc_size):
        self.time = 0
        add = 0
        best_block = 0
        best_block_tam = self.size + 1

        while add < self.size:
            self.time += 1
            if self.bitMap[add] == 0:
                i = 0
                while add + i < self.size and self.bitMap[add + i] == 0:
                    self.time += 1
                    i += 1

                if i >= alloc_size and i < best_block_tam:
                    best_block_tam = i
                    best_block = add
                add += i
            else:
                add += 1

        if best_block_tam <= self.size:
            i = 0
            while i < alloc_size:
                self.time += 1
                self.bitMap[best_block + i] = 1
                i += 1
            return best_block
        return -1

    def worst_fit(self, alloc_size):
        self.time = 0
        add = 0
        worst_block = 0
        worst_block_tam = -1

        while add < self.size:
            self.time += 1
            if self.bitMap[add] == 0:
                i = 0
                while add + i < self.size and self.bitMap[add + i] == 0:
                    self.time += 1
                    i += 1

                if i >= alloc_size and i > worst_block_tam:
                    worst_block_tam = i
                    worst_block = add
                add += i
            else:
                add += 1

        if worst_block_tam > 0:
            i = 0
            while i < alloc_size:
                self.time += 1
                self.bitMap[worst_block + i] = 1
                i += 1
            return worst_block
        return -1
        
    def free(self, add, alloc_size):
        self.time = 0
        i = 0
        while i < alloc_size:
            self.time += 1
            self.bitMap[add + i] = 0
            i += 1

    def segmentation(self):
        spaces = 0
        i = -1
        while i < self.size:
            i += 1
            while i < self.size and self.bitMap[i] == 0:
                spaces += 1
                i += 1
        return (self.size - sum(self.bitMap),spaces)
