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
rf = pyrtl.MemBlock(32, addrwidth=32, name='rf', max_read_ports=2, max_write_ports=4, asynchronous=False, block=None)

# rf inputs
r_reg0 = pyrtl.WireVector(5, 'r_reg0')  # read source register name
r_reg1 = pyrtl.WireVector(5, 'r_reg1')  # read target register name
w_reg = pyrtl.WireVector(32, 'w_reg')  # write to register
w_data = pyrtl.WireVector(5, 'w_data')  # write data

# rf outputs
data0 = pyrtl.WireVector(32, 'data01')
data1 = pyrtl.WireVector(32, 'data02')

# wire inputs from decoder
r_reg0 <<= rs
r_reg1 <<= rt
w_reg <<= rd

# make alu
alu_out = pyrtl.WireVector(32, 'alu_out')

# wire input ports to rf
rf[rs] <<= r_reg0
rf[rt] <<= r_reg1
rf[rd] <<= w_reg
rf[alu_out] <<= w_data

# wire write output ports from rf
data0 <<= rf[rs]
data1 <<= rf[rt]

# ALU
def alu (a, b, sh, funct):
    """
        Implementation of R-Type operation ALU:
        funct decides operation 
        can do: ADD, SUB, AND, OR, XOR, SLL, SRL, SRA, and SLT
    """
    # Operation 0: a and b
    ADD = a + b
    SUB = a - b
    AND = a & b
    OR = a | b
    XOR = a ^ b
    #SLL = 
    #SRL = 
    #SRA = 
    #SLT = 

    alu_output = pyrtl.WireVector(32)  # output
    
    with pyrtl.conditional_assignment:
        with funct == 0x20:
            alu_output |= ADD
        with funct == 0x22:
            alu_output |= SUB
        with funct == 0x24:
            alu_output |= AND
        with funct == 0x25:
            alu_output |= OR
        with funct == 0x26:
            alu_output|= XOR
    #    with funct == 0x00:
    #        alu_output |= SLL
    #    with funct == 0x02:
    #        alu_output |= SRL 
    #    with funct == 0x03:
    #        alu_output |= SRA
    #    with funct == 0x2a:
    #        alu_output |= SLT

    return alu_output

# Call the above-defined "alu" function and connect its results to the block's output ports 
alu_out <<= alu(data0, data1, sh, funct)
w_data <<= alu_out

# simulate processor
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
sim.step({ 'instr' : 0x014B4820 }) 
sim_trace.render_trace()

""" TODO: 
- implement alu shift operations
"""
