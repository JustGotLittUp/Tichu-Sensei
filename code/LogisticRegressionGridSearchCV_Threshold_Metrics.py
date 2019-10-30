import os
import numpy as nm

Dir = os.path.normpath(r'INSERT_YOUR_PATH_HERE')
os.chdir(Dir)

c_estimator = 8.3022
resultList = list()
with open(r'SVRTestPlayerCalls.data') as results:
    for line in results:
        resultList.append(line)
    thresholdArray = nm.linspace(0, 1, 2000)
    for threshold in thresholdArray:
        max_acc = -1.0
        max_f1 = -1.0
        max_precision = -1.0
        max_recall = -1.0
        with open('Final_GSVLR_C_' + str(c_estimator) + '_Threshold_' + str(threshold) + '.metrics', 'a+') as GSCVR_Threshold_Metrics:
            if os.path.exists(r'GridSearchCVLogisticRegression_' + '_C_Estimator_' + str(c_estimator) + '.results'):
                with open(r'GridSearchCVLogisticRegression_' + '_C_Estimator_' + str(c_estimator) + '.results') as GSCVLR_Results:
                    gridSearchCVLogisticRegressionResultList = GSCVLR_Results.readline().split()
                    GSCVLR_FilteredList = list(map(lambda ch: 0 if float(ch) < float(threshold) else 1, gridSearchCVLogisticRegressionResultList))
                    true_positives = 0
                    false_positives = 0
                    true_negatives = 0
                    false_negatives = 0
                    for elemIndex in range(len(GSCVLR_FilteredList)):
                        if GSCVLR_FilteredList[elemIndex] == int(resultList[elemIndex]):
                            if GSCVLR_FilteredList[elemIndex] == 0:
                                true_negatives += 1
                            else:
                                true_positives += 1
                        else:
                            if GSCVLR_FilteredList[elemIndex] == 0:
                                false_negatives += 1
                            else:
                                false_positives += 1
                    accuracy = (true_positives + true_negatives) / (true_positives + true_negatives + false_negatives + false_positives) if true_positives + true_negatives + false_negatives + false_positives > 0 else 0
                    precision = true_positives/(true_positives+false_positives) if true_positives+false_positives > 0 else 0
                    recall = true_positives/(false_negatives+true_positives) if false_negatives+true_positives > 0 else 0
                    f1 = 2*(recall*precision)/(recall+precision) if recall+precision > 0 else 0
                    if max_f1 < f1:
                        max_f1 = f1
                    if max_acc < accuracy:
                        max_acc = accuracy
                    if max_precision < precision:
                        max_precision = precision
                    if max_recall < recall:
                        max_recall = recall
            GSCVR_Threshold_Metrics.write("f1: ")
            GSCVR_Threshold_Metrics.write(str(max_f1))
            GSCVR_Threshold_Metrics.write('\n')
            GSCVR_Threshold_Metrics.write("precision: ")
            GSCVR_Threshold_Metrics.write(str(max_precision))
            GSCVR_Threshold_Metrics.write('\n')
            GSCVR_Threshold_Metrics.write("recall: ")
            GSCVR_Threshold_Metrics.write(str(max_recall))
            GSCVR_Threshold_Metrics.write('\n')
            GSCVR_Threshold_Metrics.write("acc: ")
            GSCVR_Threshold_Metrics.write(str(max_acc))
            GSCVR_Threshold_Metrics.write('\n')
