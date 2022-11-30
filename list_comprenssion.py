import subprocess

import argparse

parser = argparse.ArgumentParser(description='Search for words including partial word')
parser.add_argument('snippet', help='partial (or complete) string to search for in words')

args = parser.parse_args()
snippet = args.snippet.lower()

with open('words.txt') as f:
    words = f.readlines()

# matches = []

# for word in words:
#     if snippet in word.lower():
#         matches.append(word)

# above code is replced with list comprehension


matches = [ word.strip() for word in words if snippet in word.lower() ] # strip will remove the \n or white spaces.
print(matches)
