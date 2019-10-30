from sklearn.externals import joblib
import os
import numpy as np
# import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

#C parameters are the ones that provide the best results. After running this code we found that 8.3022 is the best one.

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
            lr = LogisticRegression()
            parameters = {'C': [8.3022, 8.3024, 8.3026, 8.3028, 8.303, 8.3032, 8.3034, 8.3036, 8.3038, 8.304, 8.3042, 8.3044, 8.3046, 8.3048, 8.305, 8.3052, 8.3054, 8.3056, 8.3058]}
            clf = GridSearchCV(estimator=lr, param_grid=parameters, cv=10)
            clf.fit(X, y)
            print('CLF READY!')
            c_estimator = clf.best_params_['C']
            curr_clf_predictions = clf.score(X, y)
            print(c_estimator)
            print(curr_clf_predictions)
            Y_Test = clf.predict_proba(X_Test)[:, 1]
            print('PREDICTION READY')
            np.set_printoptions(suppress=True)
            np.savetxt('GridSearchCVLogisticRegression_' + '_C_Estimator_' + str(c_estimator) + '.results', Y_Test, newline=" ")
            joblib.dump(clf, 'GridSearchCVLogisticRegression_CLFReady' + '_C_Estimator_' + str(c_estimator) + '.pkl')
            features.close()
    calls.close()
features_test.close()
input("Press enter to exit ;)")
