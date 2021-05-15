# -*- coding: utf-8 -*-
"""
Created on Sat May 15 08:23:43 2021

@author: rabindra
"""


import pandas as pd
import pandas_profiling


def read_data(file_name, file_date):
    loaded_df = pd.read_excel(file_name)
    loaded_df['ExamYear'] = file_date
    return loaded_df


df_2074 = read_data('data/2074_Sanjeev_Sir.xlsx', '2074')
df_2073 = read_data('data/BE2073.xlsx', '2073')
df_2076 = read_data('data/Daya Sir 2076.xlsx', '2076')
df_2077 = read_data('data/Students2077.xlsx', '2077')

aggregated_data = pd.concat([df_2073, df_2074, df_2076, df_2077], ignore_index=True)
print(aggregated_data.head())



profile_report = pandas_profiling.ProfileReport(aggregated_data)
profile_report.to_file('InitialProfilingReport.html')
aggregated_data.to_csv('data/AggregatedData.csv', quotechar='"', index=False)