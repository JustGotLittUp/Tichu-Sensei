import os
import numpy as nm

Dir = os.path.normpath(r'INSERT_YOUR_PATH_HERE')
os.chdir(Dir)

CIndex = [1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2, 1, 2, 4, 8, 16, 32, 64,
          128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
GIndex = [1 / 32768, 2 / 32768, 4 / 32768, 8 / 32768, 16 / 32768, 32 / 32768, 64 / 32768, 128 / 32768,
          256 / 32768,
          512 / 32768, 1024 / 32768, 2048 / 32768, 4096 / 32768, 8192 / 32768, 16384 / 32768, 1, 2, 4, 8]

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
        max_acc_C = -1
        max_acc_G = -1
        max_f1_C = -1
        max_f1_G = -1
        max_precision_C = -1
        max_precision_G = -1
        max_recall_C = -1
        max_recall_G = -1
        with open(r'Threshold=' + str(threshold) + '.metrics', 'a+') as SVR_Threshold_Metrics:
            for i in range(len(CIndex)):
                for j in range(len(GIndex)):
                    if os.path.exists(r'SVC_test_c(' + str(CIndex[i]) + ')_g(' + str(GIndex[j]) + ').results'):
                        with open(r'SVC_test_c(' + str(CIndex[i]) + ')_g(' + str(GIndex[j]) + ').results') as svrResults:
                            svrResultList = svrResults.readline().split()
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
                            if max_f1 < f1:
                                max_f1 = f1
                                max_f1_C = CIndex[i]
                                max_f1_G = GIndex[j]
                            if max_acc < accuracy:
                                max_acc = accuracy
                                max_acc_C = CIndex[i]
                                max_acc_G = GIndex[j]
                            if max_precision < precision:
                                max_precision = precision
                                max_precision_C = CIndex[i]
                                max_precision_G = GIndex[j]
                            if max_recall < recall:
                                max_recall = recall
                                max_recall_C = CIndex[i]
                                max_recall_G = GIndex[j]
            SVR_Threshold_Metrics.write('F1: ' + str(max_f1))
            SVR_Threshold_Metrics.write('\n')
            SVR_Threshold_Metrics.write('F1_C: ' + str(max_f1_C))
            SVR_Threshold_Metrics.write('\n')
            SVR_Threshold_Metrics.write('F1_Gamma: ' + str(max_f1_G))
            SVR_Threshold_Metrics.write('\n')
            SVR_Threshold_Metrics.write('Acc: ' + str(max_acc))
            SVR_Threshold_Metrics.write('\n')
            SVR_Threshold_Metrics.write('Acc_C: ' + str(max_acc_C))
            SVR_Threshold_Metrics.write('\n')
            SVR_Threshold_Metrics.write('Acc_Gamma: ' + str(max_acc_G))
            SVR_Threshold_Metrics.write('\n')
            SVR_Threshold_Metrics.write('Prec: ' + str(max_precision))
            SVR_Threshold_Metrics.write('\n')
            SVR_Threshold_Metrics.write('Prec_C: ' + str(max_precision_C))
            SVR_Threshold_Metrics.write('\n')
            SVR_Threshold_Metrics.write('Prec_Gamma: ' + str(max_precision_G))
            SVR_Threshold_Metrics.write('\n')
            SVR_Threshold_Metrics.write('Rec: ' + str(max_recall))
            SVR_Threshold_Metrics.write('\n')
            SVR_Threshold_Metrics.write('Rec_C: ' + str(max_recall_C))
            SVR_Threshold_Metrics.write('\n')
            SVR_Threshold_Metrics.write('Rec_G: ' + str(max_recall_G))
            SVR_Threshold_Metrics.write('\n')
