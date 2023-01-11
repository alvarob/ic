import csv, functools, math, os, operator, sys

import pandas as pd
import numpy as np

from ic import util


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


def problem_filter(chunk, columns):
    checks = [ (chunk[c] < 0) | pd.isna(chunk[c]) | (chunk[c].abs() == math.inf) for c in columns ]
    return functools.reduce(operator.or_, checks)


def strip_column_names(dataframe):
    return dataframe.rename(columns=lambda c: c.strip())


def remove_init_win_columns(dataframe):
    return dataframe.drop(['Init_Win_bytes_forward', 'Init_Win_bytes_backward'], axis=1)


def remove_duplicate_fwd_header_length(dataframe):
    return dataframe.drop('Fwd Header Length.1', axis=1)


def transform_dataframe(dataframe, transformations):
    return functools.reduce(lambda x, f: f(x), transformations, dataframe)


def apply_numeric_label(dataframe):
    new_df = dataframe
    new_df['Label'] = new_df['Label'].transform(lambda x: int(x != 'BENIGN'))
    return new_df


def remove_problem_rows(dataframe):
    all_but_label = dataframe.columns.tolist()[:-1]
    new_df = dataframe[~problem_filter(dataframe, all_but_label)]
    return new_df


def cleaned_up_chunks(in_file_path, chunksize=1000):
    chunks = pd.read_csv(in_file_path, chunksize=chunksize)

    for chunk in chunks:
        yield transform_dataframe(chunk, [
            strip_column_names,
            remove_init_win_columns,
            remove_duplicate_fwd_header_length,
            apply_numeric_label,
            remove_problem_rows
        ])


class WarmUpBuilder():
    def __init__(self, columns, n_classes=2, n_samples=500):
        self.dataframe = pd.DataFrame(columns=columns)
        self.leftover = pd.DataFrame(columns=columns)
        self.counts = [ 0 for _ in range(n_classes) ]
        self.n_samples = n_samples

    def is_done(self):
        return all([ x >= self.n_samples for x in self.counts ])

    def add_row(self, row):
        if self.is_done():
            self.leftover = self.leftover.append(row)
            return

        label = int(row[-1])
        if self.counts[label] < self.n_samples:
            self.dataframe = self.dataframe.append(row)
            self.counts[label] += 1

    def process_chunk(self, chunk):
        for _, row in chunk.iterrows():
            self.add_row(row)

    def dataframes(self):
        for int_field in ['Destination Port', 'Label']:
            self.dataframe[int_field] = self.dataframe[int_field].astype(int)
            self.leftover[int_field] = self.leftover[int_field].astype(int)

        return (self.dataframe, self.leftover)


def preprocess_with_warmup(in_file_path, out_file_dir, suffix="processed"):
    out_file = f'{out_file_dir}/{util.basename(in_file_path)}.{suffix}.csv'
    chunks = cleaned_up_chunks(in_file_path)
    chunk = next(chunks)
    warm_up_builder = WarmUpBuilder(chunk.columns.tolist())

    while not warm_up_builder.is_done():
        warm_up_builder.process_chunk(chunk)
        try:
            chunk = next(chunks)
        except StopIteration:
            break

    if not warm_up_builder.is_done():
        raise RuntimeError("Não existem dados suficientes para preprocessar gerando o warmup: "+in_file_path)

    df, leftover = warm_up_builder.dataframes()
    df.to_csv(out_file, mode="w", header=True, index=False)
    leftover.to_csv(out_file, mode="a", header=False, index=False)

    for chunk in chunks:
        chunk.to_csv(out_file, mode="a", header=False, index=False)

def preprocess_and_join(in_files, out_file):
    first = True

    for file in in_files:
        chunks = cleaned_up_chunks(file)

        for chunk in chunks:
            mode = 'w' if first else 'a'
            chunk.to_csv(out_file, mode=mode, header=first, index=False)
            first = False


def main():
    in_files = sys.argv[1:]
    preprocess(in_files)

if __name__ == "__main__":
    main()
