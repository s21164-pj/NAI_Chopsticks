import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


'''
read data from csv
'''
data = pd.read_csv("LoanApprovalPrediction.csv")
data.head(5)


'''
Get the number of columns of object datatype.
'''
obj = (data.dtypes == 'object')
print("Categorical variables:",len(list(obj[obj].index)))


'''
Visualize all the unique values in columns using barplot. This will simply show which value is dominating as per our dataset.
'''
data.drop(['Loan_ID'],axis=1,inplace=True)
obj = (data.dtypes == 'object')
object_cols = list(obj[obj].index)
plt.figure(figsize=(18, 36))
index = 1

for col in object_cols:
    y = data[col].value_counts()
    plt.subplot(11, 4, index)
    plt.xticks(rotation=90)
    sns.barplot(x=list(y.index), y=y)
    index += 1


'''
label_encoder object knows how to understand word labels.
'''
label_encoder = preprocessing.LabelEncoder()
obj = (data.dtypes == 'object')
for col in list(obj[obj].index):
    data[col] = label_encoder.fit_transform(data[col])


''' 
To find the number of columns with datatype==object
'''
obj = (data.dtypes == 'object')
print("Categorical variables:",len(list(obj[obj].index)))

plt.figure(figsize=(12, 6))


'''
generating heatmap
'''
sns.heatmap(data.corr(), cmap='BrBG', fmt='.2f',
            linewidths=2, annot=True)


'''
generating gender plot
'''
sns.catplot(x="Gender", y="Married",
            hue="Loan_Status",
            kind="bar",
            data=data)


'''
Now we will find out if there is any missing values in the dataset
'''
for col in data.columns:
    data[col] = data[col].fillna(data[col].mean())

data.isna().sum()


'''
Splitting Dataset 
'''
X = data.drop(['Loan_Status'], axis=1)
Y = data['Loan_Status']
X.shape, Y.shape

X_train, X_test, Y_train, Y_test = train_test_split(X, Y,
                                                    test_size=0.4,
                                                    random_state=1)
X_train.shape, X_test.shape, Y_train.shape, Y_test.shape


'''
To predict the accuracy we will use the accuracy score function from scikit-learn library.
'''
knn = KNeighborsClassifier(n_neighbors=3)
rfc = RandomForestClassifier(n_estimators=7,
                             criterion='entropy',
                             random_state=7)
svc = SVC()
lc = LogisticRegression()


'''
Prediction on the test set:
'''
for clf in (rfc, knn, svc,lc):
    clf.fit(X_train, Y_train)
    Y_pred = clf.predict(X_test)
    print("Accuracy score of ",
          clf.__class__.__name__,"=",
          100*metrics.accuracy_score(Y_test,
                                     Y_pred))