import subprocess
import sys
import os

from Utilities.locs import findLocs

from Primers.autoprimer1 import process_files_in_directory
from Primers.autoprimer2 import run_primer3_on_files
from Primers.primer2 import writePrimers
from Primers.primermatch4 import MatchPrimers

helpPage = """

Help sayfasi.

"""

def read_fasta(file_path):
    sequences = {} ##header ve sequnce saklanir.
    with open(file_path, 'r') as file:
        header = None
        sequence = []
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                if header:
                    sequences[header] = ''.join(sequence)
                header = line[1:]
                sequence = []
            else:
                sequence.append(line)
        if header:
            sequences[header] = ''.join(sequence)
    return sequences ## fasta dosyasindaki tum basliklari ve dizileri iceren sequences dict dondurulur

def extract_sequence(sequence, start, end):
    start -= 1 ## 1 tabanlı indeksi 0 tabanli indekse donusum yapilir
    end -= 1
    subseq = sequence[start:end + 1] # son indeksi dahil etmek icin +1 eklenir
    return subseq, start + 1, end + 1  

def write_fasta(file_path, sequences):
    with open(file_path, 'w') as file:
        for header, (sequence, start, end) in sequences.items():
            file.write(f">{header} (start: {start}, end: {end})\n")
            for i in range(0, len(sequence), 60):
                file.write(f"{sequence[i:i+60]}\n")

def Extract(fasta_file1,start1,end1,fasta_file2,start2,end2):
    
    # Read FASTA files
    fasta_data1 = read_fasta(fasta_file1)
    fasta_data2 = read_fasta(fasta_file2)
    
    # Extract sequences
    first_sequence1 = next(iter(fasta_data1.values()))
    subsequence1, start1_adj, end1_adj = extract_sequence(first_sequence1, start1, end1)
    
    first_sequence2 = next(iter(fasta_data2.values()))
    subsequence2, start2_adj, end2_adj = extract_sequence(first_sequence2, start2, end2)
    
    # Prepare results
    result_sequences = {
        "sequence_from_file1": (subsequence1, start1_adj, end1_adj),
        "sequence_from_file2": (subsequence2, start2_adj, end2_adj)
    }
    
    # Write results to file
    write_fasta("./tmpData/result.fa", result_sequences)
    print("Results written to result.fa")


FASTA_PATH_1,FASTA_PATH_2 = None,None

def main():
    print(sys.argv)
    for l,arg in enumerate(sys.argv):

        if arg == "-h" or "--help" and len(sys.argv) == 2:
            print(helpPage)

        elif arg == "--seqFiles":
            print(l,arg)
            FASTA_PATH_1 = sys.argv[l+1]
            FASTA_PATH_2 = sys.argv[l+2]
    subprocess.call(["mkdir","tmpData"])
    subprocess.call(["mkdir","seq1"])
    subprocess.call(["mkdir","seq2"])
    currentDir = "./tmpData"
    subprocess.call(["nucmer","--coords",FASTA_PATH_1,FASTA_PATH_2],cwd=".")
    
    locList = findLocs(f"./out.coords")
    for i in locList:
        start1 = int(i[0][0])
        end1 = int(i[0][1])
        start2 = int(i[1][0])
        end2 = int(i[1][1])
        Extract(FASTA_PATH_1,start1,end1,FASTA_PATH_2,start2,end2)
        outFile = f"{start1}_{end1}_{start2}_{end2}.aln"
        subprocess.call(["clustalw","-infile=result.fa",f"-outfile={outFile}"],cwd = currentDir)
    process_files_in_directory(currentDir)
    subprocess.call(["mv","*seq1_output.txt"],["../seq1"],cwd = currentDir)
    subprocess.call(["mv","*seq2_output.txt"],["../seq2"],cwd = currentDir)
    run_primer3_on_files("./seq1")
    run_primer3_on_files("./seq2")
    writePrimers("./seq1","seq1.txt")
    writePrimers("./seq2","seq2.txt")
    MatchPrimers("seq1.txt","seq2.txt")
      





