# instr_dec.py 
# instruction decoder: combinatorial logic block
# input: MIPS 32-bit instruction
# sets up processor control blocks

import pyrtl

# instantiate a memory block storing sample instructions (32-bit each)
# reads one instruction per cycle
sample_instructions = [201326592, 286326786, 4202528, 2366177284]
mem = pyrtl.RomBlock(bitwidth=32, addrwidth=2, romdata=sample_instructions, max_read_ports=1)

# variable counter will serve as an address in this example 
counter = pyrtl.Register(bitwidth=2)
counter.next <<= counter + 1

# read data stored in rom
data = pyrtl.WireVector(bitwidth=32, name='data')
data <<= mem[counter]

# output data
op = pyrtl.Output(bitwidth=6, name='op')
rs = pyrtl.Output(bitwidth=5, name='rs')
rt = pyrtl.Output(bitwidth=5, name='rt')
rd = pyrtl.Output(bitwidth=5, name='rd')
sh = pyrtl.Output(bitwidth=5, name='sh')
func = pyrtl.Output(bitwidth=6, name='func')
imm = pyrtl.Output(bitwidth=16, name='imm')  # for I-type 
addr = pyrtl.Output(bitwidth=26, name='addr')  # for J-type instruct

### ADD YOUR INSTRUCTION DECODE LOGIC HERE ###
# R-Type: op(6), rs(5), rt(5), rd(5), shamt(5), funct(6)
# I-Type: op(6), rs(5), rt(5), immed(16)
# J-Type: op(6), addr(26)
# find opcode first to determine which type of instruction

func <<= data[:6]
sh <<= data[6:11]
rd <<= data[11:16]
rt <<= data[16:21]
rs <<= data[21:26]
op <<= data[26:]
addr <<= data[:26]
imm <<= data[:16]


# simulate
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(4):
    sim.step({})
sim_trace.render_trace(symbol_len=20, segment_size=1)
