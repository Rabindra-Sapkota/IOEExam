# -*- coding: utf-8 -*-
"""
Created on Sat May 15 10:27:03 2021

@author: rabindra
"""


import pandas as pd
import pandas_profiling
from pyBSDate import convert_BS_to_AD
import datetime


def convert_bs_to_ad(bs_series):
    try:
        ad_date = convert_BS_to_AD(bs_series[:4], bs_series[5:7], bs_series[-2:])
        return datetime.datetime(ad_date[0], ad_date[1], ad_date[2]).strftime('%Y-%m-%d')
    except:
        return pd.NaT


data_df = pd.read_csv('data/AggregatedData.csv', low_memory=False)
data_df.drop(['FormNo', 'FirstName', 'MiddleName', 'LastName', 'ModifiedDate',
              'ModifiedBy', 'CreatedDate', 'WardNo', 'SLCSymbolNo', 'PCLSymbolNo',
              'FatherFirstName', 'FatherMiddleName', 'FatherLastName', 'MotherFirstName',
              'MotherMiddleName', 'MotherLastName', 'DistrictCode', 'StudentID',
              'VoucherNo', 'StudentCode', 'ContactNo', 'Email', 'NationalityID',
              'CountryID', 'IndianEmbassyID', 'ExamCenterID', 'DistrictID',
              'SLCEquivalentID', 'PCLEquivalentID', 'SLCBoardID', 'PCLBoardID',
              'PCLResultTypeID', 'PCLLocationID', 'EthnicGroupID', 'EthnicGroupSpecify',
              'IdentificationNo', 'CheckedBy', 'Password', 'FacultyID', 'LevelID',
              'ShiftID', 'FiscalYearID', 'FullName', 'CreatedBy', 'ExamSessionID',
              'IdentificationTypeID', 'BirthDateAD', 'InstitutionTypeID', 'RejectReason',
              'Capacity', 'ExamDurationMinute', 'IsResultImmediately', 'PageSize',
              'FacultyName', 'LevelName', 'ExamRollNo',  'PCLBoardName', 'PCLBoardSpecify',
              'PCLEquivalentSpecify', 'PCLPassedYear', 'PCLPercentage','PCLSchoolFullAddress',
              'RollNoString', 'SLCBoardName', 'SLCBoardSpecify', 'SLCEquivalentSpecify',
               'SLCSchoolFullAddress', 'ZoneID', 'SLCSchoolDistrictID', 'PCLSchoolDistrictID',
               'IsAccepted', 'IsSubmitted', 'ExamSessionDateBS', 'FormStatus', 'FormIndex',
               'PhotoDocumentID', 'Active', 'ExamSessionName', 'StartTime', 'StartTime',
               'EndTime', 'ExamStartedTime','FiscalYearName', 'PCLPassedYearCalendar',
               'SLCPassedYearCalendar', 'FormSubmittedDate', 'ExamSessionDateAD'],
             axis='columns', inplace=True)

bs_ad_map = {2034:1978, 2039:1983, 2042:1986, 2051:1995, 2053:1997, 2054:1998, 2055:1999, 2056:2000, 2057:2001,
             2058:2002, 2059:2003, 2060:2004, 2061:2005, 2062:2006, 2063:2007, 2064:2008, 2065:2009, 2066:2010,
             2067:2011, 2068:2012, 2069:2013, 2070:2014, 2071:2015, 2072:2016, 2073:2017, 2074:2018, 2075:2019,
             2076:2020, 2077:2021, 2014:2014, 2013:2013, 2012:2012, 2006:2006, 2011:2011, 2001:2001, 2010:2010,
             2016:2016, 2005:2005, 2007:2007, 2015:2015, 2009:2009, 2008:2008, 2017:2017, 2002:2002, 2019:2019,
             2018:2018, 1999:1999}

# 2073 data had missing values for four columns so fill it by one static value
data_df.loc[data_df.Date==2073, 'ShiftName'] = 'Missing'
data_df['MunicipalityVdc'] = data_df.MunicipalityVdc.fillna('Missing')
data_df['DistrictName'] = data_df.DistrictName.fillna('Missing')
data_df.loc[data_df.Date==2073, 'HasStudentAttemptedExam'] = 2
data_df['BirthDateBS'] = data_df.BirthDateBS.str.split(' ').str[0]
data_df['BirthDateAD'] = data_df.BirthDateBS.apply(convert_bs_to_ad)

data_df.drop('BirthDateBS', axis='columns', inplace=True)

# For student who have not appeared exam give score as 0 and rank as maximum
data_df['EntranceScore'] = data_df.EntranceScore.fillna(0)
data_df['EntranceRank'] = data_df.EntranceRank.fillna(10000000)

# data_df.dropna(how='any', thresh=25655, axis='columns', inplace=True)
# PCL data are missing in higher percentage
data_df['SLCPassedYear'] = data_df.SLCPassedYear.map(bs_ad_map)
# print(sorted(data_df.columns.values.tolist()))

data_df.dropna(subset=['ShiftName'], inplace=True)
data_df = data_df.drop_duplicates()

profile_report = pandas_profiling.ProfileReport(data_df)
profile_report.to_file('CleanedProfilingReport.html')
data_df.to_csv('data/CleanedData.csv', index=False)
