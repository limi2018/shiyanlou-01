# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def data_clean():
    df_data = pd.read_excel('ClimateChange.xlsx', sheetname='Data')

    df_co2 = df_data[df_data['Series code']=='EN.ATM.CO2E.KT'].set_index('Country code')
    df_gdp = df_data[df_data['Series code'] =='NY.GDP.MKTP.CD'].set_index('Country code')

    df_co2_nan = df_co2.replace({'..': pd.np.NaN})
    df_gdp_nan = df_gdp.replace({'..': pd.np.NaN})

    df_co2_fill = df_co2_nan.iloc[:, 5:].fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    df_gdp_fill = df_gdp_nan.iloc[:, 5:].fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)

    df_co2_fill['CO2-SUM'] = df_co2_fill.sum(axis=1)
    df_gdp_fill['GDP-SUM'] = df_gdp_fill.sum(axis=1)
    df_merge = pd.concat([df_co2_fill['CO2-SUM'], df_gdp_fill['GDP-SUM']], axis=1)

    df_merge_fill = df_merge.fillna(value=0)

    return df_merge_fill


def co2_gdp_plot():
    df_clean = data_clean()
    df_max_min = (df_clean - df_clean.min()) / (df_clean.max() - df_clean.min())

    china=[]
    for i in df_max_min[df_max_min.index == 'CHN'].values:
        china.extend(np.round(i, 3).tolist())
    
    countries_labels = ['USA', 'CHN', 'FRA', 'RUS', 'GBR']
    sticks_labels = []
    labels_position = []

    for i in range(len(df_max_min)):
        if df_max_min.index[i] in countries_labels:
            sticks_labels.append(df_max_min.index[i])
            labels_position.append(i)

    fig = plt.subplot()
    df_max_min.plot(kind='line',title='GDP-CO2', ax=fig)
    plt.xlabel('Countries')
    plt.ylabel('Values')
    plt.xticks(labels_position, sticks_labels, rotation='vertical')
    plt.show()

    return fig, china

#if __name__ == '__main__':
#    co2_gdp_plot()

