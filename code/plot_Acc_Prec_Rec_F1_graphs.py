import os
import numpy as nm
import matplotlib.pylab as mpl

Dir = os.path.normpath(r'INSERT_YOUR_PATH_HERE')
os.chdir(Dir)

c_estimator = 8.3022
thresholdArray = nm.linspace(0, 1, 2000)
f1PerThreshold = list()
f1CPerThreshold = list()
f1GPerThreshold = list()
recPerThreshold = list()
recCPerThreshold = list()
recGPerThreshold = list()
precPerThreshold = list()
precCPerThreshold = list()
precGPerThreshold = list()
accPerThreshold = list()
accCPerThreshold = list()
accGPerThreshold = list()
LRGSCV_f1PerThreshold = list()
LRGSCV_accPerThreshold = list()
LRGSCV_precPerThreshold = list()
LRGSCV_recPerThreshold = list()
for threshold in thresholdArray:
    if os.path.exists(r'Threshold=' + str(threshold) + '.metrics'):
        with open(r'Threshold=' + str(threshold) + '.metrics') as SVR_CurrentThresholdMetrics:
            f1PerThreshold.append(round(float(SVR_CurrentThresholdMetrics.readline().split(' ')[1]), 3))
            f1CPerThreshold.append(round(float(SVR_CurrentThresholdMetrics.readline().split(' ')[1]), 3))
            f1GPerThreshold.append(round(float(SVR_CurrentThresholdMetrics.readline().split(' ')[1]), 3))
            accPerThreshold.append(round(float(SVR_CurrentThresholdMetrics.readline().split(' ')[1]), 3))
            accCPerThreshold.append(round(float(SVR_CurrentThresholdMetrics.readline().split(' ')[1]), 3))
            accGPerThreshold.append(round(float(SVR_CurrentThresholdMetrics.readline().split(' ')[1]), 3))
            precPerThreshold.append(round(float(SVR_CurrentThresholdMetrics.readline().split(' ')[1]), 3))
            precCPerThreshold.append(round(float(SVR_CurrentThresholdMetrics.readline().split(' ')[1]), 3))
            precGPerThreshold.append(round(float(SVR_CurrentThresholdMetrics.readline().split(' ')[1]), 3))
            recPerThreshold.append(round(float(SVR_CurrentThresholdMetrics.readline().split(' ')[1]), 3))
            recCPerThreshold.append(round(float(SVR_CurrentThresholdMetrics.readline().split(' ')[1]), 3))
            recGPerThreshold.append(round(float(SVR_CurrentThresholdMetrics.readline().split(' ')[1]), 3))
    if os.path.exists(r'Final_GSVLR_C_' + str(c_estimator) + '_Threshold_' + str(threshold) + '.metrics'):
        with open(r'Final_GSVLR_C_' + str(c_estimator) + '_Threshold_' + str(threshold) + '.metrics') as LRGSCV_CurrentThresholdMetrics:
            LRGSCV_f1PerThreshold.append(round(float(LRGSCV_CurrentThresholdMetrics.readline().split(' ')[1]), 3))
            LRGSCV_precPerThreshold.append(round(float(LRGSCV_CurrentThresholdMetrics.readline().split(' ')[1]), 3))
            LRGSCV_recPerThreshold.append(round(float(LRGSCV_CurrentThresholdMetrics.readline().split(' ')[1]), 3))
            LRGSCV_accPerThreshold.append(round(float(LRGSCV_CurrentThresholdMetrics.readline().split(' ')[1]), 3))

#change LRGSCV_recPerThreshold and recPerThreshold to prec acc and f1 to get the other graphs as well.
fig, ax1 = mpl.subplots()
ax1.plot(thresholdArray, LRGSCV_recPerThreshold, color='teal')
ax1.set_xlabel('Threshold')
ax1.set_ylabel('LR Recall Score', color='teal')
ax1.set_title('Recall Score / Threshold')
ax2 = ax1.twinx()
ax2.plot(thresholdArray, recPerThreshold, color='tomato')
ax2.set_ylabel('SVR Recall Score', color='tomato')
fig.tight_layout()
mpl.show()
