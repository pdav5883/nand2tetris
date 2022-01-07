import sys
import os
import re

# symbol table is a dict with keys equal to symbol string and values equal to symbol address
default_st = {}

for i in range(16):
    default_st["R" + str(i)] = i

default_st["SCREEN"] = 16384
default_st["KBD"] = 24576
default_st["SP"] = 0
default_st["LCL"] = 1
default_st["ARG"] = 2
default_st["THIS"] = 3
default_st["THAT"] = 4

dest_table = {None:"000", "M":"001", "D":"010", "DM":"011",
              "A":"100", "AM":"101", "AD":"110", "ADM":"111",
              "MD":"011", "MA":"101", "DA":"110", "AMD":"111",
              "DAM":"111", "DMA":"111", "MAD":"111", "MDA":"111"}
comp_table = {"0"  :"0101010",
              "1"  :"0111111",
              "-1" :"0111010",
              "D"  :"0001100",
              "A"  :"0110000", "M"  :"1110000",
              "!D" :"0001101",
              "!A" :"0110001", "!M" :"1110001",
              "-D" :"0001111",
              "-A" :"0110011", "-M" :"1110011",
              "D+1":"0011111",
              "A+1":"0110111", "M+1":"1110111",
              "D-1":"0001110",
              "A-1":"0110010", "M-1":"1110010",
              "D+A":"0000010", "D+M":"1000010",
              "D-A":"0010011", "D-M":"1010011",
              "A-D":"0000111", "M-D":"1000111",
              "D&A":"0000000", "D&M":"1000000",
              "D|A":"0010101", "D|M":"1010101"}
jump_table = {None:"000", "JGT":"001", "JEQ":"010", "JGE":"011",
              "JLT":"100", "JNE":"101", "JLE":"110", "JMP":"111"}


def assemble(inpath):
    """
    Goes line by line, keeps track of symbol table, parses line, generates code for line, writes to file
    """
    st = dict(default_st)
    
    parselist = []
    curr_rom = 0

    # read input file and first pass to remove comments and add labels
    with open(inpath, "r") as fin:
        for linestr in fin:
            linedata = parse(linestr)
            
            if linedata[0] is "comment":
                pass

            elif linedata[0] is "label":
                st[linedata[1]] = curr_rom

            else:
                parselist.append(linedata)
                curr_rom += 1

    # second pass to generate code for each instruction line
    codelist = []
    next_ram = 16

    for linedata in parselist:
        # replace symbols, adding new ones to st
        if linedata[0] is "a_instruction_symbol":
            if linedata[1] not in st:
                st[linedata[1]] = next_ram
                next_ram += 1

            linedata = "a_instruction", st[linedata[1]]

        codelist.append(code(linedata))

    # write binary code lines to output file
    with open(os.path.splitext(inpath)[0] + ".hack", "w") as fout:
        for codestr in codelist:
            fout.write(codestr + "\n")


def parse(linestr):
    """
    Return tuple of (linetype, data) where data depends on type:
    comment: None
    label: symbol
    a_instruction: value
    a_instruction_symbol: symbol
    c_instruction: dest, comp, jump
    """
    # removing leading/trailing whitespace/newline
    linestr = "".join(linestr.split())

    # remove comment
    comment_match = re.search("//.*", linestr)
    if comment_match:
        linestr = linestr[:comment_match.start()]

    if not linestr:
        return "comment",

    elif linestr[0] == "(":
        return "label", linestr[1:-1]

    elif linestr[0] == "@":
        if linestr[1].isdigit():
            return "a_instruction", int(linestr[1:])
        else:
            return "a_instruction_symbol", linestr[1:]

    # c instruction -- always has comp, may have dest, jump
    else:
        equal_match = re.search("=", linestr)
        if equal_match:
            dest = linestr[:equal_match.start()]
            linestr = linestr[equal_match.start()+1:]
        else:
            dest = None

        semicolon_match = re.search(";", linestr)
        if semicolon_match:
            jump = linestr[semicolon_match.start()+1:]
            linestr = linestr[:semicolon_match.start()]
        else:
            jump = None

        comp = linestr

        return "c_instruction", dest, comp, jump


def code(linedata):
    """
    Returns the binary string representation of the parsed line data

    Only a/c instruction get passed in
    """
    if linedata[0] is "a_instruction":
        return "0" + format(linedata[1], "015b")

    elif linedata[0] is "c_instruction":
        return "111" + comp_table[linedata[2]] + dest_table[linedata[1]] + jump_table[linedata[3]]


if __name__ == "__main__":
    assemble(sys.argv[1])

