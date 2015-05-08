CS 460 Spring 2015 Final Project
Microsoft Malware Classification Challenge
-------------------------------------------------------------------------------
Ben Chansky (chansky2@illinois.edu)
Zack Berman (zberman2@illinois.edu)
-------------------------------------------------------------------------------
We chose to participate in the Microsoft Malware Classification Challenge
(Big 2015) for our semester project.  The full description for the challenge 
can be found at the following link:
https://www.kaggle.com/c/malware-classification

In general, the idea of the challenge was to train a classifier on training
data, consisting of 9 different families of malware.  Once trained, one must
use this classifier to make predictions on the classifications of test malware.
The winner of the challenge was the one who correctly predicted the most files
in the test set.

In order to run our code, one must first download the test and train data from
the following link: https://www.kaggle.com/c/malware-classification/data
Once downloaded, the .byte files from train.7z and test.7z must be extracted
and then converted to .byte.gz format.  This step can be very time intensive.

Once the data is formatted properly, one can move onto the core of our project.
Our project consists of 2 python files, byte_summarizer.py and
make_predictions.py.  The purpose of byte_summarizer.py is to read through all
the .byte.gz files from the test and training data, and extract critical
features from the malware.  This new information is then passed along to new 
files which will be used in make_predictions.py.  The job of 
make_predictions.py is to train a RandomForestClassifier on the training data, 
and then use the classifier to classify each file in the test data.  A 
submission file is then written, which can be submitted to the challenge 
website.

With the data formatted properly and the directories within each python file
set, run the following commands:
python byte_summarizer.py
python make_predictions.py

Ultimately, we did not finish in time to make a submission by the deadline of
the challenge, but we were able to submit late and see what our score was.
After tuning the RandomForestClassifier by toggling its parameters, we were
able to achieve a logarithmic loss (calculation shown here: 
https://www.kaggle.com/c/malware-classification/details/evaluation)
of only 0.109146517.