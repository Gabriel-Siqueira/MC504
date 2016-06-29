import math
            
class BitMap:
    def __init__(self, size):
        self.size = size
        self.bitMap = [0]*size
        self.add = 0
    
    def __str__(self):
        s = ""
        for bit in self.bitMap:
            s+=str(bit)

        return s + "\n"
    
    def __repr__(self):
        return str(self)
        
    def first_fit(self, alloc_size):
        self.time = 0
        add = 0
        while add < self.size:
            self.time += 1
            if self.bitMap[add] == 0:
                i = 0
                while i < alloc_size and add + i < self.size and self.bitMap[add + i] == 0:
                    self.time += 1
                    i += 1
                if i == alloc_size:
                    i = 0
                    while i < alloc_size:
                        self.time += 1
                        self.bitMap[add + i] = 1
                        i += 1
                    return add
                else:
                    add += i
            else:
                add += 1
        if add >= self.size:
            return -1
        
    def next_fit(self, alloc_size):
        self.time = 0
        add_begin = self.add
        add = self.add
        second = False
        
        
        if alloc_size == 0:
            return self.add

        while not second or add != add_begin:
            
            second = True
    
            self.time += 1
            if self.bitMap[add] == 0:
                i = 0
                while i < alloc_size and add + i < self.size and self.bitMap[add + i] == 0:
                    self.time += 1
                    i += 1
                
                if i == alloc_size:
                    i = 0
                    while i < alloc_size:
                        
                        self.time += 1
                        self.bitMap[add + i] = 1
                        i += 1

                    self.add = (add + alloc_size) % self.size
                    return add

                else:
                    if add < add_begin and add + i >= add_begin:
                        return -1
                    elif(add + i >= self.size):
                        add = 0
                    else:
                        add = add + i
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

            if block.size - alloc_size > 0:
                block_free = MemBlock(0, block.size - alloc_size)
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

            if block.size - alloc_size > 0:
                block_free = MemBlock(0, block.size - alloc_size)
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

class QuickFit:
    def __init__(self, total_mem):
        self.size = total_mem
        self.qll = {total_mem: [(0, total_mem)]}
        self.last = None
        self.time = 0

    def __str__(self):
        s = ""
        if self.qll:
            for q in self.qll:
                s += "%d msu: %s\n" % (q, self.qll[q])
        else:
            s += "(Empty)"

        return s

    def __repr__(self):
        return str(self)

    def alloc_block(self, size, block):
        if size in self.qll:
            self.qll[size] += [block]
        elif size > 0:
            self.qll[size] = [block]

    def fit(self, to_remove, alloc_size):
        if to_remove not in self.qll or not self.qll[to_remove]:
            return -1

        l = self.qll[to_remove]

        aux = l.pop()

        if not l:
            del self.qll[to_remove]

        block_size = to_remove - alloc_size
        position1 = aux[1]
        position0 = position1 - block_size
        new_block = (position0, position1)

        if block_size < 0:
            return -1

        self.alloc_block(block_size, new_block)

        return aux[0]

    def first_fit(self, alloc_size):
        to_remove = alloc_size
        for q in self.qll:
            if q >= alloc_size:
                to_remove = q
                break

        return self.fit(to_remove, alloc_size)

    def next_fit(self, alloc_size):
        if not self.last:
            self.last = alloc_size

        to_remove = self.last

        for q in self.qll:
            if q >= self.last:
                to_remove = q
                break

        return self.fit(to_remove, alloc_size)

    def best_fit(self, alloc_size):
        min_size = self.size + 1

        for q in self.qll:
            if alloc_size <= q < min_size:
                min_size = q

        return self.fit(min_size, alloc_size)

    def worst_fit(self, alloc_size):
        max_size = alloc_size

        for q in self.qll:
            if q > max_size:
                max_size = q

        return self.fit(max_size, alloc_size)

    def free(self, add_begin, size):
        add_end = add_begin + size
        viz_ant, viz_prox = None, None
        to_delete = [None] * 2
        cont = 0
        for q in self.qll:
            for block in self.qll[q]:
                if add_end == block[0]:
                    viz_prox = block
                    l = self.qll[q]
                    l.remove(block)
                    if not l:
                        to_delete[0] = q

                    cont += 1

                if block[1] == add_begin:
                    viz_ant = block
                    l = self.qll[q]
                    l.remove(block)
                    if not l:
                        to_delete[1] = q

                    cont += 1
                if cont == 2:
                    break

        for i in range(0, 2):
            if to_delete[i]:
                del self.qll[to_delete[i]]

        if viz_ant:
            add_begin = viz_ant[0]

        if viz_prox:
            add_end = viz_prox[1]

        block_size = add_end - add_begin

        if block_size < 0:
            return -1

        self.alloc_block(block_size, (add_begin, add_end))

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
                return self.right.fit(id, size, time + 1)
            else:
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
            self.right.remove(id, time + 1)
            self.merge()

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
