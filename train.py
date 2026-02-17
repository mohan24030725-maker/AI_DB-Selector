import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

data = {'load':[50,100,150,200,250,300],'db':['4 way db','4 way db','8 way db','8 way db','12 way db','16 way db']}
df = pd.DataFrame(data)

model = DecisionTreeClassifier()
model.fit(df[['load']], df['db'])

pickle.dump(model, open('model.pkl','wb'))
print("Model trained")
