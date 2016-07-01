class MemBlock:
    
    """Node of the list that has size and id of a process or free space"""
    
    def __init__(self, block_id, block_size):
        self.id = block_id
        self.size = block_size

    def __str__(self):
        return "(%d, %d)" % (self.id, self.size)
    
    def __repr__(self):
        return str(self)

class LinkedList:
    
    """Structure that represents memory divided in a sequence of blocks of processes or free spaces"""
    
    def __init__(self, total_mem):
        self.mem_list = []
        self.mem_list.append(MemBlock(0, total_mem))
        self.it = iter(self.mem_list)
    
    def __str__(self):
        return ", ".join(([str(l) for l in self.mem_list]))
    
    def __repr__(self):
        return str(self)

    def first_fit(self, process_id, alloc_size):
        
        """ Put a process of size alloc_size and id process_id in the first position of memory that has enough space """
        
        self.time = 0
        
        for block in self.mem_list:                                          #Loop for every block in the list
            self.time += 1
            if block.id == 0 and block.size >= alloc_size:                   # If block is a free space and has enough space
                block_used = MemBlock(process_id, alloc_size)                # Create a new block with the size of the process and its id
                self.mem_list.insert(self.mem_list.index(block), block_used) #Put this new block in the position of the original block

                if block.size - alloc_size > 0:                              #If there is some space in the original block that was not filled
                    block_free = MemBlock(0, block.size - alloc_size)        # Create a new block of free space and the size that was left
                    self.mem_list.insert(self.mem_list.index(block_used)+1, block_free) #Put this block after the new process block

                self.mem_list.remove(block)                                  #Remove the original block from the list

                return self.mem_list.index(block_used)

        return -1

    def next_fit(self, process_id, alloc_size):
        
        """ Put a process of size alloc_size and id process_id in the first position of memory after the last one chosen that has enough space """

        # initiate time.
        self.time = 0

        # Recover interator from last allocation.
        try:
            block = next(self.it)
        except StopIteration:
            self.it = iter(self.mem_list)
            block = next(self.it)

        # Save id from first block.
        id_begin = block.id
        second = False

        # Stop when is on the first block for the second time.
        while not second or block.id != id_begin:
            self.time += 1 
            second = True

            # If block is a free space and has enough space.
            if block.id == 0 and block.size >= alloc_size:
                # Create a new block with the of the size process and its id.
                block_used = MemBlock(process_id, alloc_size)
                # Put this new block in the position of the original block.
                self.mem_list.insert(self.mem_list.index(block), block_used)

                # If there is some space in the original block that was not filled.
                if block.size - alloc_size > 0:
                    # Create a new block of free space and the size that was left.
                    block_free = MemBlock(0, block.size - alloc_size)
                    # Put this block after the new process block.
                    self.mem_list.insert(self.mem_list.index(block_used)+1, block_free)

                # Remove the original block from the list.
                self.mem_list.remove(block)

                return self.mem_list.index(block_used)
            
            try:
                block = next(self.it)
            except StopIteration:
                self.it = iter(self.mem_list)
                block = next(self.it)

        return -1

    def best_fit(self, process_id, alloc_size):
        
        """ Put a process of size alloc_size and id process_id in the position of memory that has enough space and is the small block available """
        self.time = 0 
        best_block = -1

        for block in self.mem_list:     #Loop for every block on the list
            self.time += 1 
            if block.id == 0 and block.size >= alloc_size: #If this block is a free space and has enough space
                if best_block == -1 :   # If no best block was chosen
                    best_block = block  # Make this block the best block
                else:                   # If already have a best block
                    if block.size < best_block.size: #If this block has smaller size than the best block
                        best_block = block           # Make this block the best block

        if best_block != -1: #If was found some best block

            block_used = MemBlock(process_id, alloc_size)                       #Create a new block with the size of the process and its id
            self.mem_list.insert(self.mem_list.index(best_block), block_used)   #Put this new block in the position of the original block

            if best_block.size - alloc_size > 0:                                #If there is some space in the original block that was not filled
                block_free = MemBlock(0, best_block.size - alloc_size)          # Create a new block of free space and the size that was left
                self.mem_list.insert(self.mem_list.index(block_used)+1, block_free) #Put this block after the new process block

            self.mem_list.remove(best_block)    #Remove the original block from the list

            return self.mem_list.index(block_used)
        else:
            return -1

    def worst_fit(self, process_id, alloc_size):
        
         """ Put a process of size alloc_size and id process_id in the position of memory that has enough space and is the biggest block available """
        self.time = 0 
        worst_block = -1

        for block in self.mem_list: #Loop for every block on the list

            self.time += 1 
            if block.id == 0 and block.size >= alloc_size: #If this block is a free space and has enough space
                if worst_block == -1 :                     # If no worst block was chosen
                    worst_block = block                    # Make this block the worst block
                else:                                      # If already have a worst block
                    if block.size > worst_block.size:
                        worst_block = block                # Make this block the worst block
                            
        if worst_block != -1:                              #If was found some worst block

            block_used = MemBlock(process_id, alloc_size)                           #Create a new block with the size of the process and its id
            self.mem_list.insert(self.mem_list.index(worst_block), block_used)      #Put this new block in the position of the original block

            if worst_block.size - alloc_size > 0:                                   #If there is some space in the original block that was not filled
                block_free = MemBlock(0, worst_block.size - alloc_size)             # Create a new block of free space and the size that was left
                self.mem_list.insert(self.mem_list.index(block_used)+1, block_free) #Put this block after the new process block

            self.mem_list.remove(worst_block)   #Remove the original block from the list

            return self.mem_list.index(block_used)
        else:
            return -1

    def free(self, process_id):
        self.time = 0 
        
        for block in self.mem_list:                                 #Loop for every block on the list
            self.time += 1 
            if block.id == process_id:                              #If this block has the process to be released
                index = self.mem_list.index(block)                  #Get its index on the list
                if index != 0 and self.mem_list[index-1].id == 0:   #If is not the first block of the list and the block before is a free space
                    block_free = MemBlock(0, self.mem_list[index].size + self.mem_list[index-1].size) #Create a new block with the sum of sizes
                    self.mem_list.insert(index-1, block_free)       #Puts this new block on the list
                    self.mem_list.remove(block)                     #Removes the original block form the list
                    block = self.mem_list[index]
                    self.mem_list.remove(block)                     #Removes the block before the original
                    block = self.mem_list[index-1]
                    index = index - 1                               #Update index to the index of the new free space block

                if index != len(self.mem_list)-1 and self.mem_list[index+1].id == 0:    #If is not the last block and the block after is a free space
                    block_free = MemBlock(0, self.mem_list[index].size + self.mem_list[index+1].size) #Create a new block with the sum of sizes
                    self.mem_list.insert(index, block_free)                             #Puts this new block on the list
                    self.mem_list.remove(block)                                         #Removes the original block of the list
                    block = self.mem_list[index+1]
                    self.mem_list.remove(block)                                         #Removes the block after the original

                if self.mem_list[index].id != 0:                                        #If no merge was done
                    block_free = MemBlock(0, self.mem_list[index].size)                 #Create a new block with the same size
                    self.mem_list.insert(index, block_free)                             #Insert this block on the list
                    self.mem_list.remove(block)                                         #Removes the original block from the list

                return 1
        return -1

    def segmentation(self):

        """ Calculate values to estimate segmentation. """
        
        blocks = 0
        spaces = 0
        # Iterate through all nodes and count the number of nodes(spaces) and blocks
        for i in self.mem_list:
            if(i.id == 0):
                blocks += i.size
                spaces += 1
        return (blocks,spaces)
