import os, random, sys

def split(
        in_file_path,
        out_train_path,
        out_test_path,
        train_percentage
        ):
    with open(in_file_path, 'r', errors='ignore') as in_file, open(out_train_path, 'w') as train_file, open(out_test_path, 'w') as test_file:
        header = in_file.readline()
        train_file.writelines((header))
        test_file.writelines((header))

        for line in in_file:
            if random.random() <= train_percentage:
                train_file.writelines((line))
            else:
                test_file.writelines((line))

                
def split_with_suffix(
        in_file_path,
        train_percentage,
        train_suffix="train",
        test_suffix="test"
):
    base_name, _ = os.path.splitext(in_file_path)
    train_out_path = base_name + "." + train_suffix + ".csv"
    test_out_path = base_name + "." + test_suffix + ".csv"
    split(in_file_path, train_out_path, test_out_path, train_percentage)

    
def main():
    in_file = sys.argv[1]
    train_file = sys.argv[2]
    test_file = sys.argv[3]
    percentage = float(sys.argv[4])
    split(in_file, train_file, test_file, percentage)

if __name__ == "__main__":
    main()      
        
