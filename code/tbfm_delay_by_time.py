import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os.path
import math

month_vec = ['07','08','09','10']

x_tick = []
x_id = []
for i in range(24*4 + 1):
	if i % 4 == 0:
		x_tick.append(int(i/4))
		x_id.append(x_tick[-1]*4)



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
	
# 	for flight in range(len(df)):
# 		idx+=1
# 		ref_time = pd.Timestamp( str(df.loc[flight,'apreq_local']).split(' ')[0] + ' 00:00:00' )
# 		df_summary.loc[idx,'gufi'] = df.loc[flight,'gufi']
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


for month in range(len(month_vec)):
	count_apreq = np.zeros(max_index + 1)
	avg_tbfm_delay = np.zeros(max_index + 1)
	std_tbfm_delay = np.zeros(max_index + 1)
	plt.figure(figsize=(14,10))
	for index in range(96):
		df_temp = df_summary[ (df_summary['month'] == int(month_vec[month]) ) & (df_summary['apreq_15_minute_index'] == index) ]
		
		if filter_negative:
			df_temp = df_temp[ df_temp['tbfm_assigned_delay'] >= 0 ]
		if len(df_temp) > 0:
			avg_tbfm_delay[index] = df_temp['tbfm_assigned_delay'].mean()
			std_tbfm_delay[index] = df_temp['tbfm_assigned_delay'].std()
			count_apreq[index] = len(df_temp)

	
	plt.subplot(3,1,1)
	plt.bar(np.arange(len(count_apreq)),count_apreq,alpha=0.3,edgecolor='black',label=month_vec[month])
	plt.xlabel('Apreq Final Local Time')
	plt.ylabel('Count')
	plt.title('Number of Apreq Flights')
	plt.xticks(x_id,x_tick)
	plt.legend()
	plt.grid(True,alpha=0.6)
	plt.xlim([0,97])

	plt.subplot(3,1,2)
	plt.bar(np.arange(len(avg_tbfm_delay)),avg_tbfm_delay,alpha=0.3,edgecolor='black',label=month_vec[month])
	plt.xlabel('Apreq Final Local Time')
	plt.ylabel('TBFM Assigned Delay [Minutes]')
	plt.title('Average TBFM Assigned Delay')
	plt.xticks(x_id,x_tick)
	plt.grid(True,alpha=0.6)
	plt.ylim([0,40])
	plt.xlim([0,97])

	plt.subplot(3,1,3)
	plt.bar(np.arange(len(std_tbfm_delay)),std_tbfm_delay,alpha=0.3,edgecolor='black',label=month_vec[month])
	plt.xlabel('Apreq Final Local Time')
	plt.ylabel('TBFM Assigned Delay [Minutes]')
	plt.title('Standard Deviation TBFM Assigned Delay')
	plt.xticks(x_id,x_tick)
	plt.grid(True,alpha=0.6)
	plt.ylim([0,30])
	plt.xlim([0,97])


	plt.tight_layout()
	if filter_negative:
		plt.savefig('Apreq_Delay_Local_Time_Month_' + str(month_vec[month]) + '_No_Negative.png')
	else:
		plt.savefig('Apreq_Delay_Local_Time_Month_' + str(month_vec[month]) + '.png')
	#plt.close('all')




