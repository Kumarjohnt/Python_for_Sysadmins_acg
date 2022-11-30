## command line interpreter

import argparse

##### defining user interface for CLI #####

## build the parser

parser = argparse.ArgumentParser(description='Read a file in reverse')
parser.add_argument('filename',help='the file to read')
parser.add_argument('--limit', '-l',type=int, help='Number of lines to read' )
parser.add_argument('--version', '-v', action='version', version='%(prog)s 1.0' )

#####################################################

## parse the arguments
args = parser.parse_args()
# print(args)

#####################################################

##### Defining actual logic ######

## read the file, reverse contents and print.

with open(args.filename) as f:
    lines = f.readlines()
    lines.reverse()

    if args.limit:
        lines = lines[:args.limit]
    
    for line in lines:
        print(line.strip()[::-1]) ## reverse the line. 



