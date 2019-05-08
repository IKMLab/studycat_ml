"""For exploring distributions in the data."""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sml import util


def acc_over_time(data, days=7):
    """Visualize the evolution of mean accuracy and std over time."""
    accs = []
    times = []
    current_bin = []
    current_timestamp = None
    for x in sorted(data, key=lambda x: x['timestamp']):
        if current_timestamp is None:
            current_timestamp = x['timestamp']
        current_bin.append(x['accuracy'])
        if util.day_diff(current_timestamp, x['timestamp']) > days:
            accs.append(np.mean(current_bin))
            times.append(util.to_str(current_timestamp))
            current_bin = []
            current_timestamp = None
    plt.figure(figsize=(14, 4))
    plt.plot(range(len(accs)), accs)
    plt.xticks(list(range(len(times))), times)
    plt.xlabel('time')
    plt.ylabel('mean accuracy')
    plt.title('Evolution of mean accuracy over time')
    plt.show()


def correlation(data, x, y):
    """View the correlation between two features via a scatterplot."""
    plt.scatter(
        [d[x] for d in data],
        [d[y] for d in data])
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title('Correlation between %s and %s' % (x, y))
    plt.show()


def dist(data, attr):
    """View the distribution of a vector of values."""
    sns.distplot([x[attr] for x in data])
    plt.xlabel(attr)
    plt.ylabel('density')
    plt.show()


def mean_accs(data, attr):
    """Visualize the distribution of mean accuracies over users.

    Args:
      data: List of dicts, must be filtered just to have accuracies.
      attr: String. The feature of interest - e.g. user, teacher, school.
    """
    accs = {}
    for x in data:
        if x[attr] not in accs.keys():
            accs[x[attr]] = []
        accs[x[attr]].append(x['accuracy'])
    sns.distplot([np.mean(v) for v in accs.values()])
    plt.xlabel('mean accuracy')
    plt.ylabel('density')
    plt.show()
