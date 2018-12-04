# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.linear_model import LinearRegression

def Temperature():
    df_GreenhouseGas = pd.read_csv('GreenhouseGas.csv', header=0)
    df_GlobalSurfaceTemperature = pd.read_csv('GlobalSurfaceTemperature.csv', header=0)
    df_CO2ppm = pd.read_csv('CO2ppm.csv')

    df_GreenhouseGas_new = pd.DataFrame(df_GreenhouseGas[['N2O', 'CH4', 'CO2']].values,index=pd.to_datetime(df_GreenhouseGas['Year'].astype(str)),columns=['N2O', 'CH4', 'CO2'])
    
    df_GlobalSurfaceTemperature_new = pd.DataFrame(df_GlobalSurfaceTemperature[['Median', 'Upper', 'Lower']].values, index=pd.to_datetime(df_GlobalSurfaceTemperature['Year'].astype(str)), columns=['Median', 'Upper', 'Lower'])
    
    df_CO2ppm_new = pd.DataFrame(df_CO2ppm.iloc[:,1].values, index=pd.to_datetime(df_CO2ppm['Year'].astype(str)), columns= ['CO2_PPM'])

    df_merge = pd.concat([df_GreenhouseGas_new, df_CO2ppm_new, df_GlobalSurfaceTemperature_new], axis =1)
    
    feature = df_merge.iloc[: ,0:4].fillna(method='ffill').fillna(method='bfill')
    feature_train = feature['1970-01-01':'2010-01-01']
    feature_test = feature['2011-01-01':'2017-01-01']

    target_Median = df_merge.iloc[:, 4]
    target_Median_train = target_Median['1970-01-01':'2010-01-01']
    model_Median = LinearRegression()
    model_Median.fit(feature_train, target_Median_train)
    MedianPredict = model_Median.predict(feature_test)

    target_Upper = df_merge.iloc[:, 5]
    target_Upper_train = target_Upper['1970-01-01':'2010-01-01']
    model_Upper = LinearRegression()
    model_Upper.fit(feature_train, target_Upper_train)
    UpperPredict = model_Upper.predict(feature_test)
        
    target_Lower = df_merge.iloc[:, 6]
    target_Lower_train = target_Lower['1970-01-01':'2010-01-01']
    model_Lower = LinearRegression()
    model_Lower.fit(feature_train, target_Lower_train)
    LowerPredict = model_Lower.predict(feature_test)

    return list(UpperPredict), list(MedianPredict), list(LowerPredict)
