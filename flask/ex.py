import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
def ValuePredictor(nlist):
    train_data=pd.read_csv(r'Training.csv')
    x=train_data.drop('prognosis',axis=1)
    y=train_data['prognosis']
    rf_clf=RandomForestClassifier(n_estimators=100)
    rf_clf.fit(x,y)
    arr = np.array(nlist) 
    arr=arr.reshape(1,-1)
    result=rf_clf.predict(arr)
    return result