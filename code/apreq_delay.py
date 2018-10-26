import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os.path
import math
df = pd.read_excel('/Users/wcoupe/Documents/git/apreq/data/ZTL_CLT_Apreqs_2018.xlsx')

#df = df[ (df['Destination Airport']=='ATL') & (df['Schedule Delay(s)']<=3600) ].reset_index()
df = df[ (df['Destination Airport']=='ATL') & (df['Schedule Delay(s)']>=0)& (df['Schedule Delay(s)']<=1800) ].reset_index()



month_vec = np.arange(10) +1

df_summary = pd.DataFrame()

path = '/Users/wcoupe/Documents/git/apreq/data/'
allFiles = glob.glob(os.path.join(path, "**","ztl_compliance_*.csv"),recursive=True)


index_val = len(df)

for f in allFiles:
	if 'ztl_compliance_' in f:
		df0 = pd.read_csv(f)
		for row in range(len(df0['Callsign'])):
			index_val +=1
			df.loc[index_val,'Acid'] = df0.loc[row,'Callsign']
			df.loc[index_val,'Sched Departure Time Zulu'] = pd.Timestamp(df0.loc[row,'APREQ Time'])
			df.loc[index_val,'Departed Zulu'] = pd.Timestamp(df0.loc[row,'Estimated Wheels Off'])
			df.loc[index_val,'debug_compliance'] = df0.loc[row,'Compliance (minutes)']
			df.loc[index_val,'Schedule Delay(s)'] = df0.loc[row,'TBFM Assigned Delay (minutes)'] * 60
			df.loc[index_val,'Carrier'] = str(df0.loc[row,'Callsign'] )[0:3]
			df.loc[index_val,'Num Updates'] = df0.loc[row,'Number of APREQ Updates']
df = df.reset_index(drop=True)

for row in range(len(df['Sched Departure Time Zulu'])):
	try:
		df.loc[row,'month'] = int(df.loc[row,'Sched Departure Time Zulu'].month)
	except:
		pass

	try:
		df.loc[row,'compliance'] = pd.Timedelta( df.loc[row,'Departed Zulu'] - df.loc[row,'Sched Departure Time Zulu'] ).total_seconds()
		df.loc[row,'compliance_whole_min'] = math.floor( pd.Timedelta( df.loc[row,'Departed Zulu'] - df.loc[row,'Sched Departure Time Zulu'] ).total_seconds() / float(60) )
	except:
		pass



df.to_csv('debug.csv')

idx=-1
for month in month_vec:
	idx+=1
	df_temp = df[df['month']==month]
	df_first = df_temp[ df_temp['Num Updates'] == 0 ]
	df_DAL = df_temp[df_temp['Carrier'] == 'DAL' ]
	df_DAL_first = df_first[  df_first['Carrier'] == 'DAL']
	df_AAL = df_temp[df_temp['Carrier'].isin(['AAL','JIA','RPA','ASQ'])]
	df_AAL_first = df_first[  df_first['Carrier'].isin(['AAL','JIA','RPA','ASQ'])]
	df_summary.loc[idx,'month'] = month
	
	df_summary.loc[idx,'count_aircraft'] = len(df_temp)
	df_summary.loc[idx,'mean_delay_minutes'] = df_temp['Schedule Delay(s)'].mean() / float(60)
	df_summary.loc[idx,'std_delay_minutes'] = df_temp['Schedule Delay(s)'].std() / float(60)
	df_summary.loc[idx,'first_schedule_count'] = len(df_first)
	df_summary.loc[idx,'first_schedule_mean_delay_minutes'] = df_first['Schedule Delay(s)'].mean() / float(60)
	df_summary.loc[idx,'first_schedule_std_delay_minutes'] = df_first['Schedule Delay(s)'].std() / float(60)
	df_summary.loc[idx,'mean_number_updates'] = df_temp['Num Updates'].mean()
	df_summary.loc[idx,'std_number_updates'] = df_temp['Num Updates'].std()
	df_summary.loc[idx,'compliance'] = len( df_temp[ (df_temp['compliance'] >= -120)& (df_temp['compliance'] <= 60)] ) / float(len(df_temp))
	
	df_summary.loc[idx,'count_DAL'] = len(df_DAL)
	df_summary.loc[idx,'DAL_mean_delay_minutes'] = df_DAL['Schedule Delay(s)'].mean() / float(60)
	df_summary.loc[idx,'DAL_std_delay_minutes'] = df_DAL['Schedule Delay(s)'].std() / float(60)
	df_summary.loc[idx,'DAL_first_schedule_count'] = len(df_DAL_first)
	df_summary.loc[idx,'DAL_first_schedule_mean_delay_minutes'] = df_DAL_first['Schedule Delay(s)'].mean() / float(60)
	df_summary.loc[idx,'DAL_first_schedule_std_delay_minutes'] = df_DAL_first['Schedule Delay(s)'].std() / float(60)
	df_summary.loc[idx,'DAL_mean_number_updates'] = df_DAL['Num Updates'].mean()
	df_summary.loc[idx,'DAL_std_number_updates'] = df_DAL['Num Updates'].std()
	
	df_summary.loc[idx,'count_AAL'] = len(df_AAL)
	df_summary.loc[idx,'AAL_mean_delay_minutes'] = df_AAL['Schedule Delay(s)'].mean() / float(60)
	df_summary.loc[idx,'AAL_std_delay_minutes'] = df_AAL['Schedule Delay(s)'].std() / float(60)
	df_summary.loc[idx,'AAL_first_schedule_count'] = len(df_AAL_first)
	df_summary.loc[idx,'AAL_first_schedule_mean_delay_minutes'] = df_AAL_first['Schedule Delay(s)'].mean() / float(60)
	df_summary.loc[idx,'AAL_first_schedule_std_delay_minutes'] = df_AAL_first['Schedule Delay(s)'].std() / float(60)
	df_summary.loc[idx,'AAL_mean_number_updates'] = df_AAL['Num Updates'].mean()
	df_summary.loc[idx,'AAL_std_number_updates'] = df_AAL['Num Updates'].std()
	

df_summary.to_csv('apreq_delay_metrics.csv',index=False)