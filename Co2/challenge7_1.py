# -*- coding: utf-8 -*-
import pandas as pd

def data_clean():
    data = pd.read_excel('ClimateChange.xlsx',sheetname='Data')
    data = data[data['Series code']=='EN.ATM.CO2E.KT'].set_index('Country code')
    data.drop(labels=['Country name', 'Series code','Series name', 'SCALE', 'Decimals'],axis=1,inplace=True)
    data.replace({'..': pd.np.NaN}, inplace=True)
    data = data.fillna(method='ffill',axis=1).fillna(method='bfill',axis=1)
    data.dropna(how='all', inplace=True)
    data['Sum emissions'] = data.sum(axis=1)
    data = data['Sum emissions']

    countries = pd.read_excel('ClimateChange.xlsx',sheetname='Country')
    countries.set_index('Country code',inplace=True)
    countries.drop(labels=['Capital city', 'Region','Lending category'],axis=1,inplace=True)

    return pd.concat([data,countries],axis=1)


def co2():
    df = data_clean()

    df_sum = df.groupby('Income group').sum()

    df_max = df.sort_values(by='Sum emissions',ascending=False).groupby('Income group').head(1).set_index('Income group')
    df_max.columns = ['Highest emissions', 'Highest emission country']
    df_max = df_max.reindex(columns=['Highest emission country', 'Highest emissions'])

    df_min = df.sort_values(by='Sum emissions',ascending=True).groupby('Income group').head(1).set_index('Income group')
    df_min.columns = ['Lowest emissions','Lowest emission country']
    df_min = df_min.reindex(columns=['Lowest emission country', 'Lowest emissions'])

    result = pd.concat([df_sum,df_max,df_min],axis=1)

    return result