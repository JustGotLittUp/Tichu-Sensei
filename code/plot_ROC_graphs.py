
import os
import numpy as nm
import matplotlib.pylab as mpl
import sklearn.metrics as mtrcs


## hardcoded c, gamma, and threshold values were calculated in other files and are the values for which the models return the optimal results.

Dir = os.path.normpath(r'INSERT YOUR PATH HERE')
os.chdir(Dir)

c_estimator = 8.3022
true_positive_rate_list = list()
false_positive_rate_list = list()
resultList_LR = list()
bestThresholdResultsList_LR = list()
with open(r'SVRTestPlayerCalls.data') as results:
    for line in results:
        resultList_LR.append(int(line))
    thresholdArray = nm.linspace(0, 1, 2000)
    for threshold in thresholdArray:
        with open('GSVLR_C_' + str(c_estimator) + '_AUC_ROC_' + str(threshold) + '.metrics', 'a+') as LR_AUC_ROC:
            with open(r'GridSearchCVLogisticRegression_' + '_C_Estimator_' + str(c_estimator) + '.results') as GSCVLR_Results:
                gridSearchCVLogisticRegressionResultList = GSCVLR_Results.readline().split()
                GSCVLR_FilteredList = list(map(lambda ch: 0 if float(ch) < float(threshold) else 1, gridSearchCVLogisticRegressionResultList))
                true_positives = 0
                false_positives = 0
                true_negatives = 0
                false_negatives = 0
                for elemIndex in range(len(GSCVLR_FilteredList)):
                    if GSCVLR_FilteredList[elemIndex] == int(resultList_LR[elemIndex]):
                        if GSCVLR_FilteredList[elemIndex] == 0:
                            true_negatives += 1
                        else:
                            true_positives += 1
                    else:
                        if GSCVLR_FilteredList[elemIndex] == 0:
                            false_negatives += 1
                        else:
                            false_positives += 1
                true_positive_rate = true_positives / (true_positives + false_negatives)
                false_positive_rate = false_positives / (false_positives + true_negatives)
                if threshold == 0.39969984992496244:
                    bestThresholdResultsList_LR = gridSearchCVLogisticRegressionResultList
                LR_AUC_ROC.write("Threshold: " + str(threshold) + "--- True Positive Rate: " + str(true_positive_rate) + ", False Positive Rate: " + str(false_positive_rate) )
                LR_AUC_ROC.write('\n')
                false_positive_rate_list.append(false_positive_rate)
                true_positive_rate_list.append(true_positive_rate)
CIndex = 2
GIndex = 1 / 4
true_positive_rate_list2 = list()
false_positive_rate_list2 = list()
resultList_SVR = list()
bestThresholdResultsList_SVR = list()
auc_LR = 0
auc_SVR = 0
with open(r'SVRTestPlayerCalls.data') as results:
    for line in results:
        resultList_SVR.append(int(line))
    if os.path.exists(r'SVC_test_c(' + str(CIndex) + ')_g(' + str(GIndex) + ').results'):
        with open(r'SVC_test_c(' + str(CIndex) + ')_g(' + str(GIndex) + ').results') as svrResults:
            with open(r'SVR_test_ROC_AUC_C=' + str(CIndex) + '_G=' + str(GIndex) + '.metrics', 'a+') as SVR_AUC_ROC:
                svrResultList = svrResults.readline().split()
                thresholdArray = nm.linspace(0, 1, 2000)
                for threshold in thresholdArray:
                    svrResultFilteredList = list(
                        map(lambda ch: 0 if float(ch) < float(threshold) else 1, svrResultList))
                    true_positives = 0
                    false_positives = 0
                    true_negatives = 0
                    false_negatives = 0
                    for elemIndex in range(len(svrResultFilteredList)):
                        if svrResultFilteredList[elemIndex] == int(resultList_SVR[elemIndex]):
                            if svrResultFilteredList[elemIndex] == 0:
                                true_negatives += 1
                            else:
                                true_positives += 1
                        else:
                            if svrResultFilteredList[elemIndex] == 0:
                                false_negatives += 1
                            else:
                                false_positives += 1
                    if threshold == 0.14207103551775888:
                        bestThresholdResultsList_SVR = svrResultList
                    true_positive_rate = true_positives / (true_positives + false_negatives)
                    false_positive_rate = false_positives / (false_positives + true_negatives)
                    SVR_AUC_ROC.write("Threshold: " + str(threshold) + "--- True Positive Rate: " + str(
                        true_positive_rate) + ", False Positive Rate: " + str(false_positive_rate))
                    SVR_AUC_ROC.write('\n')
                    false_positive_rate_list2.append(false_positive_rate)
                    true_positive_rate_list2.append(true_positive_rate)

    fig, ax1 = mpl.subplots()
    ax1.plot(false_positive_rate_list, true_positive_rate_list, color='teal', label='Logistic Regression ROC with AUC: ' + str(mtrcs.auc(false_positive_rate_list, true_positive_rate_list)))
    ax1.set_xlabel('False Positive Rate [0,1]')
    ax1.set_ylabel('True Positive Rate [0,1]')
    ax1.set_title('Receiver Operating Characteristic curves')
    ax1.plot(false_positive_rate_list2, true_positive_rate_list2, color='tomato', label='Support Vector Regression ROC with AUC: ' + str(mtrcs.auc(false_positive_rate_list2, true_positive_rate_list2)))
    mpl.legend(loc='best')
    fig.tight_layout()
    mpl.show()
