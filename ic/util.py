import csv, glob, os

from IPython.display import  HTML


CSV_FILE_NAMES = [
  'Monday-WorkingHours.pcap_ISCX.csv',
  'Tuesday-WorkingHours.pcap_ISCX.csv',
  'Wednesday-workingHours.pcap_ISCX.csv',
  'Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv',
  'Friday-WorkingHours-Morning.pcap_ISCX.csv',
  'Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv',
  'Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv',
]

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


def basename(file_path):
    base_path, _ = os.path.splitext(file_path)
    return os.path.basename(base_path)

  
def h(i, text):
    return HTML(f'<h{i}>{text}</h{i}>')


HR = HTML('<hr/>')
