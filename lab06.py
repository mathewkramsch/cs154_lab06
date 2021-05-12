# lab06.py

# build part of the datapath of a single-cycle 32 bit MIPS processor (non-pipelined)
# ALU instructs: ADD, SUB, AND, OR, XOR, SLL, SRL, SRA, and SLT (R-Type)
# Register file: 32 rigisters, use PyRTL MemBlock to implement
    # name it rf
    # make it ascessible from the class level
# Input: instruction fed through, named instr

# instr -> Decoder -> rf -> ALU

import pyrtl

# instruction input
instr = pyrtl.Input(bitwidth=32, name='instr')

# decoder (only R-type)
rs = pyrtl.WireVector(bitwidth=5, name='rs')
rt = pyrtl.WireVector(bitwidth=5, name='rt')
rd = pyrtl.WireVector(bitwidth=5, name='rd')
sh = pyrtl.WireVector(bitwidth=5, name='sh')
funct = pyrtl.WireVector(bitwidth=6, name='func')

funct <<= instr[:6]
sh <<= instr[6:11]
rd <<= instr[11:16]
rt <<= instr[16:21]
rs <<= instr[21:26]

# register file
rf = pyrtl.MemBlock(bitwidth=32, addrwidth=2, name='rf', max_read_ports=2, max_write_ports=1, asychronous=False, block=None)

# rf inputs
r_reg0 = WireVector(5, 'r_reg0')  # read source register name
r_reg1 = WireVector(5, 'r_reg1')  # read target register name
w_reg = WireVector(32, 'w_reg')  # write to register
w_data = WireVector(5, 'w_data')  # write data

# rf outputs
data01 = WireVector(32, 'data01')
data02 = WireVector(32, 'data02')

# wire inputs from decoder
r_reg0 <<= rs
r_reg1 <<= rt
w_reg <<= rd

# wire input ports to rf
rf <<= r_reg0
rf <<= r_reg1
rf <<= w_reg
rf <<= w_data

# wire write output ports from rf
data01 <<= rf
data02 <<= rf

# ALU

