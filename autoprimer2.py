'''
autoprimer1 ile oluşan input dosyalarını oto şekilde primer3 run eder subprocess
'''



import os
import subprocess
import sys

def run_primer3_on_files(directory_path):
    # Klasördeki tüm dosyaları al
    for file_name in sys.argv[1:]:
        file_path = os.path.join(file_name)
        
        # Dosya olup olmadığını kontrol et
        if os.path.isfile(file_path):
            # Dosya adından uzantıyı ayır
            base_name, _ = os.path.splitext(file_name)
            
            # Primer3 için output dosya yolu
            output_file_path = os.path.join(f"{base_name}_output.txt")
            
            # primer3_core komutunu çalıştır
            with open(file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
                subprocess.run(['primer3_core'], stdin=input_file, stdout=output_file)


if __name__ == "__main__":
# Doğrudan komut satırından dizin yolunu al
    directory_path = sys.argv[1]
    run_primer3_on_files(directory_path)
