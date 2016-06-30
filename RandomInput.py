from BitMap import *
from LinkedList import *
from QuickFit import *
from BuddySystem import *
import random as ran

class Process:

     """ Representation of a Process. """
     
     id = 1
     # Size is the number of blocks. 
     def __init__(self, size):
          self.id = Process.id
          Process.id += 1
          self.size = size
          
def test(size, it, ch):

     """ Test of memory management algorithms.
         size: total size of the memory (in number of blocks).
         it: number of operations (insert, delete memory).
         ch: chose type of information to be display. """

     # Create structures
     bf = BitMap(size) # Bit Map for use of fist fit
     bn = BitMap(size) # Bit Map for use of next fit
     bb = BitMap(size) # Bit Map for use of best fit
     bw = BitMap(size) # Bit Map for use of worst fit
     lf = LinkedList(size) # Linked List for use of fist fit
     ln = LinkedList(size) # Linked List for use of next fit
     lb = LinkedList(size) # Linked List for use of best fit
     lw = LinkedList(size) # Linked List for use of worst fit
     qf = QuickFit(size) # Adapted quick fit using fist fit
     qb = QuickFit(size) # Adapted quick fit using best fit
     qw = QuickFit(size) # Adapted quick fit using worst fit
     bs = BuddySystem(size) # Tree for Buddy System

     # Initial information for specific algorithms
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

     # Segmentation table header
     if ch == 'seg':
          print("operacao,bfblock,bnblock,bbblock,bwblock,lfblock,lnblock,lbblock,lwblock,qfblock,qbblock,qwblock,bsblock,bfspaces,bnspaces,bbspaces,bwspaces,lfspaces,lnspaces,lbspaces,lwspaces,qfspaces,qbspaces,qwspaces,bsspaces")
     # Time table header
     if ch == 'time':
          print('operacao,','begbf,','begbn,',"begbb,","begbw,","begqf,","begqb,","begqw,","size,","id,","bftime,","bntime,","bbtime,","bwtime,","lftime,","lntime,","lbtime,","lwtime,","qftime,","qbtime,","qwtime,","bstime")

     on_memory = [] # indicates processes on memory
     for i in range(it):

        # random choice is free memory
        if(ran.random() > 0.5 and on_memory):
               # Chose random process to free from memory
               out = on_memory[ran.randint(0,len(on_memory) - 1)]

               # Row of a time table
               if ch == 'time':
                    times = "free" + 21 * ",{:d}"
                    print(times.format(new.begbf,new.begbn,new.begbb,new.begbw,new.begqf,new.begqb,new.begqw,new.size,new.id,bf.time,bn.time,bb.time,bw.time,lf.time,ln.time,lb.time,lw.time,qf.time,qb.time,qw.time,bs.time))

               # Information for specific algorithms
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
               elif ch == "bs":
                    print("free: id",out.id,"size:", out.size)

               # free memory in all structures where this process is allocate
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

               # Remove process from process list
               on_memory.remove(out)

               # Row of a segmentation table
               if ch == 'seg':
                    (bfblock,bfspaces) = bf.segmentation()
                    (bnblock,bnspaces) = bn.segmentation()
                    (bbblock,bbspaces) = bb.segmentation()
                    (bwblock,bwspaces) = bw.segmentation()
                    (lfblock,lfspaces) = lf.segmentation()
                    (lnblock,lnspaces) = ln.segmentation()
                    (lbblock,lbspaces) = lb.segmentation()
                    (lwblock,lwspaces) = lw.segmentation()
                    (qfblock,qfspaces) = qf.segmentation()
                    (qbblock,qbspaces) = qb.segmentation()
                    (qwblock,qwspaces) = qw.segmentation()
                    (bsblock,bsspaces) = bs.segmentation()
                    print("free",",",bfblock,",",bnblock,",",bbblock,",",bwblock,",",lfblock,",",lnblock,",",lbblock,",",lwblock,",",qfblock,",",qbblock,",",qwblock,",",bsblock,",",bfspaces,",",bnspaces,",",bbspaces,",",bwspaces,",",lfspaces,",",lnspaces,",",lbspaces,",",lwspaces,",",qfspaces,",",qbspaces,",",qwspaces,",",bsspaces)

        # random choice is allocate memory
        else:
               # Chose random size to be allocate
               alloc_size = ran.randint(0,20)
               # Create new Process representation
               new = Process(alloc_size)

               # Allocate process memory using all the algorithms
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

               # Add new process to the list of process
               on_memory.append(new)

               # Row of a time table
               if ch == 'time':
                    times = "alloc" + 21 * ",{:d}"
                    print(times.format(new.begbf,new.begbn,new.begbb,new.begbw,new.begqf,new.begqb,new.begqw,new.size,new.id,bf.time,bn.time,bb.time,bw.time,lf.time,ln.time,lb.time,lw.time,qf.time,qb.time,qw.time,bs.time))

               # Information for specific algorithms
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
               elif ch == "bs":
                    print("alloc: id",new.id,"size:", new.size)

               # Row of a segmentation table
               if ch == 'seg':
                    (bfblock,bfspaces) = bf.segmentation()
                    (bnblock,bnspaces) = bn.segmentation()
                    (bbblock,bbspaces) = bb.segmentation()
                    (bwblock,bwspaces) = bw.segmentation()
                    (lfblock,lfspaces) = lf.segmentation()
                    (lnblock,lnspaces) = ln.segmentation()
                    (lbblock,lbspaces) = lb.segmentation()
                    (lwblock,lwspaces) = lw.segmentation()
                    (qfblock,qfspaces) = qf.segmentation()
                    (qbblock,qbspaces) = qb.segmentation()
                    (qwblock,qwspaces) = qw.segmentation()
                    (bsblock,bsspaces) = bs.segmentation()
                    print("alloc",",",bfblock,",",bnblock,",",bbblock,",",bwblock,",",lfblock,",",lnblock,",",lbblock,",",lwblock,",",qfblock,",",qbblock,",",qwblock,",",bfspaces,",",bnspaces,",",bbspaces,",",bwspaces,",",lfspaces,",",lnspaces,",",lbspaces,",",lwspaces,",",qfspaces,",",qbspaces,",",qwspaces)

        # state of structure after each operation for specific algorithms
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

