import csv, glob, os


def files_from_dir(dir_path, extension):
  pattern = f'{dir_path}/*.{extension}'
  return [
      path
      for path in glob.glob(pattern)
  ]


def csv_headers(path):
    with open(path) as file:
        csv_reader = csv.reader(file)
        return next(csv_reader)
