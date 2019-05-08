"""Code for reproducing the baselines."""
from sklearn import metrics, linear_model, svm
import numpy as np
from sml import exp_data as ex


def eval_linear_regression(X_train, y_train, X_test, y_test):
    model = linear_model.LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = metrics.mean_squared_error(y_pred, y_test)
    print('Linear regression gives RMSE of %s' % np.sqrt(mse))


def eval_mean_acc(data):
    mean_acc = np.mean([x['accuracy'] for x in data if x['subset'] == 'train'])
    y_pred = [mean_acc] * 10000
    y_test = [x['accuracy'] for x in data if x['subset'] == 'test']
    mse = metrics.mean_squared_error(y_test, y_pred)
    print('Predicting with mean acc in training set yields '
          '%s rmse on the test set.' % np.sqrt(mse))


def eval_svr(X_train, y_train, X_test, y_test):
    model = svm.SVR()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = metrics.mean_squared_error(y_pred, y_test)
    print('SVR gives RMSE of %s' % np.sqrt(mse))


def get_X_y(data):
    """Get the design matrix and response vector for the baseline models.

    The design matrix is composed of a concatenation of one-hot vectors for each
    of the independent variables we have chosen, being
      - teacher
      - class
      - level
      - unit_module
    """
    n_teachers = max([x['teacher'] for x in data]) + 1
    n_classes = max([x['class'] for x in data]) + 1
    n_levels = max([x['level'] for x in data]) + 1
    n_modules = max([x['unit_module'] for x in data]) + 1
    n_feats = n_teachers + n_classes + n_levels + n_modules
    X = np.zeros((len(data), n_feats + 1))
    y = np.array([x['accuracy'] for x in data])
    print('Generating one-hot vectors')
    for ix, x in enumerate(data):
        teacher_ix = x['teacher']
        class_ix = n_teachers + x['class']
        level_ix = n_teachers + n_classes - 1 + x['level']
        module_ix = n_teachers + n_classes + n_levels - 2 + x['unit_module']
        X[ix, 0] = 1  # bias term - also why not subtracting 1 for class_ix
        X[ix, teacher_ix] = 1
        X[ix, class_ix] = 1
        X[ix, level_ix] = 1
        X[ix, module_ix] = 1

    # splits
    print('Determining splits...')
    train_ixs = [ix for ix, x in enumerate(data) if x['subset'] == 'train']
    val_ixs = [ix for ix, x in enumerate(data) if x['subset'] == 'val']
    test_ixs = [ix for ix, x in enumerate(data) if x['subset'] == 'test']

    X_train = X[train_ixs, :]
    y_train = y[train_ixs]
    X_val = X[val_ixs, :]
    y_val = y[val_ixs]
    X_test = X[test_ixs, :]
    y_test = y[test_ixs]

    print('Ready to go.')

    return X_train, y_train, X_val, y_val, X_test, y_test
