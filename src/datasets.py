import numpy as np
from sklearn.model_selection import KFold, train_test_split

# listed of trained models to stack - each references results stored in files
# named inferences/%s_{train,test}.txt, each of which may contain multiple
# columns for different hyperparameters
TRAINED_MODELS = [
    'adaboost',
    'adaboost_n373_lr1',
    'adaboost_n374_lr1',
    'knn_2',
    'knn_4',
    'knn_8',
    'knn_16',
    'knn_32',
    'knn_64',
    'knn_128',
    'knn_256',
    'knn_512',
    'knn_1024',
    'rf',
    'rf2',
    'rf3',
    'rf_md144_mss80',
    'ffm',
    'vw_logistic',
    'vw_logistic_nn5',
    'xgb',
    'xgb2',
    'lr',
    'lr2',
    'et',
    'nn',
    'nn2',
    'nn3',
]

# instantiating this here so that we can share the same random seed everywhere
KF_SEEDED = KFold(n_splits=4, shuffle=True, random_state=212)

def load_data(holdout=0.1):
    """Load provided training and test data from files.

    Returns numpy arrays X_train, y_train, X_test.

    """
    training_data = np.loadtxt('../data/training_data.txt', skiprows=1)
    X_test = np.loadtxt('../data/test_data.txt', skiprows=1)
    X_train = training_data[:,1:]
    y_train = training_data[:,0]
    X_train, X_holdout, y_train, y_holdout = train_test_split(
        X_train, y_train, test_size=holdout, random_state=100)
    return X_train, y_train, X_test, X_holdout, y_holdout


def load_models(models=TRAINED_MODELS):
    """Load training results from specified models.

    Models should be strings that match values available in TRAINED_MODELS.

    Returns aggregated numpy arrays containing a column for each model:
        X_meta_train, X_meta_test

    """
    # NB: knn models have multiple columns of results for different distance metrics, so we just
    # use the last column (bray curtis) which performed the best
    X_meta_train = np.hstack([
        np.loadtxt(f'../inferences/{m}_train.txt', ndmin=2)[:,-1:] for m in models])
    X_meta_test = np.hstack([
        np.loadtxt(f'../inferences/{m}_test.txt', ndmin=2)[:,-1:] for m in models])
    return X_meta_train, X_meta_test
