class MemBlock:
    def __init__(self, block_id, block_size):
        self.id = block_id
        self.size = block_size

    def __str__(self):
        return "(%d, %d)" % (self.id, self.size)
    
    def __repr__(self):
        return str(self)

class LinkedList:
    
    def __init__(self, total_mem):
        self.mem_list = []
        self.mem_list.append(MemBlock(0, total_mem))
        self.it = iter(self.mem_list)
    
    def __str__(self):
        return ", ".join(([str(l) for l in self.mem_list]))
    
    def __repr__(self):
        return str(self)

    def first_fit(self, process_id, alloc_size):
        self.time = 0
        for block in self.mem_list:
            self.time += 1
            if block.id == 0 and block.size >= alloc_size:
                block_used = MemBlock(process_id, alloc_size)
                self.mem_list.insert(self.mem_list.index(block), block_used)

                if block.size - alloc_size > 0:
                    block_free = MemBlock(0, block.size - alloc_size)
                    self.mem_list.insert(self.mem_list.index(block_used)+1, block_free)

                self.mem_list.remove(block)

                return self.mem_list.index(block_used)

        return -1

    def next_fit(self, process_id, alloc_size):
        self.time = 0 
        try:
            block = next(self.it)
        except StopIteration:
            self.it = iter(self.mem_list)
            block = next(self.it)
        id_begin = block.id
        second = False

        while not second or block.id != id_begin:
            self.time += 1 
            second = True
            
            if block.id == 0 and block.size >= alloc_size:
                block_used = MemBlock(process_id, alloc_size)
                self.mem_list.insert(self.mem_list.index(block), block_used)

                if block.size - alloc_size > 0:
                    block_free = MemBlock(0, block.size - alloc_size)
                    self.mem_list.insert(self.mem_list.index(block_used)+1, block_free)

                self.mem_list.remove(block)

                return self.mem_list.index(block_used)
            
            try:
                block = next(self.it)
            except StopIteration:
                self.it = iter(self.mem_list)
                block = next(self.it)

        return -1

    def best_fit(self, process_id, alloc_size):
        self.time = 0 
        best_block = -1

        for block in self.mem_list:
            self.time += 1 
            if block.id == 0 and block.size >= alloc_size:
                if best_block == -1 :
                    best_block = block
                else:
                    if block.size < best_block.size:
                        best_block = block

        if best_block != -1:

            block_used = MemBlock(process_id, alloc_size)
            self.mem_list.insert(self.mem_list.index(best_block), block_used)

            if best_block.size - alloc_size > 0:
                block_free = MemBlock(0, best_block.size - alloc_size)
                self.mem_list.insert(self.mem_list.index(block_used)+1, block_free)

            self.mem_list.remove(best_block)

            return self.mem_list.index(block_used)
        else:
            return -1

    def worst_fit(self, process_id, alloc_size):
        self.time = 0 
        worst_block = -1

        for block in self.mem_list:

            self.time += 1 
            if block.id == 0 and block.size >= alloc_size:
                if worst_block == -1 :
                    worst_block = block
                else:
                    if block.size > worst_block.size:
                        worst_block = block
                            
        if worst_block != -1:

            block_used = MemBlock(process_id, alloc_size)
            self.mem_list.insert(self.mem_list.index(worst_block), block_used)

            if worst_block.size - alloc_size > 0:
                block_free = MemBlock(0, worst_block.size - alloc_size)
                self.mem_list.insert(self.mem_list.index(block_used)+1, block_free)

            self.mem_list.remove(worst_block)

            return self.mem_list.index(block_used)
        else:
            return -1

    def free(self, process_id):
        self.time = 0 
        
        for block in self.mem_list:
            self.time += 1 
            if block.id == process_id:
                index = self.mem_list.index(block)
                if index != 0 and self.mem_list[index-1].id == 0:
                    block_free = MemBlock(0, self.mem_list[index].size + self.mem_list[index-1].size)
                    self.mem_list.insert(index-1, block_free)
                    self.mem_list.remove(block)
                    block = self.mem_list[index]
                    self.mem_list.remove(block)
                    block = self.mem_list[index-1]
                    index = index - 1

                if index != len(self.mem_list)-1 and self.mem_list[index+1].id == 0:
                    block_free = MemBlock(0, self.mem_list[index].size + self.mem_list[index+1].size)
                    self.mem_list.insert(index, block_free)
                    self.mem_list.remove(block)
                    block = self.mem_list[index+1]
                    self.mem_list.remove(block)

                if self.mem_list[index].id != 0:
                    block_free = MemBlock(0, self.mem_list[index].size)
                    self.mem_list.insert(index, block_free)
                    self.mem_list.remove(block)

                return 1
        return -1

    def segmentation(self):
        blocks = 0
        spaces = 0
        for i in self.mem_list:
            if(i.id == 0):
                blocks += i.size
                spaces += 1
        return (blocks,spaces)
