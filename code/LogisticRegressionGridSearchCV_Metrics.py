import os

import numpy as nm
# import matplotlib.pyplot as pl

Dir = os.path.normpath(r'INSERT_YOUR_PATH_HERE')
os.chdir(Dir)

c_estimator = 8.3022
max_acc = -1.0
max_f1 = -1.0
max_precision = -1.0
max_recall = -1.0
max_acc_info = ""
max_f1_info = ""
max_precision_info = ""
max_recall_info = ""
resultList = list()
with open(r'SVRTestPlayerCalls.data') as results:
    for line in results:
        resultList.append(line)
    with open('Final_GSVLR_C_' + str(c_estimator) + '.metrics', 'a+') as GSCVLR_Final_Metrics:
         if os.path.exists(r'GridSearchCVLogisticRegression_' + '_C_Estimator_' + str(c_estimator) + '.results'):
            with open(r'GridSearchCVLogisticRegression_' + '_C_Estimator_' + str(c_estimator) + '.results') as GSCVLR_Results:
                with open(r'GridSearchCVLogisticRegression_' + '_C_Estimator_' + str(c_estimator) + '.metrics', 'a+') as GSCVR_Metrics:
                    gridSearchCVLogisticRegressionResultList = GSCVLR_Results.readline().split()
                    f1list = list()
                    accuracyList = list()
                    precisionList = list()
                    recallList = list()
                    thresholdArray = nm.linspace(0, 1, 2000)
                    for threshold in thresholdArray:
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
                        GSCVR_Metrics.write("Threshold: " + str(threshold) + "--- Accuracy: " +
                                       str(accuracy) + ", Precision: " + str(precision) + ", Recall: " + str(recall) +
                                       ", F1: " + str(f1))
                        GSCVR_Metrics.write('\n')
                        f1list.append(f1)
                        accuracyList.append(accuracy)
                        precisionList.append(precision)
                        recallList.append(recallList)
                        if max_f1 < f1:
                            max_f1 = f1
                            max_f1_info = "C: " + str(c_estimator) + " ,Threshold: " + str(threshold) + " , F1: " + str(f1)
                        if max_acc < accuracy:
                            max_acc = accuracy
                            max_acc_info = "C: " + str(c_estimator) + " ,Threshold: " + str(threshold) + " , Accuracy: " + str(accuracy)
                        if max_precision < precision:
                            max_precision = precision
                            max_precision_info = "C: " + str(c_estimator) + " ,Threshold: " + str(threshold) + " , Precision: " + str(precision)
                        if max_recall < recall:
                            max_recall = recall
                            max_recall_info = "C: " + str(c_estimator) + " ,Threshold: " + str(threshold) + " , Recall: " + str(recall)
         GSCVLR_Final_Metrics.write("f1: ")
         GSCVLR_Final_Metrics.write(str(max_f1))
         GSCVLR_Final_Metrics.write(" " + str(max_f1_info))
         GSCVLR_Final_Metrics.write('\n')
         GSCVLR_Final_Metrics.write("precision: ")
         GSCVLR_Final_Metrics.write(str(max_precision))
         GSCVLR_Final_Metrics.write(" " + str(max_precision_info))
         GSCVLR_Final_Metrics.write('\n')
         GSCVLR_Final_Metrics.write("recall: ")
         GSCVLR_Final_Metrics.write(str(max_recall))
         GSCVLR_Final_Metrics.write(" " + str(max_recall_info))
         GSCVLR_Final_Metrics.write('\n')
         GSCVLR_Final_Metrics.write("acc: ")
         GSCVLR_Final_Metrics.write(str(max_acc))
         GSCVLR_Final_Metrics.write(" " + str(max_acc_info))
         GSCVLR_Final_Metrics.write('\n')
