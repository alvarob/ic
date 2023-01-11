import pandas as pd
import matplotlib.pyplot as plt

from ic.util import h, HR

def line_chart(dataframes, metric):
    return pd.concat([
        df[[metric]].rename(columns={metric: algorithm}) for (algorithm, df) in dataframes.items()
    ], axis=1)


def bar_chart(dataframes, metrics):
    return pd.concat([
        pd.DataFrame({ algorithm: df.iloc[-1] }) for (algorithm, df) in dataframes.items()
    ], axis=1).loc[metrics].transpose()


def all_charts(dataframes, metrics):
    line_charts = dict([
      (metric, line_chart(dataframes, metric)) for metric in metrics
    ])
    return (line_charts, bar_chart(dataframes, metrics))


def show_report(file_name, algorithms, metrics, figsize=(16, 8)):
    file_name_template = f'$BASE_PATH$/{file_name}.pcap_ISCX.processed.$ALGORITHM$.metrics.csv'
    dataframes = dict([
      (algorithm, pd.read_csv(
          file_name_template.replace(
            '$ALGORITHM$', algorithm
          ).replace(
            '$BASE_PATH$', base_path
          ),
          index_col='step'
      )) for [base_path, algorithm] in algorithms
    ])

    lines, bar = all_charts(dataframes, metrics)

    display(h(1, file_name))

    for metric in metrics:
        display(h(2, metric))
        lines[metric].plot.line(figsize=figsize)
        plt.show()

    bar.plot.bar(figsize=figsize)
    plt.show()

    display(HR)
