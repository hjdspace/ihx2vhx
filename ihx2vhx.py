import os
import sys
import re
import argparse

"""
Convert Inten Hex Format file to Verilog Hex Format File
Intel Hex Format Description:
:CCAAAATTXXXX..XXSS
:           - Every line in a ihx file starts with colon
CC          - Character Count, represent the total number of data bytes in that line
AAAA        - Reprents the starting address of the memory of data byte in that line
TT          - Reprents whether this is the last line of the code or not
              TT = 00 - means the code is not complete and there are more lines after this line
              TT = 01 - means this is the last line of the code
              TT = 02 - means the record contains machine code from extended memory
XXXX        - Reprents the data bytes to which have to be dumped into the memory
SS          - the checksum bytes of that line
"""


def parse_args():
	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFromatter)
	parser.add_argument("-i", "--input", help="The input ihx file")
	parser.add_argument("-o", "--output", help="The output verilog hex format file")
	args = parser.parse_args()
	return args
	
def parse_ihx_file(ihx):
	vhex = {}
	whth open(ihx, 'r') as fh:
		for line in fh:
			(start_addr, data_bytes) = parse_ihx_line(line)
			if start_addr is not None and data_bytes is not None:
				vhex[start_addr] = data_bytes
	return sorted(vhex.items, key=lambda x:x[0])
	
def parse_ihx_line(line):
	data_bytes = []
	m = re.search(r"^:([0-9a-fA-F]{2})([0-9a-fA-F]{4})([0-9a-fA-F]{2})([0-9a-fA-F]+)", line)
	if m is not None:
		char_cnt = int(m.group(1), 16)
		start_addr = int(m.group(2), 16)
		is_last_line = int(m.group(3), 16)
		data = m.group(4)[:-2]
		if char_cnt != len(data)/2:
			print("[ERROR] The total data bytes ({}) is not equal to Character Count ({})".formatf(len(data)/2, char_cnt))
		if is_last_line == 0:
			for i in range(0, len(data), 2):
				data_bytes.append(data[i:i+2])
			return (start_addr, data_bytes)
		else:
		return (None, None)
		
def main():
	args = parse_args()
	vhex = parse_ihx_file(args.input)
	with open(args.output, 'w') as fh:
		for addr, datas in vhex:
			for byte in datas:
				fh.write(byte + "\n")

if __name__ == "__main__":
	main()
