import sys
import re

F1 = open("BLAST_Results.out","r")

for i in F1:
    temp = i.split()
    if int(temp[7]) < int(temp[6]):
        start = temp[7]
        end = temp[6]
        strand = "-"
    else:
        start = temp[6]
        end = temp[7]
        strand = "+"
        
    hit_length = int(temp[5]) - int(temp[4]) + 1
    if float(temp[2]) == 100 and hit_length == int(temp[3]):
        txt = temp[1] + "\t" + "Salmon" + "\t" + "miRNA" + "\t" + str(start) + "\t" + str(end) + "\t.\t" + strand + "\t.\t" + "ID=" + temp[0] + ";Name=" + temp[0]
        print txt