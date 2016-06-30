from BitMap import *
from LinkedList import *
from QuickFit import *
from BuddySystem import *
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
     qb = QuickFit(size)
     qw = QuickFit(size)
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
          print(qb)
          print(qw)
     elif ch == 'bs':
          print(bs)

     print('operacao,','begbf,','begbn,',"begbb,","begbw,","begqf,","begqb,","begqw,","size,","id,","bftime,","bntime,","bbtime,","bwtime,","lftime,","lntime,","lbtime,","lwtime,","qftime,","qbtime,","qwtime,","bstime")
     on_memory = [] # indicates processes on memory
     for i in range(it):
          # random choice is free memory
          if(ran.random() > 0.5 and on_memory):
               out = on_memory[ran.randint(0,len(on_memory) - 1)]

               if ch == 'time':
                    times = "free" + 21 * ",{:d}"
                    print(times.format(new.begbf,new.begbn,new.begbb,new.begbw,new.begqf,new.begqb,new.begqw,new.size,new.id,bf.time,bn.time,bb.time,bw.time,lf.time,ln.time,lb.time,lw.time,qf.time,qb.time,qw.time,bs.time))
               elif ch == 'bf':
                    print("free: id",out.id,"beg:",out.begbf,"size:", out.size)
               elif ch == 'bn':
                    print("free: id",out.id,"beg:",out.begbn,"size:", out.size)
               elif ch == 'bb':
                    print("free: id",out.id,"beg:",out.begbb,"size:", out.size)
               elif ch == 'bw':
                    print("free: id",out.id,"beg:",out.begbw,"size:", out.size)
               elif ch == 'qf':
                    print("free: id",out.id,"beg:",out.begqf,"size:", out.size)
                    print("free: id",out.id,"beg:",out.begqb,"size:", out.size)
                    print("free: id",out.id,"beg:",out.begqw,"size:", out.size)
               else:
                    print("free: id",out.id,"size:", out.size)

               if out.begbf >= 0:
                    bf.free(out.begbf,out.size)
               if out.begbn >= 0:
                    bn.free(out.begbn,out.size)
               if out.begbb >= 0:
                    bb.free(out.begbb,out.size)
               if out.begbf >= 0:
                    bw.free(out.begbw,out.size)
               lf.free(out.id)
               ln.free(out.id)
               lb.free(out.id)
               lw.free(out.id)
               if out.begqf != -1:
                    qf.free(out.begqf, out.size)
               if out.begqb != -1:
                    qb.free(out.begqb, out.size)
               if out.begqw != -1:
                    qw.free(out.begqw, out.size)
               bs.free(out.id)
               on_memory.remove(out)

          # random choice is allocate memory
          else:
               alloc_size = ran.randint(0,20)
               new = Process(alloc_size)
               new.begbf = bf.first_fit(new.size)
               new.begbn = bn.next_fit(new.size)
               new.begbb = bb.best_fit(new.size)
               new.begbw = bw.worst_fit(new.size)
               lf.first_fit(new.id, new.size)
               ln.next_fit(new.id, new.size)
               lb.best_fit(new.id, new.size)
               lw.worst_fit(new.id, new.size)
               new.begqf = qf.first_fit(new.size)
               new.begqb = qb.best_fit(new.size)
               new.begqw = qw.worst_fit(new.size)
               bs.buddy_system(new.id, new.size)
               on_memory.append(new)

               if ch == 'time':
                    times = "alloc" + 21 * ",{:d}"
                    print(times.format(new.begbf,new.begbn,new.begbb,new.begbw,new.begqf,new.begqb,new.begqw,new.size,new.id,bf.time,bn.time,bb.time,bw.time,lf.time,ln.time,lb.time,lw.time,qf.time,qb.time,qw.time,bs.time))
               elif ch == 'bf':
                    print("alloc: id",new.id,"beg:",new.begbf,"size:", new.size)
               elif ch == 'bn':
                    print("alloc: id",new.id,"beg:",new.begbn,"size:", new.size)
               elif ch == 'bb':
                    print("alloc: id",new.id,"beg:",new.begbb,"size:", new.size)
               elif ch == 'bw':
                    print("alloc: id",new.id,"beg:",new.begbw,"size:", new.size)
               elif ch == 'qf':
                    print("alloc: id",new.id,"beg:",new.begqf,"size:", new.size)
                    print("alloc: id",new.id,"beg:",new.begqb,"size:", new.size)
                    print("alloc: id",new.id,"beg:",new.begqw,"size:", new.size)
               else:
                    print("alloc: id",new.id,"size:", new.size)

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
               print(qb)
               print(qw)
          elif ch == 'bs':
               print(bs)
