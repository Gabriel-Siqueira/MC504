class QuickFit:
    def __init__(self, total_mem):
        self.size = total_mem
        self.qll = {total_mem: [(0, total_mem)]}
        self.last = None
        self.time = 0

    def segmentation(self):
        blocks = sum([(b[1] - b[0]) for b in l for l in list(self.qll.values())])
        spaces = sum([len(l) for l in list(self.qll.values())])*self.size
        return (blocks,spaces)
        
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
