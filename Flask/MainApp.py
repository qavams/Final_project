from flask import Flask, request
import requests
import json
import csv
import pandas as pd 
import numpy as np
import copy
import warnings

app = Flask(__name__)

@app.route('/a', methods=['GET', 'POST'])
def Update():
    myjson=request.get_json()
    inputData=myjson['Data'].split('\n')
    for i in range(len(inputData)):
        if inputData[i].lstrip('-').isdigit():
            inputData[i]=float(inputData[i])
               
    Digits=[inputData[1],inputData[6],inputData[7],inputData[8],inputData[9],inputData[10],inputData[11],inputData[12]]
    for i in Digits:
        if isinstance(i,float)!=True:
            print('The order is messed up. Try again.')
            print(Digits)
            print(inputData)
            return 'The order is messed up. Try again.'
    if '' in inputData:
        print('There should be no blanks among the entries')
        return 'There should be no blanks among the entries'
    elif int(min([inputData[1],min(inputData[6:12])])) < 0 :
        print('Numbers must be positive') 
        return 'Numbers must be positive'
    elif inputData[0]!='female' and inputData[0]!='male':
        print('Err in value 1')
        return 'Err in value 1'
    elif inputData[2]!='Black' and inputData[2]!='White' and inputData[2]!='Mexican' and inputData[2]!='Other' and inputData[2]!='Hispanic':
        print('Err in value 3') 
        return 'Err in value 3'   
    elif inputData[3]!='9 - 11th Grade' and inputData[3]!='8th Grade' and inputData[3]!='College Grad' and inputData[3]!='High School' and inputData[3]!='Some College':
        print('Err in value 4')   
        return 'Err in value 4'   
    elif inputData[4]!='Divorced' and inputData[4]!='LivePartner' and inputData[4]!='Married' and inputData[4]!='Widowed' and inputData[4]!='NeverMarried' and inputData[4]!='Separated':
        print('Err in value 5') 
        return 'Err in value 5'
    elif inputData[5]!='Looking' and inputData[5]!='NotWorking' and inputData[5]!='Working' :
        print('Err in value 6')  
        return 'Err in value 6'
    elif inputData[13]!='No' and inputData[13]!='Yes':
        print('Err in value 14')  
        return 'Err in value 14' 
    elif inputData[14]!='No' and inputData[14]!='Yes':
        print('Err in value 15')
        return 'Err in value 15'
    else:   
        myFile = open('NHANES.csv', 'a')
        writer = csv.writer(myFile)
        writer.writerow(inputData)
        myFile.close()
        print('Successfully delivered')    
        return 'Successfully delivered'

@app.route('/b', methods=['GET', 'POST'])
def Prediction():
    myjson=request.get_json()
    inputData=myjson['Data'].split('\n')
    for i in range(len(inputData)):
        if inputData[i].lstrip('-').isdigit():
            inputData[i]=float(inputData[i])
    inputData.append('Yes')
    Digits=[inputData[1],inputData[6],inputData[7],inputData[8],inputData[9],inputData[10],inputData[11],inputData[12]]
    for i in Digits:
        if (isinstance(i,float))!=True:
            print('The order is messed up. Try again.')
            return 'The order is messed up. Try again.'
    if '' in inputData:
        print('There should be no blanks among the entries')
        print(inputData)
        return 'There should be no blanks among the entries'
    elif int(min([inputData[1],min(inputData[6:12])])) < 0 :
        print('Numbers must be positive') 
        return 'Numbers must be positive'
    elif inputData[0]!='female' and inputData[0]!='male':
        print('Err in value 1')
        return 'Err in value 1'
    elif inputData[2]!='Black' and inputData[2]!='White' and inputData[2]!='Mexican' and inputData[2]!='Other' and inputData[2]!='Hispanic':
        print('Err in value 3') 
        return 'Err in value 3'   
    elif inputData[3]!='9 - 11th Grade' and inputData[3]!='8th Grade' and inputData[3]!='College Grad' and inputData[3]!='High School' and inputData[3]!='Some College':
        print('Err in value 4')   
        return 'Err in value 4'   
    elif inputData[4]!='Divorced' and inputData[4]!='LivePartner' and inputData[4]!='Married' and inputData[4]!='Widowed' and inputData[4]!='NeverMarried' and inputData[4]!='Separated':
        print('Err in value 5') 
        return 'Err in value 5'
    elif inputData[5]!='Looking' and inputData[5]!='NotWorking' and inputData[5]!='Working' :
        print('Err in value 6')  
        return 'Err in value 6'
    elif inputData[13]!='No' and inputData[13]!='Yes':
        print('Err in value 14')  
        return 'Err in value 14'    
    else:    
        warnings.filterwarnings('ignore')
        dataset1 = pd.read_csv('NHANES.csv')
        #Here, because we have little processing power, we had to delete some data.
        #dataset2=dataset1.drop(dataset1.index[4594:10001])
        dataset2=dataset1.sample(n = 100)

        #Here, we are going to delete the columns that we don't need.
        dataset3=dataset2[["Gender",'Age','Race1','Education','MaritalStatus','Work','Weight','Height','BMI','BPSysAve','BPDiaAve','DirectChol','TotChol','PhysActive','Diabetes']]

        dataset=copy.deepcopy(dataset3)
        dataset_new=dataset
        df3 = dataset_new.copy()
        # These columns must be converted
        df3=df3.dropna()

        a=inputData

        #print(len(df3.index))
        df3 = df3.append(pd.DataFrame([a], columns=df3.columns), ignore_index=True)
        #print(df3.iloc[-1,:])

        df3 = pd.get_dummies(df3,columns = ['Gender', 'Race1','Education','MaritalStatus','Work','PhysActive','Diabetes'], drop_first = True)
        #print(df3.columns)
        x=df3.iloc[-1,:].tolist()
        x.pop()
        #print(len(df3.index))
        dataset_new=df3.copy()
        df3=df3.drop(len(df3)-1)
        #print(len(df3.index))
        #print(x)

        # Selecting X & Y
        X = dataset_new.iloc[:, :-1].values
        Y = dataset_new.iloc[:, -1].values

        # Splitting the dataset into the Training set and Test set
        from sklearn.model_selection import train_test_split
        XTrain, XTest, YTrain, YTest = train_test_split(X,Y, test_size = 0.25, random_state = 0)

        #print(dataset_new.columns)

        from sklearn.linear_model import LogisticRegression
        logreg = LogisticRegression()
        #print(XTest[0])  
        logreg.fit(XTrain, YTrain)
        logreg_pred=logreg.predict(XTest)

        YP_ranfor = logreg.predict(XTest)

        TempX=x
        TempXnpArr=np.array(TempX) 
        TempXnpArr=TempXnpArr.reshape(1,-1)
        Answer=logreg.predict(TempXnpArr)

        if Answer[0]==1:
            print("You may develop diabetes!")
            return 'You may develop diabetes!'
        else:    
            print('The chances of you developing diabetes are very low')
            return 'The chances of you developing diabetes are very low'

if __name__ == '__main__':
    app.run()

