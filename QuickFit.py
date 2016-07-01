"""
    Implements a Hash-Table in wich values are lists of blocks and keys are the sizes of the blocks. Each block is represented by a tuple of two values: (first position, last position + 1).
"""


class QuickFit:
    """
        Constructor:
            size: Total size of the memory
            qll: Is the Hash-Table of Lists whose keys are the memory sizes and values are lists of blocks.
            time: Is the variable responsible for keep the virtual time that the operations take to get done
    """

    def __init__(self, total_mem):
        self.size = total_mem
        self.qll = {total_mem: [(0, total_mem)]}
        self.time = 0

    """
        Function defined measure the segmentation of the memory in this structure:
        returns:
            blocks: Number of free blocks of memory
            spaces: Number of contiguous sets of blocks of free memory

    """

    def segmentation(self):
        blocks = 0
        for l in list(self.qll.values()):
            blocks += sum([(b[1] - b[0]) for b in l])
        spaces = sum([len(l) for l in list(self.qll.values())])
        return blocks, spaces

    def __str__(self):
        s = ""
        if self.qll:
            for q in self.qll:
                s += "Tam : %d: %s\n" % (int(q), self.qll[q])
        else:
            s += "(Empty)"

        return s

    def __repr__(self):
        return str(self)

    """
        Insert a block of free memory into the structure
            Size: Size of the block that is being inserted
            Block: Block been inserted
    """

    def insert_block(self, size, block):
        if size in self.qll:
            self.qll[size] += [block]
        elif size > 0:
            self.qll[size] = [block]

    """
        It is used in all the other *_fit to fit a block inside another one, greater or equal to the one being allocated
        Fits a block of size alloc_size in the block to_remove, whose size must be bigger than alloc_size.
            to_remove: Is the block from witch the block been allocated will be extracted
            alloc_size: The size to be allocated
        Returns -1 if it is not possible to allocate and the first position of the block being allocated.
    """

    def fit(self, to_remove, alloc_size):
        # If the block to_remove is not in the structure the operation is invalid
        # If the list of blocks of the size to_remove is empty, the operation is invalid too
        if to_remove not in self.qll or not self.qll[to_remove]:
            return -1
        # Let l be the list of blocks of the size to_remove
        l = self.qll[to_remove]
        # Let aux be one of that blocks (we know that at least one exists, otherwise the list would be empty
        # Take it out of the list
        aux = l.pop()
        # If after taking aux out of l, it becomes empty, it must be removed from the structure
        if not l:
            del self.qll[to_remove]

        # Calculate the block size that have to be returned back to the structure (the payback)
        block_size = to_remove - alloc_size
        # By convention, all the blocks are allocated at the beginning of block in witch it fits.
        # That is the Large_Block is the concatenation ((Allocated_Block)(Returned_Block))
        #   So the final address of the block been returned is the final position of the original block
        position1 = aux[1]
        #   So the initial address is the final position subtracted by the size of this block being returned
        position0 = position1 - block_size
        #   Therefore the block to be returned is:
        new_block = (position0, position1)

        # Asserts the block is valid
        if block_size < 0:
            return -1

        self.insert_block(block_size, new_block)

        return aux[0]

    """
        Find the first list in the structure with blocks of size grater or equal to the size being allocated
            alloc_size: size being allocated.
    """

    def first_fit(self, alloc_size):
        self.time = 0
        to_remove = alloc_size
        # If alloc_size is in the structure calls fit method defined above with alloc_size = to_remove as parameters
        for q in self.qll:
            # Counts an operation of access in the structure due to the iterator q
            self.time += 1
            # If alloc_size "fits" inside a blocks with size to_remove
            if q >= alloc_size:
                to_remove = q
                break
        # Calls fit function to fit alloc_size in to_remove
        return self.fit(to_remove, alloc_size)

    """
        Find the best list in the structure with blocks of size grater or equal to alloc_size.
        Here best list means the list with the least size greater or equal to alloc_size.
            alloc_size: size being allocated.
    """

    def best_fit(self, alloc_size):
        self.time = 0
        # To find the minimum size, min_size starts with a bigger value than it can have, self.size + 1
        min_size = self.size + 1

        for q in self.qll:
            # Counts an operation of access in the structure due to the iterator q
            self.time += 1
            # If q is less than the min_size and still containing alloc_size
            if alloc_size <= q < min_size:
                min_size = q
        # Calls fit function to fit alloc_size in min_size
        return self.fit(min_size, alloc_size)

    """
        Find the worst list in the structure with blocks of size grater or equal to alloc_size.
        Here worst list means the list with the greater size.
            alloc_size: size being allocated.
    """

    def worst_fit(self, alloc_size):
        self.time = 0
        # To find the maximum size, max_size starts with the smallest value it can have, alloc_size
        max_size = alloc_size

        for q in self.qll:
            # Counts an operation of access in the structure due to the iterator q
            self.time += 1
            # If max_size is not the max_size ...
            if q > max_size:
                # ... updates the max_size
                max_size = q

        return self.fit(max_size, alloc_size)

    """
        Release a a block of memory
        add_begin: Is the initial address of the block being released
        size: Is the size being released
    """

    def free(self, add_start, size):
        # Starts to count the virtual time
        self.time = 0
        # Defines the end address of the block being released for convenience
        add_end = add_start + size
        # Declares variables to contain left and right neighbors to merge
        l_neigh, r_neigh = None, None
        # Mark variables to be removed
        to_delete = [None] * 2
        # Counts the number of neighbors found (it can only have two)
        cont = 0
        # For each block of each list
        for q in self.qll:
            for block in self.qll[q]:
                # Counts an access operation
                self.time += 1
                # If end of inserting and start of a generic block coincides ...
                if add_end == block[0]:
                    # ... that means the generic is the right neighbor of the inserting block
                    r_neigh = block
                    # Let l be the list containing the size of this block
                    l = self.qll[q]
                    # We remove this block from the structure because there'll be a merge
                    l.remove(block)
                    # If the list becomes empty we mark it to be removed
                    if not l:
                        to_delete[0] = q

                    cont += 1

                # If end of generic and start of a inserting block coincides ...
                if block[1] == add_start:
                    # ... that means the generic is the right neighbor of the inserting block
                    l_neigh = block
                    # Let l be the list containing the size of this block
                    l = self.qll[q]
                    # We remove this block from the structure because there'll be a merge
                    l.remove(block)
                    # If the list becomes empty we mark it to be removed
                    if not l:
                        to_delete[1] = q

                    cont += 1
                # If counter reaches two, it means two neighbors have already been found
                if cont == 2:
                    break

        # Remove the lists marked to be removed
        for i in range(0, 2):
            self.time += 1
            if to_delete[i]:
                del self.qll[to_delete[i]]

        # If there is a left neighbor ...
        if l_neigh:
            # ... The start address to be inserted should be the the stating address of the left neighbor
            add_start = l_neigh[0]
        # If there is a right neighbor ...
        if r_neigh:
            # ... The end address to be inserted should be the the end address of the left neighbor
            add_end = r_neigh[1]

        # Recalculate the size that is going to be inserted
        block_size = add_end - add_start

        # Asserts if it is a valid size
        if block_size < 0:
            return -1

        # Insert the block released in the structure
        self.insert_block(block_size, (add_start, add_end))
