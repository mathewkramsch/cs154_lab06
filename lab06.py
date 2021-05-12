# lab06.py

# build part of the datapath of a single-cycle 32 bit MIPS processor (non-pipelined)
# ALU instructs: ADD, SUB, AND, OR, XOR, SLL, SRL, SRA, and SLT (R-Type)
# Register file: 32 rigisters, use PyRTL MemBlock to implement
    # name it rf
    # make it ascessible from the class level
# Input: instruction fed through, named instr

import pyrtl
