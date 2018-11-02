import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os.path
import math
df = pd.read_excel('/Users/wcoupe/Documents/git/apreq/data/ZTL_CLT_Apreqs_2018.xlsx')

#df = df[ (df['Destination Airport']=='ATL') & (df['Schedule Delay(s)']<=3600) ].reset_index()
#df = df[ (df['Destination Airport']=='ATL') ].reset_index()



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
		if df.loc[row,'compliance'] == 0:
			df.loc[row,'compliance_whole_min'] = 0
		else:
			val = pd.Timedelta( df.loc[row,'Departed Zulu'] - df.loc[row,'Sched Departure Time Zulu'] ).total_seconds()
			sign = val / float(abs(val))
			df.loc[row,'compliance_whole_min'] = sign * round( abs(pd.Timedelta( df.loc[row,'Departed Zulu'] - df.loc[row,'Sched Departure Time Zulu'] ).total_seconds() / float(60) ) )
		if (df.loc[row,'compliance_whole_min'] >= -2) & (df.loc[row,'compliance_whole_min'] <= 1):
			df.loc[row,'binary_compliance'] = True
		else:
			df.loc[row,'binary_compliance'] = False

	except:
		pass


df_with_neg = df[ df['Schedule Delay(s)']<=1800 ]
df.to_csv('debug_apreq.csv',index=False)
df_negative = df[ df['Schedule Delay(s)']<0 ]
df = df[ (df['Schedule Delay(s)']>=0) & (df['Schedule Delay(s)']<=1800)].reset_index()



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

	df_DAL_negative = df_negative[ df_negative['Carrier'] == 'DAL' ]
	df_AAL_negative = df_negative[ df_negative['Carrier'].isin(['AAL','JIA','RPA','ASQ']) ]
	
	df_summary.loc[idx,'count_aircraft'] = len(df_temp)
	df_summary.loc[idx,'count_negative'] = len(df_negative[ df_negative['month'] == month ])
	df_summary.loc[idx,'binary_compliance'] = len( df_temp[ df_temp['binary_compliance']==True ] ) / float(len(df_temp))
	df_summary.loc[idx,'mean_delay_minutes'] = df_temp['Schedule Delay(s)'].mean() / float(60)
	df_summary.loc[idx,'std_delay_minutes'] = df_temp['Schedule Delay(s)'].std() / float(60)
	df_summary.loc[idx,'first_schedule_count'] = len(df_first)
	df_summary.loc[idx,'first_schedule_mean_delay_minutes'] = df_first['Schedule Delay(s)'].mean() / float(60)
	df_summary.loc[idx,'first_schedule_std_delay_minutes'] = df_first['Schedule Delay(s)'].std() / float(60)
	df_summary.loc[idx,'mean_number_updates'] = df_temp['Num Updates'].mean()
	df_summary.loc[idx,'std_number_updates'] = df_temp['Num Updates'].std()
	#df_summary.loc[idx,'compliance'] = len( df_temp[ (df_temp['compliance_whole_min'] >= -2)& (df_temp['compliance_whole_min'] <= 1)] ) / float(len(df_temp))
	
	
	df_summary.loc[idx,'count_DAL'] = len(df_DAL)
	df_summary.loc[idx,'count_DAL_negative'] = len(df_DAL_negative[ df_DAL_negative['month'] == month ])
	df_summary.loc[idx,'DAL_binary_compliance'] = len( df_DAL[ df_DAL['binary_compliance']==True ] ) / float(len(df_DAL))
	df_summary.loc[idx,'DAL_mean_delay_minutes'] = df_DAL['Schedule Delay(s)'].mean() / float(60)
	df_summary.loc[idx,'DAL_std_delay_minutes'] = df_DAL['Schedule Delay(s)'].std() / float(60)
	df_summary.loc[idx,'DAL_first_schedule_count'] = len(df_DAL_first)
	df_summary.loc[idx,'DAL_first_schedule_mean_delay_minutes'] = df_DAL_first['Schedule Delay(s)'].mean() / float(60)
	df_summary.loc[idx,'DAL_first_schedule_std_delay_minutes'] = df_DAL_first['Schedule Delay(s)'].std() / float(60)
	df_summary.loc[idx,'DAL_mean_number_updates'] = df_DAL['Num Updates'].mean()
	df_summary.loc[idx,'DAL_std_number_updates'] = df_DAL['Num Updates'].std()
	
	df_summary.loc[idx,'count_AAL'] = len(df_AAL)
	df_summary.loc[idx,'count_AAL_negative'] = len(df_AAL_negative[ df_AAL_negative['month']==month ]  )
	df_summary.loc[idx,'AAL_binary_compliance'] = len( df_AAL[ df_AAL['binary_compliance']==True ] ) / float(len(df_AAL))
	df_summary.loc[idx,'AAL_mean_delay_minutes'] = df_AAL['Schedule Delay(s)'].mean() / float(60)
	df_summary.loc[idx,'AAL_std_delay_minutes'] = df_AAL['Schedule Delay(s)'].std() / float(60)
	df_summary.loc[idx,'AAL_first_schedule_count'] = len(df_AAL_first)
	df_summary.loc[idx,'AAL_first_schedule_mean_delay_minutes'] = df_AAL_first['Schedule Delay(s)'].mean() / float(60)
	df_summary.loc[idx,'AAL_first_schedule_std_delay_minutes'] = df_AAL_first['Schedule Delay(s)'].std() / float(60)
	df_summary.loc[idx,'AAL_mean_number_updates'] = df_AAL['Num Updates'].mean()
	df_summary.loc[idx,'AAL_std_number_updates'] = df_AAL['Num Updates'].std()
	

df_summary.to_csv('apreq_delay_metrics_with_negative.csv',index=False)


plt.figure(figsize=(14,10))
plt.subplot(2,1,1)
df_before = df[ df['month'].isin([1,2,3,4,5,6,7,8,9]) ]
df_after = df[ df['month'].isin([10]) ]
plt.hist(df_before['Schedule Delay(s)'] / float(60) , range=[-10,130],bins=60,edgecolor='black',alpha=0.6,normed=True,label='Jan - Sep')
plt.hist(df_after['Schedule Delay(s)'] / float(60) , range=[-10,130],bins=60,edgecolor='black',alpha=0.6,normed=True,label='Oct')
plt.legend()
plt.title('Scheduled Delay from TBFM')

plt.subplot(2,1,2)
df_before = df[ df['month'].isin([1,2,3,4,5,6,7,8,9]) ]
df_after = df[ df['month'].isin([10]) ]
plt.hist(df_before['Num Updates']  , range=[0,10],bins=10,edgecolor='black',alpha=0.6,normed=True,label='Jan - Sep')
plt.hist(df_after['Num Updates'], range=[0,10],bins=10,edgecolor='black',alpha=0.6,normed=True,label='Oct')
plt.title('Number of Reschedules')
plt.legend()
plt.tight_layout()
plt.savefig('apreq_scheduled_delay.png')



plt.figure(figsize=(14,10))



plt.subplot(2,1,1)
df_before = df[ df['month'].isin([1,2,3,4,5,6,7,8,9]) ]
df_after = df[ df['month'].isin([10]) ]
plt.hist(df_before['Schedule Delay(s)'] / float(60) , range=[-10,30],bins=40,edgecolor='black',alpha=0.6,normed=True,label='Jan - Sep')
plt.hist(df_after['Schedule Delay(s)'] / float(60) , range=[-10,30],bins=40,edgecolor='black',alpha=0.6,normed=True,label='Oct')
plt.legend()
plt.title('Scheduled Delay from TBFM')

plt.subplot(2,1,2)
df_before = df[ df['month'].isin([1,2,3,4,5,6,7,8,9]) ]
df_after = df[ df['month'].isin([10]) ]
plt.hist(df_before['Num Updates']  , range=[0,10],bins=10,edgecolor='black',alpha=0.6,normed=True,label='Jan - Sep')
plt.hist(df_after['Num Updates'], range=[0,10],bins=10,edgecolor='black',alpha=0.6,normed=True,label='Oct')
plt.title('Number of Reschedules')
plt.legend()


plt.tight_layout()
plt.savefig('apreq_scheduled_delay_zoomed.png')




############ PLOT WITH NEGATIVE VALUES


df = df_with_neg


plt.figure(figsize=(14,10))
plt.subplot(2,1,1)
df_before = df[ df['month'].isin([1,2,3,4,5,6,7,8,9]) ]
df_after = df[ df['month'].isin([10]) ]
plt.hist(df_before['Schedule Delay(s)'] / float(60) , range=[-30,130],bins=60,edgecolor='black',alpha=0.6,normed=True,label='Jan - Sep')
plt.hist(df_after['Schedule Delay(s)'] / float(60) , range=[-30,130],bins=60,edgecolor='black',alpha=0.6,normed=True,label='Oct')
plt.legend()
plt.title('Scheduled Delay from TBFM')

plt.subplot(2,1,2)
df_before = df[ df['month'].isin([1,2,3,4,5,6,7,8,9]) ]
df_after = df[ df['month'].isin([10]) ]
plt.hist(df_before['Num Updates']  , range=[0,10],bins=10,edgecolor='black',alpha=0.6,normed=True,label='Jan - Sep')
plt.hist(df_after['Num Updates'], range=[0,10],bins=10,edgecolor='black',alpha=0.6,normed=True,label='Oct')
plt.title('Number of Reschedules')
plt.legend()
plt.tight_layout()
plt.savefig('apreq_scheduled_delay_with_negative.png')



plt.figure(figsize=(14,10))



plt.subplot(2,1,1)
df_before = df[ df['month'].isin([1,2,3,4,5,6,7,8,9]) ]
df_after = df[ df['month'].isin([10]) ]
plt.hist(df_before['Schedule Delay(s)'] / float(60) , range=[-10,30],bins=40,edgecolor='black',alpha=0.6,normed=True,label='Jan - Sep')
plt.hist(df_after['Schedule Delay(s)'] / float(60) , range=[-10,30],bins=40,edgecolor='black',alpha=0.6,normed=True,label='Oct')
plt.legend()
plt.title('Scheduled Delay from TBFM')

plt.subplot(2,1,2)
df_before = df[ df['month'].isin([1,2,3,4,5,6,7,8,9]) ]
df_after = df[ df['month'].isin([10]) ]
plt.hist(df_before['Num Updates']  , range=[0,10],bins=10,edgecolor='black',alpha=0.6,normed=True,label='Jan - Sep')
plt.hist(df_after['Num Updates'], range=[0,10],bins=10,edgecolor='black',alpha=0.6,normed=True,label='Oct')
plt.title('Number of Reschedules')
plt.legend()


plt.tight_layout()
plt.savefig('apreq_scheduled_delay_zoomed_with_negative.png')