"""
zberman2, chansky2, based off of VishnuC's classifier
Python program which trains a RandomForestClassifier on the given training data
and uses it to make predictions for the given test data. A spreadsheet of
predictions is written to submission.gz.
"""
import os
import numpy as np
import gzip
from csv import reader, writer
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

import six

# Decide read/write mode based on python version
read_mode, write_mode = ('r','w') if six.PY2 else ('rt','wt')  #vishnu

# Decide zip based on python version (vishnu)
if six.PY2:
    from itertools import izip
    zp = izip
else:
    zp = zip

"""
Function which takes in the label file and returns a list of labels
"""
def load_labels(flabel):
    print('loading started')
    # Lets read labels first as things are not sorted in files
    labels = {}
    with open(flabel) as f:
        next(f)    # Ignoring header
        for row in reader(f):
            labels[row[0]] = int(row[1])
    print('labels loaded')
    return labels

"""
Set up a RandomForestClassifier according to set parameters
"""
def classifier():
    # Parameters for Randomforest
    n_jobs = -1
    verbose = 2
    depth = 12
    features = "log2"
    est = 50
    boot = false
    clf = RandomForestClassifier(n_jobs=n_jobs, max_depth=depth, max_features=features, n_estimators=est, bootstrap=boot, verbose = verbose)
    return clf

"""
Takes in a list of labels and the file with training data.
RandomForestClassifier created, which is trained and returned
"""
def train(labels, ftrain):
    # Dimensions for train set
    ntrain = 10868
    nfeature = 16**2 + 1 + 1 # For two_byte_codes, no_que_marks, label
    train = np.zeros((ntrain, nfeature), dtype = int)
    with gzip.open(ftrain, read_mode) as f:
        next(f)    # Ignoring header
        print(f)
        for t,row in enumerate(reader(f)):
            train[t,:-1] = map(int, row[1:]) if six.PY2 else list(map(int, row[1:]))
            train[t,-1] = labels[row[0]]
            if(t+1)%1000==0:
                print(t+1, 'records loaded')
    print('training set loaded')
    del labels
    
    clf = classifier()
    # Start training
    print('training started')
    clf.fit(train[:,:-1], train[:,-1])
    print('training completed')
    # We don't need training set now
    del train
    return clf

"""
Given the test data, and our RandomForestClassifier from before,
this function classifies test data and returns the predictions
"""
def test(clf, ftest):
    # Dimensions for train set
    ntest = 10873
    nfeature = 16**2 + 1 # For two_byte_codes, no_que_marks
    test = np.zeros((ntest, nfeature), dtype = int)
    Ids = []    # Required test set ids

    with gzip.open(ftest, read_mode) as f:
        next(f)    # Ignoring header
        for t,row in enumerate(reader(f)):
            test[t,:] = map(int, row[1:]) if six.PY2 else list(map(int, row[1:]))
            Ids.append(row[0])
            if(t+1)%1000==0:
                print(t+1, 'records loaded')
    print('test set loaded')
    # Predict for whole test set
    return clf.predict_proba(test)

"""
Given the predictions recorded by our classifier, and the submission
file, this function writes the prediction to a spreadsheet, and returns it.
"""
def write_submission(y_pred, fsubmission):
    # Writing results to file
    with gzip.open(fsubmission, write_mode) as f:
        fw = writer(f)
        # Header preparation
        header = ['Id'] + ['Prediction'+str(i) for i in range(1,10)]
        fw.writerow(header)
        for t, (Id, pred) in enumerate(zp(Ids, y_pred.tolist())):
            fw.writerow([Id]+pred)
            if(t+1)%1000==0:
                print(t+1, 'prediction written')

#change dir for convenience of paths sake
path = '/Users/benchansky/Desktop/460_malware_project/'
os.chdir(path)
ftrain = 'train_converted.gz'
ftest = 'test_converted.gz'
flabel = 'trainLabels.csv'
fsubmission = 'submission.gz'

# list labels
labels = load_labels(flabel)
# train classifier
clf = train(labels, ftrain)
# use classifier to make predictions
y_pred = test(clf, ftest)
# record predictions
write_submission(y_pred, fsubmission)