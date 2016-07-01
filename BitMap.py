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
        
    """
        It tries to allocate in the best set of congruent free blocks that fits the requisition.
        Here, best set means the set of blocks with less blocks but more or exactly what is requested
            alloc_size: Requested size to allocate
    """
    def best_fit(self, alloc_size):
        # Starts to count virtual time
        self.time = 0
        # Initialize address to start the search
        add = 0
        # The first position of the best block
        best_block = 0
        # Starts the size of the best block with a very big value
        best_block_tam = self.size + 1
        # while there is blocks to be searched
        while add < self.size:
            # Counts access in the structure for the comparison below
            self.time += 1
            # If the first block is free
            if self.bitMap[add] == 0:
                # Starts a new search
                i = 0
                # While only less then alloc_size valid free blocks are found
                while add + i < self.size and self.bitMap[add + i] == 0:
                    self.time += 1
                    i += 1
                # If best_block is not the best ...
                if alloc_size <= i < best_block_tam:
                    # ... updates best_block and its size
                    best_block_tam = i
                    best_block = add
                # Jumps set of blocks
                add += i
            # Else tries the next
            else:
                add += 1
        # If a best_block was found
        if best_block_tam <= self.size:
            # Alocate the block
            i = 0
            while i < alloc_size:
                self.time += 1
                self.bitMap[best_block + i] = 1
                i += 1
            # Return first address of allocated Block
            return best_block
        # Else Return error
        return -1

    """
        It tries to allocate in the worst set of congruent free blocks that fits the requisition.
        Here, worst set means the set of blocks with more blocks possible
            alloc_size: Requested size to allocate
    """
    def worst_fit(self, alloc_size):
        # Starts to count virtual time
        self.time = 0
        # Initialize address to start the search
        add = 0
        # The first position of the worst block
        worst_block = 0
        # Starts the size of the best block with a very low value
        worst_block_tam = -1
        # while there is blocks to be searched
        while add < self.size:
            # Counts access in the structure for the comparison below
            self.time += 1
            # If the first block is free
            if self.bitMap[add] == 0:
                # Starts a new search
                i = 0
                # While only less then alloc_size valid free blocks are found
                while add + i < self.size and self.bitMap[add + i] == 0:
                    self.time += 1
                    i += 1
                # If worst_block is not the worst ...
                if i >= alloc_size and i > worst_block_tam:
                    # ... updates worst_block and its size
                    worst_block_tam = i
                    worst_block = add
                # Jumps set of blocks
                add += i
            # Else tries the next block
            else:
                add += 1
        # If a worst_block was found
        if worst_block_tam > 0:
            # Alocate the block
            i = 0
            while i < alloc_size:
                self.time += 1
                self.bitMap[worst_block + i] = 1
                i += 1
            # Return first address of allocated Block
            return worst_block
        # Else Return error
        return -1
    """
        Release a set of blocks starting in add with size alloc_size
            add: address to start the "desallocation"
            alloc_size: size of the "desallocation"
    """
    def free(self, add, alloc_size):
        # Starts to count virtual time
        self.time = 0
        # Put ones starting in add along alloc_size blocks
        i = 0
        while i < alloc_size:
            self.time += 1
            self.bitMap[add + i] = 0
            i += 1
    """
        Counts number of free blocks and the number of spaces, that are sets of congruent free blocks
    """
    def segmentation(self):
        spaces = 0
        i = -1
        while i < self.size:
            i += 1
            while i < self.size and self.bitMap[i] == 0:
                spaces += 1
                i += 1
        return (self.size - sum(self.bitMap),spaces)
