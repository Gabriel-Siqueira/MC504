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
        add = 0
        while add < self.size:
            if self.bitMap[add] == 0:
                i = 0
                while i < alloc_size and add + i < self.size and self.bitMap[add + i] == 0:
                    i += 1

                if i == alloc_size:
                    i = 0
                    while i < alloc_size:
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
        
        add_begin = self.add
        add = self.add
        second = False
        
        if alloc_size == 0:
            return self.add

        while not second or add != add_begin:
            second = True
            if self.bitMap[add] == 0:
                i = 0
                while i < alloc_size and add + i < self.size and self.bitMap[add + i] == 0:
                    i += 1
                
                if i == alloc_size:
                    i = 0
                    while i < alloc_size:
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
        add = 0
        best_block = 0
        best_block_tam = self.size + 1

        while add < self.size:
            if self.bitMap[add] == 0:
                i = 0
                while add + i < self.size and self.bitMap[add + i] == 0:
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
                self.bitMap[best_block + i] = 1
                i += 1
            return best_block
        return -1

    def worst_fit(self, alloc_size):
        add = 0
        worst_block = 0
        worst_block_tam = -1

        while add < self.size:
            if self.bitMap[add] == 0:
                i = 0
                while add + i < self.size and self.bitMap[add + i] == 0:
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
                self.bitMap[worst_block + i] = 1
                i += 1
            return worst_block
        return -1
        
    def free(self, add, alloc_size):
        i = 0
        while i < alloc_size:
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

        for block in self.mem_list:

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

        try:
            block = next(self.it)
        except StopIteration:
            self.it = iter(self.mem_list)
            block = next(self.it)
        id_begin = block.id
        second = False

        while not second or block.id != id_begin:
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

        best_block = -1

        for block in self.mem_list:

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

        worst_block = -1

        for block in self.mem_list:

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

        for block in self.mem_list:
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
        self.qll = {total_mem: [(0, total_mem)]}

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

    def quick_fit(self, alloc_size):
        if alloc_size in self.qll:

            l = self.qll[alloc_size]
            aux = l.pop()
            if not l:
                del self.qll[alloc_size]

            return aux[0]
        elif 2 * alloc_size in self.qll:
            l = self.qll[2 * alloc_size]
            aux = l.pop()
            if not l:
                del self.qll[2 * alloc_size]
            try:
                self.qll[alloc_size] += [(aux[1] - alloc_size, aux[1])]
            except KeyError:
                self.qll[alloc_size] = [(aux[1] - alloc_size, aux[1])]

            return aux[0]
        else:
            try:
                prox = alloc_size
                for q in self.qll:
                    if q > alloc_size:
                        prox = q
                        break

                try:
                    l = self.qll[prox]
                    aux = l.pop()
                    if not l:
                        del self.qll[prox]
                    try:
                        self.qll[prox - alloc_size] += [(aux[1] - (prox - alloc_size), aux[1])]
                    except KeyError:
                        self.qll[prox - alloc_size] = [(aux[1] - (prox - alloc_size), aux[1])]
                    return aux[0]
                except IndexError:
                    del self.qll[prox]
                except KeyError:
                    return -1

            except StopIteration:
                return -1

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

        # if size > 0
        if add_begin < add_end:
            try:
                self.qll[add_end - add_begin] += [(add_begin, add_end)]
            except KeyError:
                self.qll[add_end - add_begin] = [(add_begin, add_end)]

def teste(params, size):
    q = QuickFit(size)
    k = 1
    for i in range(0, len(params)):
        if i % 2 == 1:
            param = params[i]
            if idc == 'a':
                print("q.quick_fit(%d) returns %s" % (param, str(q.quick_fit(param))))
            elif idc == 'f':
                q.free(param[0], param[1])
                print("q.free(%d, %d)" % (param[0], param[1]))

            print("Resultado %d:\n" % (k), q)
            k += 1
        else:
            idc = params[i]

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

    def marge(self):
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

    def fit(self, id, size):
        if size > self.size:
            return -1
        elif not self.whole:
            if(self.left.fit(id, size) == -1):
                return self.right.fit(id, size)
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
                self.left.fit(id, size)
    def remove(self, id):
        if self.whole:
            if (not self.empty) and (self.id == id):
                self.empty = True
                self.id = -1
                return 1
            else:
                return -1
        else:
            self.left.remove(id)
            self.right.remove(id)
            self.marge()

class BuddySystem:
    def __init__(self, size):
        self.Memory = BuddyBlock(math.floor(math.log(size,2)))

    def __str__(self):
        return str(self.Memory)
    
    def __repr__(self):
        return repr(self.Memory)

    def buddy_system(self, id, size):
        return self.Memory.fit(id,size)

    def free(self, id):
        return self.Memory.remove(id)
