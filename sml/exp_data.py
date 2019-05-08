"""Basic operations on the data."""
import json
import random
from tqdm import tqdm
from sml import util


def load(just_accs=False):
    file_name = 'acc_data.json' if just_accs else 'data.json'
    with open(file_name) as f:
        return json.loads(f.read())


def filter_accs(data):
    """Filters out just the records with accuracies."""
    return [x for x in data if 'accuracy' in x.keys()]


def splits(data):
    """Determine the train, val, test split and mark the records."""
    random.seed(42)
    ixs = list(range(len(data)))
    val_test_ixs = random.sample(ixs, 20000)
    val_ixs = random.sample(val_test_ixs, 10000)
    with tqdm(total=len(data)) as pbar:
        for ix, x in enumerate(data):
            if ix not in val_test_ixs:
                x['subset'] = 'train'
            elif ix in val_ixs:
                x['subset'] = 'val'
            else:  # must be test
                x['subset'] = 'test'
            pbar.update()
    with open('acc_data.json', 'w') as f:
        f.write(json.dumps(data, cls=util.DecimalEncoder))
