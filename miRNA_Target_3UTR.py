import sys
import re

#############################################################################################
#################################### SUB PROGRAM ############################################
#############################################################################################
def filter_results(temp):
    Flag = 0
    D = int(temp[5]) - int(temp[4]) + 1
    if D == int(temp[3]) and float(temp[2]) == 100:
        Flag = 1

    return Flag

def check_strand(temp):
    if int(temp[6]) < int(temp[7]):
        R1 = int(temp[6])
        R2 = int(temp[7])
    else:
        R1 = int(temp[7])
        R2 = int(temp[6])
    
    return R1,R2

def check_positions_1(temp,GFF3,miRNA_Target):
    Chr = temp[1]
    R1,R2 = check_strand(temp)
    #start_previous = R1; end_previous = R2
    M = 0; N = 0
    for i in GFF3[Chr]:
        for j in GFF3[Chr][i]:
            print j
            """
            if i != "match_part":
                temp1 = j.split("-")
                if R1 >= int(temp1[0]) and R2 <= int(temp1[1]):
                    if i == "mRNA" or i == "gene":
                        t1 = temp1[2].split(";")[0]
                        ID = t1.replace("ID=","")
                    else:
                        ID = temp1[2].replace("Parent=","")
                    M = 1
                    if i == "three_prime_UTR":
                        start,end = check_strand(temp)
                        if miRNA_Target.has_key(temp[0]):
                            miRNA_ID = temp[0] + "_" + str(miRNA_Target[temp[0]])
                            miRNA_Target[temp[0]] += 1
                        else:
                            miRNA_Target[temp[0]] = 1
                            miRNA_ID = temp[0]
                        
                        #if start_previous == start and end_previous == end:
                        #    N = 1
                        #else:
                        #    N = 0
                            
                        #start_previous = start; end_previous = end
                        txt = Chr + "\t" + "Salmon" + "\t" + "miRNA_Target" + "\t" + str(start) + "\t" + str(end) + "\t.\t+\t.\t" + "ID=" + miRNA_ID + ";Name=" + miRNA_ID
                        
                        #print txt
                        #print R1,R2
                        #print temp1
                        #print temp1[0],temp1[1]
                        #sys.exit()
                        
            """
    #if M == 0:
    #    print temp[0],"\t",Chr,"\t","Inter-genic"
    sys.exit()
    return 0

########################################################################################
# This Function takes only file with 3 Prime UTR
# Compares only with one Transcript
########################################################################################
def check_positions(temp,GFF3,miRNA_Target):
    Chr = temp[1]
    R1,R2 = check_strand(temp)
    M = 0; N = 0
    for i in GFF3[Chr]:
        for j in GFF3[Chr][i]:
                temp1 = j.split("-")
                if R1 >= int(temp1[0]) and R2 <= int(temp1[1]):
                        ID = temp1[2].replace("Parent=","")
            
                        start,end = check_strand(temp)
                        if miRNA_Target.has_key(temp[0]):
                            miRNA_ID = temp[0] + "_" + str(miRNA_Target[temp[0]])
                            miRNA_Target[temp[0]] += 1
                        else:
                            miRNA_Target[temp[0]] = 1
                            miRNA_ID = temp[0]
                        
                        txt = Chr + "\t" + "Salmon" + "\t" + "miRNA_Target" + "\t" + str(start) + "\t" + str(end) + "\t.\t+\t.\t" + "ID=" + miRNA_ID + ";Name=" + miRNA_ID
                        print txt
                        break
    #if M == 0:     
    #    print temp[0],"\t",Chr,"\t","Inter-genic"
    
    return 0


############################################################################################
###################### Storing only the 3 Prime UTR Regions from GFF3 file #################
############################################################################################
def store_GFF3_data(data):
    GFF3 = {}
    for i in data:
        temp = i.split()
        #if temp[2] != "sequence_assembly":
        if temp[2] == "three_prime_UTR":
            if GFF3.has_key(temp[0]):
                # Check for CDS
                if GFF3[temp[0]].has_key(temp[2]):
                    R = str(temp[3]) + "-" + str(temp[4]) + "-" + str(temp[8])
                    GFF3[temp[0]][temp[2]].append(R)
                else:
                    R = str(temp[3]) + "-" + str(temp[4]) + "-" + str(temp[8])
                    GFF3[temp[0]][temp[2]] = [R]
                    
            else:
                R = str(temp[3]) + "-" + str(temp[4]) + "-" + str(temp[8])
                GFF3[temp[0]] = {temp[2]: [R]}
                
    return GFF3

############################################################################################
################################ MAIN PROGRAM ##############################################
############################################################################################
# Latest GFF3 File 
GFF3_1 = open("/mnt/users/jeevka/Make_GFF3_For_GBrowse/Salmon_3p6_Chr_051214.gff3","r")
#GFF3_1 = open("Test.gff3","r")
GFF3 = GFF3_1.readlines()
del GFF3[0]

GFF3 = store_GFF3_data(GFF3)
miRNA_Target = {}

# BLAST output file from miRNAA target sequences
miRNA = open("BLAST_miRNA_Targets_Results.out","r")

for i in miRNA:
    temp = i.split()
    # Filter
    Flag = filter_results(temp)
    
    if Flag == 1 and GFF3.has_key(temp[1]):
            check_positions(temp,GFF3,miRNA_Target)