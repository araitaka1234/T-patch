pip3 install pandas
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import xlrd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
import os
import csv


df=pd.read_excel('data/JTM_outbound20190906.xlsx')
# df.head()

df_korea=df.iloc[:,6]
# df_korea.head()
df_korea_2005_to_2018=df_korea.iloc[63:231,]
# df_korea_2005_to_2018
np_korea_2005_to_2018=df_korea_2005_to_2018.values
# type(np_korea_2005_to_2018)
df_korea_2005_to_2018_2=pd.DataFrame(np_korea_2005_to_2018,columns=['visitor'])
# df_korea_2005_to_2018_2.head(20)

korea_month=np.arange(1,13)
# korea_month

for i in range(1,14):
    print(i)
    korea_month=np.append(korea_month,[1,2,3,4,5,6,7,8,9,10,11,12],axis=0)

np_korea_month=korea_month.reshape(len(korea_month),1)

df_korea_month=pd.DataFrame(np_korea_month,columns=["month"])

df_exchange=pd.read_excel('data/won_yen.xlsx',encoding='shift-Jis')
s_exchange=df_exchange.iloc[:168,:]
df_exchange_2=pd.DataFrame(columns=['start','max','min','fin'])
s_exchange.index=np.arange(len(s_exchange))
s=s_exchange.values
# s
s_exchange_2=pd.DataFrame()
for i in range(168):
    array=s[[167-i]]
    df_array=pd.DataFrame(array)
    s_exchange_2=pd.concat([s_exchange_2,df_array],axis=0)

exchange_rename=s_exchange_2.rename(columns={1:'start',2:'min',3:'max',4:'fin'})
exchange_data=exchange_rename.loc[:,['start','min','max','fin']]
exchange_data.index=np.arange(len(exchange_data))

w1=pd.read_csv('data/data.csv',encoding='shift-Jis')

df_process=pd.concat([df_korea_month,exchange_data,w1,df_korea_2005_to_2018_2],axis=1)

df_target=pd.concat([df_korea_month,exchange_data,w1],axis=1)

exchange_min=exchange_data.iloc[:,1]
exchange_min.head(10)
df_exchange_min=pd.DataFrame(exchange_min)
# df_exchange_min.head()

exchange_last=exchange_data.iloc[:,3]
df_exchange_last=pd.DataFrame(exchange_last)

y_lin=np.array(df_korea_2005_to_2018_2.values)

quad=PolynomialFeatures(degree=2)

min_quad=quad.fit_transform(df_exchange_min.values)
last_quad=quad.fit_transform(df_exchange_last.values)

X_quad=np.hstack((min_quad,last_quad))

X_quad_train,X_quad_test, y_lin_train, y_lin_test = train_test_split(X_quad, y_lin, test_size = 0.3, random_state = 0)

model_quad_2 = LinearRegression()
model_quad_2.fit(X_quad_train, y_lin_train)


def __predictor__(exchange_test):
    X_new=(exchange_test)
    y_pred=model_quad_2.predict(X_new)
    y_y=int(y_pred)
    y_y_y=int(y_y/218475*100)
    return y_y_y
