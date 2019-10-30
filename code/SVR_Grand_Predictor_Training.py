# 3 hyperparameters, F1-score, C and gamma. Got to find the best threshold value for all of them.
# cross-validation will be used as well (5=10-fold)

# from sklearn.cross_validation import cross_val_score
# from sklearn.cross_validation import cross_val_score
from sklearn.externals import joblib
import os
import numpy as np
# import metrics
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVR

Dir = os.path.normpath(r'INSERT_YOUR_PATH_HERE')
os.chdir(Dir)

with open('SVRTestFeatures.data') as features_test:
    with open('SVRPlayerCalls.data') as calls:
        with open('SVRFeatures.data') as features:
            y = np.fromfile(calls, dtype=float, count=-1, sep=' ')
            X = np.fromfile(features, dtype=float, count=-1, sep=' ')
            X = np.reshape(X, (3269, 98), order='C')
            X_Test = np.fromfile(features_test, dtype=float, count=-1, sep=' ')
            X_Test = np.reshape(X_Test, (428, 98), order='C')
            CIndex = [1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2, 1, 2, 4, 8, 16, 32, 64,
                      128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
            GIndex = [1 / 32768, 2 / 32768, 4 / 32768, 8 / 32768, 16 / 32768, 32 / 32768, 64 / 32768, 128 / 32768,
                      256 / 32768,
                      512 / 32768, 1024 / 32768, 2048 / 32768, 4096 / 32768, 8192 / 32768, 16384 / 32768, 1, 2, 4, 8]
            for i in range(len(CIndex)):
                for j in range(len(GIndex)):
                    print(CIndex[i], GIndex[j])
                    if os.path.exists('SVC_test_c(' + str(CIndex[i]) + ')_g(' + str(GIndex[j]) + ').results'):
                        continue
                    clf = SVR(C=CIndex[i], gamma=GIndex[j])
                    clf.fit(X, y)
                    print('CLF READY!')
                    joblib.dump(clf, 'SVR_c(' + str(CIndex[i]) + ')_g(' + str(GIndex[j]) + ')_pre_cross_Val.pkl')
                    # curr_clf_scores = cross_val_score(clf, X, y, cv=5, scoring='f1')
                    curr_clf_predictions = cross_val_score(clf, X, y, cv=10)
                    print('CROSS VAL READY')
                    Y_Test = clf.predict(X_Test)
                    print('PREDICTION READY')
                    np.set_printoptions(suppress=True)
                    np.savetxt('SVC_test_c(' + str(CIndex[i]) + ')_g(' + str(GIndex[j]) +
                               ').results', Y_Test, newline=" ")
                    joblib.dump(clf, 'SVR_c(' + str(CIndex[i]) + ')_g(' + str(GIndex[j]) + ').pkl')
            features.close()
    calls.close()
features_test.close()
input("Press enter to exit ;)")
