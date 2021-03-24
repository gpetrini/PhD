#!/usr/bin/env python3
# input file
fin = open("used_figures.txt", "rt")
# output file to write the result to
fout = open("out.txt", "wt")
# for each line in the input file
for line in fin:
    line = line.split("{")[1]
    line = line.split("}")[0] + "\n"
    fout.write(line)

fin.close()
fout.close()
