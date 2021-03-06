# lab06.py
# build part of the datapath of a single-cycle 32 bit MIPS processor (non-pipelined)

import pyrtl

def alu (rs, rt, sh, funct):
    """
        Implementation of R-Type operation ALU:
        funct decides operation 
        can do: ADD, SUB, AND, OR, XOR, SLL, SRL, SRA, and SLT
    """
    # Operation 0: a and b
    ADD = rs + rt
    SUB = rs - rt
    AND = rs & rt
    OR = rs | rt
    XOR = rs ^ rt
    SLL = pyrtl.shift_left_logical(rt,sh) # shifts use rt, sh = shift amnt
    SRL = pyrtl.shift_right_logical(rt,sh)
    SRA = pyrtl.shift_right_arithmetic(rt,sh)
    SLT = pyrtl.signed_lt(rs,rt)  # set less than (rd = rs<rt? 1:0)

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
        with funct == 0x00:
            alu_output |= SLL
        with funct == 0x02:
            alu_output |= SRL 
        with funct == 0x03:
            alu_output |= SRA
        with funct == 0x2a:
            alu_output |= SLT

    return alu_output


# instruction input
instr = pyrtl.Input(bitwidth=32, name='instr')

# decode instruction (only R-type)
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
data0 = pyrtl.WireVector(32, 'data01')  # rf outputs
data1 = pyrtl.WireVector(32, 'data02')


# wire input/output ports from rf
data0 <<= rf[rs]  # data0 = the value of rs register in rf
data1 <<= rf[rt]
alu_out = pyrtl.WireVector(32, 'alu_out')  # for alu output
alu_out <<= alu(data0, data1, sh, funct)  # connect alu function results to alu output wire
rf[rd] <<= alu_out  # value of rd destination register = alu output

# simulate processor
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
sim.step({ 'instr' : 0x014B4820 }) 
sim_trace.render_trace()
