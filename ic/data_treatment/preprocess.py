import csv, math, os, sys


def should_ignore(row):
    values = [ row[5], *row[7:-1] ]
    for v in values:
        try:
            float_value = float(v)
            if float_value < 0 or math.fabs(float_value) == math.inf or float_value == math.nan:
                return True
        except:
            return True

    return False
    
    
def preprocess(file_paths, suffix='processed'):
    for file_path in file_paths:
        print("Processando arquivo", file_path)

        base_name, _ = os.path.splitext(file_path)
        out_path = base_name + "." + suffix + ".csv"
        
        with open(file_path, errors='ignore') as in_file, open(out_path, 'w') as processed_file:
            csv_reader = csv.reader(in_file)
            header = in_file.readline()
            processed_file.writelines((header))
            
            ignored = 0
            total = 0

            for row in csv_reader:
                total += 1
                ignore_row = should_ignore(row)
                ignored += int(ignore_row)

                if not ignore_row:
                    line = ','.join(row)+"\n"
                    processed_file.writelines((line))

            print("Arquivo processado, resultado em", out_path)
            print("Total de linhas:", total, ", ignoradas:", ignored, "(", ignored*100/total, "% )\n")

def main():
    in_files = sys.argv[1:]
    preprocess(in_files)

if __name__ == "__main__":
    main()

                
