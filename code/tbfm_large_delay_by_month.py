import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os.path
import math

month_vec = ['01','02','03','04','05','06','07','08','09','10','11']
#month_vec = ['07','08','09','10']

threshold = [10,20,30]
quantile = [0.5,0.75,0.9]

filter_negative = True

# path = '/Users/wcoupe/Documents/flight_summary_v1.0/2018/'
# allFiles = os.listdir(path)

# df_summary = pd.DataFrame()
# idx=-1
# for month in range(len(month_vec)):
# 	path = '/Users/wcoupe/Documents/flight_summary_v1.0/2018/' + str(month_vec[month])
# 	allFiles = os.listdir(path)
# 	indiv_files = []
# 	for file_name in range(len(allFiles)):
# 		if 'KCLT.fullFlightSummary.v1.0' in allFiles[file_name]:
# 			print(allFiles[file_name])
# 			df = pd.read_csv(path + '/' + allFiles[file_name],parse_dates=['apreq_final'])
# 			df = df.assign(apreq_local = df['apreq_final'].dt.tz_localize("UTC").dt.tz_convert("US/Eastern"))
# 			indiv_files.append(df)

# 	df = pd.concat(indiv_files)
# 	df = df[ (df['apreq_final'].notnull()) & (df['arrival_aerodrome_icao_name'] == 'KATL') ].reset_index(drop=True)
# 	#df = df[ (df['apreq_final'].notnull())  ].reset_index(drop=True)
	
# 	for flight in range(len(df)):
# 		idx+=1
# 		ref_time = pd.Timestamp( str(df.loc[flight,'apreq_local']).split(' ')[0] + ' 00:00:00' )
# 		df_summary.loc[idx,'gufi'] = df.loc[flight,'gufi']
# 		df_summary.loc[idx,'arrival_aerodrome_icao_name'] = df.loc[flight,'arrival_aerodrome_icao_name']
# 		df_summary.loc[idx,'month'] = int(month_vec[month])
# 		df_summary.loc[idx,'apreq_relative_local'] = pd.Timedelta( df.loc[flight,'apreq_final'] - ref_time ).total_seconds() / float(60)
# 		df_summary.loc[idx,'apreq_15_minute_index'] = int( math.floor(df_summary.loc[idx,'apreq_relative_local']/15) )
# 		df_summary.loc[idx,'tbfm_assigned_delay'] = df.loc[flight,'tbfm_assigned_delay'] / float(60)
# 		df_summary.loc[idx,'apreq_num_updates'] = df.loc[flight,'apreq_num_updates']
# 		df_summary.loc[idx,'apreq_compliance_sec'] = df.loc[flight,'apreq_compliance_sec']
# 		df_summary.loc[idx,'apreq_compliance_truncated_sec'] = df.loc[flight,'apreq_compliance_truncated_sec']
# 		df_summary.loc[idx,'apreq_compliant'] = df.loc[flight,'apreq_compliant']
# 		df_summary.loc[idx,'apreq_prescheduled'] = df.loc[flight,'apreq_prescheduled']
# 		df_summary.loc[idx,'eobt_at_preschedule'] = df.loc[flight,'eobt_at_preschedule']
# 		df_summary.loc[idx,'pilot_ready_time'] = df.loc[flight,'pilot_ready_time']
# 		df_summary.loc[idx,'departure_stand_actual_time'] = df.loc[flight,'departure_stand_actual_time']


# df_summary.to_csv('apreq_times.csv',index=False)

df_summary = pd.read_csv('apreq_times.csv')

max_index = int(df_summary['apreq_15_minute_index'].max())


above = np.zeros((len(threshold),len(month_vec)))
q = np.zeros((len(quantile),len(month_vec)))
avg_delay = np.zeros(len(month_vec))
count = np.zeros(len(month_vec))
count_neg = np.zeros(len(month_vec))

for month in range(len(month_vec)):
	df_temp = df_summary[ (df_summary['month'] == int(month_vec[month]) )]
	if filter_negative:
		df_temp = df_temp[ df_temp['tbfm_assigned_delay']>=0]
	for value in range(len(threshold)):
		# above[value,month] = len( df_summary[ (df_summary['month'] == int(month_vec[month]) ) & (df_summary['tbfm_assigned_delay'] >= threshold[value]) ] ) / float(len( df_summary[ (df_summary['month'] == int(month_vec[month]) )]  ))
		above[value,month] = len(df_temp[ df_temp['tbfm_assigned_delay'] >= threshold[value] ]) / float(len(df_temp))
	
	for q_val in range(len(quantile)):
		q[q_val,month] = df_temp['tbfm_assigned_delay'].quantile( quantile[q_val] )

	avg_delay[month] = df_temp['tbfm_assigned_delay'].mean()
	count[month] = len(df_temp)
	count_neg[month] = len( df_temp[ df_temp['tbfm_assigned_delay'] < 0] )



plt.figure(figsize=(14,10))

plt.subplot(3,1,1)
plt.bar(np.arange(len(month_vec)),count,color='green',alpha=0.5,edgecolor='black',label='Count of Flights')
plt.bar(np.arange(len(month_vec)),count_neg,color='green',alpha=0.8,edgecolor='black',label='Count of Flights: TBFM Delay < 0')
plt.grid(True,alpha=0.5)
plt.xticks(np.arange(len(month_vec)), month_vec)
plt.legend(loc='upper left',fontsize=7)
plt.ylabel('Count')
plt.title('Flight Counts')


plt.subplot(3,1,2)
for q_val in range(len(quantile)):	
	plt.bar( np.arange(len(month_vec)) , q[q_val,:],alpha = 0.8 / float(1+q_val),color='purple' , edgecolor='black',label='Quantile ' + str(quantile[q_val]) )


plt.plot(np.arange(len(month_vec)) ,avg_delay,'-',marker='d',markersize=9,markeredgecolor='black',color='purple' ,label='Mean' )
plt.legend(loc='upper left',fontsize=7)
plt.grid(True,alpha=0.5)
plt.xticks(np.arange(len(month_vec)), month_vec)
plt.ylabel('TBFM Delay [Minutes]')
plt.title('TBFM Assigned Delay')
#plt.ylim([0,23])

for value in range(len(threshold)):

	plt.subplot(3,1,3)
	plt.plot(above[value,:],marker='o',linewidth=3,markersize=13,markeredgecolor='black',alpha=0.7,label='Percentage TBFM Delay > ' + str(threshold[value]) + ' Minutes')
	plt.ylabel('Percentage Above Threshold Value')
	plt.xlabel('Month')
	plt.legend(loc='upper left',fontsize=7)
	plt.grid(True,alpha=0.6)
	plt.xticks(np.arange(len(month_vec)), month_vec)
	plt.title('Percentage of Flights Experiencing TBFM Assigned Delay Above Threshold')
#plt.ylim([-0.05,.25])

plt.tight_layout()
if filter_negative:
	plt.savefig('tbfm_assigned_delay_no_negative.png')
else:
	plt.savefig('tbfm_assigned_delay_with_negative.png')