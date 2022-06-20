from sklearn.naive_bayes import ComplementNB

from ic.models.common import main


CLASSES = [
    'BENIGN', 'Heartbleed', 'DDoS', 'Web Attack  Sql Injection',
    'Infiltration', 'Web Attack  XSS', 'SSH-Patator', 'DoS slowloris',
    'Web Attack  Brute Force', 'PortScan', 'DoS GoldenEye', 'Bot',
    'DoS Slowhttptest', 'FTP-Patator', 'DoS Hulk'
]

def process_row(row):
  y = [CLASSES.index(row[-1])]
  x = [ float(val) for val in
        [ row[5], *row[7:72], *row[73:-1] ]
      ]
  return (x, y)


if __name__ == "__main__":
    main(ComplementNB(), range(len(CLASSES)), process_row)
