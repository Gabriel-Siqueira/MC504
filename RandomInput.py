from MemMan import *
import random as ran

class Process:
     id = 1
     def __init__(self, size):
          self.id = Process.id
          Process.id += 1
          self.size = size
          
def test(size, it, ch):

     """ Test of memory management algorithms.
         size: total size of the memory.
         it: number of operations (insert, delete memory). """
     
     bf = BitMap(size)
     bn = BitMap(size)
     bb = BitMap(size)
     bw = BitMap(size)
     lf = LinkedList(size)
     ln = LinkedList(size)
     lb = LinkedList(size)
     lw = LinkedList(size)
     qf = QuickFit(size)
     bs = BuddySystem(size)

     if ch == 'bf':
          print(bf)
     elif ch == 'bn':
          print(bn)
     elif ch == 'bb':
          print(bb)
     elif ch == 'bw':
          print(bw)
     elif ch == 'lf':
          print(lf)
     elif ch == 'ln':
          print(ln)
     elif ch == 'lb':
          print(lb)
     elif ch == 'lw':
          print(lw)
     elif ch == 'qf':
          print(qf)
     elif ch == 'bs':
          print(bs)

     
     on_memory = [] # indicates processes on memory
     for i in range(it):
          # random choice is free memory
          if(ran.random() > 0.5 and on_memory != []):
               out = on_memory[ran.randint(len(on_memory))]

               if ch == 'bf':
                    print("free: id",out.id,"beg:",out.begbf,"size:", out.size)
               elif ch == 'bn':
                    print("free: id",out.id,"beg:",out.begbn,"size:", out.size)
               elif ch == 'bb':
                    print("free: id",out.id,"beg:",out.begbb,"size:", out.size)
               elif ch == 'bw':
                    print("free: id",out.id,"beg:",out.begbw,"size:", out.size)
               elif ch == 'qf':
                    print("free: id",out.id,"beg:",out.begqf,"size:", out.size)
               else:
                    print("free: id",out.id,"size:", out.size)

               bf.free(out.begbbf,out.size)
               bn.free(out.begbbn,out.size)
               bb.free(out.begbbb,out.size)
               bw.free(out.begbbw,out.size)
               lf.free(out.id)
               ln.free(out.id)
               lb.free(out.id)
               lw.free(out.id)
               qf.free(out.begqf, out.size)
               bs.free(self.id)
               on_memory.remove(out)

          # random choice is allocate memory
          else:
               alloc_size = ran.randint(0,size)
               new = Process(alloc_size)
               new.begbf = bf.first_fit(new.size)
               new.begbn = bn.next_fit(new.size)
               new.begbb = bb.best_fit(new.size)
               new.begbw = bw.worst_fit(new.size)
               lf.first_fit(new.id, new.size)
               ln.next_fit(new.id, new.size)
               lb.best_fit(new.id, new.size)
               lw.worst_fit(new.id, new.size)
               new.begqf = qf.quick_fit(new.size)
               bs.buddy_system(new.id, new.size)

               if ch == 'bf':
                    print("create: id",new.id,"beg:",new.begbf,"size:", new.size)
               elif ch == 'bn':
                    print("create: id",new.id,"beg:",new.begbn,"size:", new.size)
               elif ch == 'bb':
                    print("create: id",new.id,"beg:",new.begbb,"size:", new.size)
               elif ch == 'bw':
                    print("create: id",new.id,"beg:",new.begbw,"size:", new.size)
               elif ch == 'qf':
                    print("create: id",new.id,"beg:",new.begqf,"size:", new.size)
               else:
                    print("create: id",new.id,"size:", new.size)

          if ch == 'bf':
               print(bf)
          elif ch == 'bn':
               print(bn)
          elif ch == 'bb':
               print(bb)
          elif ch == 'bw':
               print(bw)
          elif ch == 'lf':
               print(lf)
          elif ch == 'ln':
               print(ln)
          elif ch == 'lb':
               print(lb)
          elif ch == 'lw':
               print(lw)
          elif ch == 'qf':
               print(qf)
          elif ch == 'bs':
               print(bs)
