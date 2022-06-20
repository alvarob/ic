import sys

def group(in_file_paths, out_file_path):
    add_header = True

    with open(out_file_path, 'w') as out_file:
        for file_path in in_file_paths:
            with open(file_path, 'r', errors="ignore") as in_file:
                header = in_file.readline()

                if add_header:
                    out_file.writelines((header))
                    add_header = False

                for line in in_file:
                    out_file.writelines((line))

def main():
    in_files = sys.argv[1:-1]
    out_file = sys.argv[-1]
    print(in_files, out_file)
    group(in_files, out_file)

if __name__ == "__main__":
    main()
