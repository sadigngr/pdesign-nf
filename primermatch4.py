import sys


def extract_primer_left_with_ids(filename):
    primer_left_values = {}  # Dizi ve sequence ID'lerini saklayacağımız sözlük
    sequence_id = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()  # Satırı temizle
            if line.startswith("SEQUENCE_ID"):  # Sequence ID'sini al
                sequence_id = line.split('=')[-1].strip()
            elif line.startswith("PRIMER_LEFT"):  # PRIMER_LEFT dizisini al
                # '=' sembolünden sonrasını al
                value = line.split('=')[-1].strip()
                # Dizi ve en yakın sequence ID'yi sakla
                if value not in primer_left_values:
                    primer_left_values[value] = sequence_id

    return primer_left_values

def MatchPrimers(file1,file2):
    # Dosya isimlerini buraya girin
    #file1 = 'primer3_seq1.txt'
    #file2 = 'primer3_seq2.txt'

    # Her iki dosyadan değerleri al
    values1 = extract_primer_left_with_ids(file1)
    values2 = extract_primer_left_with_ids(file2)

    # Ortak değerleri bul
    common_values = set(values1.keys()).intersection(set(values2.keys()))

    # Sonuçları listele
    print("Sequences and sequence IDs found in both files::")
    for value in common_values:
        id1 = values1[value]
        
        print(f"{value} | Sequence ID : {id1} | ")
        print("-"*80)

if __name__ == "__main__":
    MatchPrimers(sys.argv[1],sys.argv[2])
