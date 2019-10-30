from sklearn.externals import joblib
import os
import numpy as np
# import metrics
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV

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
            mySVR = SVR()
            parameters = {'C': [1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2, 1, 2, 4, 8, 16, 32, 64,
                      128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768],
                          'gamma': [1 / 32768, 2 / 32768, 4 / 32768, 8 / 32768, 16 / 32768, 32 / 32768, 64 / 32768, 128 / 32768,
                      256 / 32768,
                      512 / 32768, 1024 / 32768, 2048 / 32768, 4096 / 32768, 8192 / 32768, 16384 / 32768, 1, 2, 4, 8]}
            clf = GridSearchCV(estimator=mySVR, param_grid=parameters, cv=10)
            clf.fit(X, y)
            print('CLF READY!')
            c_estimator = clf.best_params_['C']
            g_estimator = clf.best_params_['gamma']
            curr_clf_predictions = clf.score(X, y)
            print(c_estimator, g_estimator)
            print(curr_clf_predictions)
            Y_Test = clf.predict(X_Test)
            print('PREDICTION READY')
            np.set_printoptions(suppress=True)
            np.savetxt('GridSearchCVSupportVectorRegression_' + '_C_Estimator_' + str(c_estimator) + '_G_estimator_' + str(g_estimator) + '.results', Y_Test, newline=" ")
            joblib.dump(clf, 'GridSearchCVSupportVectorRegression_CLFReady' + '_C_Estimator_' + str(c_estimator) + '_G_estimator_' + str(g_estimator) + '.pkl')
            features.close()
    calls.close()
features_test.close()
input("Press enter to exit ;)")
