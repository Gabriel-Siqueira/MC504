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
		second = False;
		
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
	
	mem_list = []

	def __init__(self, total_mem):
		self.mem_list.append(MemBlock(0, total_mem))
	
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


