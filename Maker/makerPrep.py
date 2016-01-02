#!/usr/bin/python3
# Toni Westbrook (anthonyw@wildcats.unh.edu)
# Fixup headers in FASTA for CEGMA run

import os
import argparse

argParser = argparse.ArgumentParser( description="Fixup headers in FASTA for CEGMA run")
argParser.add_argument('--fasta', default="", help="FASTA file to fix")
argParser.add_argument('--output', default="", help="Output file")

#--------------------------- Main --------------------------------------
# Parse arguments
args = argParser.parse_args()

inputHandle = open(args.fasta, 'r')
outputHandle = open(args.output, 'w')

seqID = 1
        
for inputLine in inputHandle:
    if inputLine[0] == '>':
        outputHandle.write(">SEQ{0}\n".format(seqID))
        seqID += 1
    else:
        outputHandle.write("{0}".format(inputLine))
        
inputHandle.close()
outputHandle.close()
