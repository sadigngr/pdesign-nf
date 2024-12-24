'''
primer3 run etmek için clustalw çıktı dosyalarındaki '-' işaretini kaldırarak yeni listeler oluşturur. sonra primer3 e uygun input formatında her çıktı için yeni input dosyası oluşturur.
'''

import sys
import os

def process_clustal_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    seq1 = []
    seq2 = []
 
    for line in lines:
        line = line.strip()
        if line.startswith("sequence_from_file1"):
            seq1.append(line.split()[1])
        elif line.startswith("sequence_from_file2"):
            seq2.append(line.split()[1])

    seq1_str = "".join(seq1).replace("-", "")
    seq2_str = "".join(seq2).replace("-", "")
    
    return seq1_str, seq2_str

def process_files_in_directory(directory_path):
    # Klasördeki tüm dosyaları al
    files = [file for file in sys.argv[1:]]
    
    for file_name in files:
        file_path = os.path.join(file_name)
        
        # Dosya olup olmadığını kontrol et
        if os.path.isfile(file_path):
            # seq1 ve seq2 için çıktı dosyalarının yolları
            seq1_output_file_path = os.path.join(f"{os.path.splitext(file_name)[0]}_seq1.txt")
            seq2_output_file_path = os.path.join(f"{os.path.splitext(file_name)[0]}_seq2.txt")

            # Dosyayı işle
            seq1, seq2 = process_clustal_file(file_path)

            # seq1 çıktısını dosyaya yaz
            with open(seq1_output_file_path, 'w') as seq1_output_file:
                seq1_output_file.write(f"SEQUENCE_ID={file_path}\n")
                seq1_output_file.write(f"SEQUENCE_TEMPLATE={seq1}\n")
                seq1_output_file.write("PRIMER_OUTPUT_FORMAT=0\n")
                seq1_output_file.write("PRIMER_TASK=generic\n")
                seq1_output_file.write("PRIMER_PRODUCT_SIZE_RANGE=150-200\n")
                seq1_output_file.write("PRIMER_EXPLORATORY=1\n")
                seq1_output_file.write("=" + "\n")
            
            # seq2 çıktısını dosyaya yaz
            with open(seq2_output_file_path, 'w') as seq2_output_file:
                seq2_output_file.write(f"SEQUENCE_ID={file_path}\n")
                seq2_output_file.write(f"SEQUENCE_TEMPLATE={seq2}\n")
                seq2_output_file.write("PRIMER_OUTPUT_FORMAT=0\n")
                seq2_output_file.write("PRIMER_TASK=generic\n")
                seq2_output_file.write("PRIMER_PRODUCT_SIZE_RANGE=150-200\n")
                seq2_output_file.write("PRIMER_EXPLORATORY=1\n")
                seq2_output_file.write("=" + "\n")
'''
primer3 input file format için bu şekilde düzenlenmiştir.
'''
# Fonksiyonları çalıştır

if __name__ == "__main__":
    directory_path = sys.argv[1]
    process_files_in_directory(directory_path)
