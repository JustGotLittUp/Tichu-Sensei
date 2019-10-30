import os

import numpy as nm
# import matplotlib.pyplot as pl

Dir = os.path.normpath(r'INSERT_YOUR_PATH_HERE')
os.chdir(Dir)

CIndex = [1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2, 1, 2, 4, 8, 16, 32, 64,
          128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
GIndex = [1 / 32768, 2 / 32768, 4 / 32768, 8 / 32768, 16 / 32768, 32 / 32768, 64 / 32768, 128 / 32768,
          256 / 32768,
          512 / 32768, 1024 / 32768, 2048 / 32768, 4096 / 32768, 8192 / 32768, 16384 / 32768, 1, 2, 4, 8]
max_acc = -1.0
max_f1 = -1.0
max_precision = -1.0
max_recall = -1.0
max_acc_info = ""
max_f1_info = ""
max_precison_info = ""
max_recall_info = ""
resultList = list()
with open(r'SVRTestPlayerCalls.data') as results:
    for line in results:
        resultList.append(line)
    with open('Final.metrics', 'a+') as SVR_Final_Metrics:
        for i in range(len(CIndex)):
            for j in range(len(GIndex)):
                if os.path.exists(r'SVC_test_c(' + str(CIndex[i]) + ')_g(' + str(GIndex[j]) + ').results'):
                    with open(r'SVC_test_c(' + str(CIndex[i]) + ')_g(' + str(GIndex[j]) + ').results') as SVR_Results:
                        with open(r'SVR_test_C=' + str(CIndex[i]) + '_G=' + str(GIndex[j]) + '.metrics', 'a+') as SVR_Metrics:
                            svrResultList = SVR_Results.readline().split()
                            f1list = list()
                            accuracyList = list()
                            precisionList = list()
                            recallList = list()
                            thresholdArray = nm.linspace(0, 1, 2000)
                            for threshold in thresholdArray:
                                svrResultFilteredList = list(map(lambda ch: 0 if float(ch) < float(threshold) else 1, svrResultList))
                                true_positives = 0
                                false_positives = 0
                                true_negatives = 0
                                false_negatives = 0
                                for elemIndex in range(len(svrResultFilteredList)):
                                    if svrResultFilteredList[elemIndex] == int(resultList[elemIndex]):
                                        if svrResultFilteredList[elemIndex] == 0:
                                            true_negatives += 1
                                        else:
                                            true_positives += 1
                                    else:
                                        if svrResultFilteredList[elemIndex] == 0:
                                            false_negatives += 1
                                        else:
                                            false_positives += 1
                                accuracy = (true_positives + true_negatives) / (true_positives + true_negatives + false_negatives + false_positives) if true_positives + true_negatives + false_negatives + false_positives > 0 else 0
                                precision = true_positives/(true_positives+false_positives) if true_positives+false_positives > 0 else 0
                                recall = true_positives/(false_negatives+true_positives) if false_negatives+true_positives > 0 else 0
                                f1 = 2*(recall*precision)/(recall+precision) if recall+precision > 0 else 0
                                SVR_Metrics.write("Threshold: " + str(threshold) + "--- Accuracy: " +
                                               str(accuracy) + ", Precision: " + str(precision) + ", Recall: " + str(recall) +
                                               ", F1: " + str(f1))
                                SVR_Metrics.write('\n')
                                f1list.append(f1)
                                accuracyList.append(accuracy)
                                precisionList.append(precision)
                                recallList.append(recallList)
                                if max_f1 < f1:
                                    max_f1 = f1
                                    max_f1_info = "C: " + str(CIndex[i]) + " , G: " + str(GIndex[
                                                                                              j]) + " ,Threshold: " + str(threshold) + " , F1: " + str(f1)
                                if max_acc < accuracy:
                                    max_acc = accuracy
                                    max_acc_info = "C: " + str(CIndex[i]) + " , G: " + str(GIndex[
                                        j]) + " ,Threshold: " + str(threshold) + " , Accuracy: " + str(accuracy)
                                if max_precision < precision:
                                    max_precision = precision
                                    max_precision_info = "C: " + str(CIndex[i]) + " , G: " + str(GIndex[
                                        j]) + " ,Threshold: " + str(threshold) + " , Precision: " + str(precision)
                                if max_recall < recall:
                                    max_recall = recall
                                    max_recall_info = "C: " + str(CIndex[i]) + " , G: " + str(GIndex[
                                        j]) + " ,Threshold: " + str(threshold) + " , Recall: " + str(recall)
        SVR_Final_Metrics.write("f1: ")
        SVR_Final_Metrics.write(str(max_f1))
        SVR_Final_Metrics.write(" " + str(max_f1_info))
        SVR_Final_Metrics.write('\n')
        SVR_Final_Metrics.write("precision: ")
        SVR_Final_Metrics.write(str(max_precision))
        SVR_Final_Metrics.write(" " + str(max_precision_info))
        SVR_Final_Metrics.write('\n')
        SVR_Final_Metrics.write("recall: ")
        SVR_Final_Metrics.write(str(max_recall))
        SVR_Final_Metrics.write(" " + str(max_recall_info))
        SVR_Final_Metrics.write('\n')
        SVR_Final_Metrics.write("acc: ")
        SVR_Final_Metrics.write(str(max_acc))
        SVR_Final_Metrics.write(" " + str(max_acc_info))
        SVR_Final_Metrics.write('\n')
