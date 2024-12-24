import subprocess
import sys
import os

chr1 = sys.argv[1]
chr2 = sys.argv[2]
parsedLocs = sys.argv[3]

def _write(path,sequences):
    with open(path,"w") as file:
        for header, (sequence,start,end) in sequences.items():
            file.write(f">{header} (start: {start}, end: {end})\n")
            for i in range(0,len(sequence),60):
                file.write(f"{sequence[i:i+60]}\n") 

with open(chr1,"r") as f:
    buff = f.read().replace("\n","")

with open(chr2,"r") as f1:
    buff1 = f1.read().replace("\n","")

with open(parsedLocs,"r") as f2:
    f2.readline()
    while True:
        loc = f2.readline().replace("\n","")
        if loc:
            i = loc.split(" ") 
            s1 = int(i[0])
            e1 = int(i[1])
            s2 = int(i[2])
            e2 = int(i[3])
            seq1 = buff[s1-1:e1-1]
            seq2 = buff1[s2-1:e2-1]
            result_sequences = {
                "sequence_from_file1" : (seq1,s1,e1),
                "sequence_from_file2" : (seq2,s2,e2)
            }
            
            _write("result.fa",result_sequences)
            
            outFile = f"{s1}_{e1}_{s2}_{e2}.aln"
            subprocess.call(["clustalw","-infile=result.fa",f"-outfile={outFile}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT) 
        else:
            break
 
