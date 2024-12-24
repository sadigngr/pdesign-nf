import os
import sys


def writePrimers(outPath,dirPath):
    primer = []
    output_file_path = f"primer3_result_{outPath}"

    for file_name in sys.argv[2:]:
        file_path = os.path.join(file_name)
        
        with open(file_path, "r") as files:
            for line in files:
                line = line.strip()  
                if (line.startswith("SEQUENCE_ID=") or \
                   (line.startswith("PRIMER_LEFT_") and "_SEQUENCE" in line) or \
                   (line.startswith("PRIMER_RIGHT_") and "_SEQUENCE" in line)):
                    primer.append(line)


    with open(output_file_path, "w") as output_file:
        for line in primer:
            output_file.write(line + "\n")

    print(f"Primerler {output_file_path} dosyasına yazıldı.")


if __name__ == "__main__":
    writePrimers(sys.argv[1],sys.argv[2])
