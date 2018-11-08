import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os.path
import math

df_summary = pd.DataFrame()

path = '/Users/wcoupe/Documents/git/apreq/data/'
allFiles = glob.glob(os.path.join(path, "**","ztl_compliance_*.csv"),recursive=True)

indiv_files = []
for f in allFiles:
	if 'ztl_compliance_' in f:
		df = pd.read_csv(f,parse_dates=['Actual Pushback','EOBT at Pre-Schedule'])
		indiv_files.append(df)
df = pd.concat(indiv_files)
df = df.reset_index(drop=True)

for row in range(len(df)):
	df.loc[row,'eobt_compliance'] = pd.Timedelta( pd.Timestamp(df.loc[row,'Actual Pushback']) - pd.Timestamp(df.loc[row,'EOBT at Pre-Schedule'])).total_seconds() / float(60)
	df.loc[row,'eobt_change'] = pd.Timedelta( pd.Timestamp(df.loc[row,'EOBT at Pushback']) - pd.Timestamp(df.loc[row,'EOBT at Pre-Schedule'])).total_seconds() / float(60)
df = df[ df['Release Type'] == 'APREQ' ]

df_pre_schedule = df[ df['Pre-Scheduled']==True ]
df_no_pre_schedule = df[ df['Pre-Scheduled']==False ]


print('THIS IS NUMBER OF PRESCHEDULE')
print(len(df_pre_schedule))
print('THIS IS NUMBER OF NON PRESCHEDULE')
print(len(df_no_pre_schedule))

#########################################################
#########################################################
#########################################################
##################### NEW FIGURE ########################
#########################################################
#########################################################
#########################################################


plt.figure(figsize=(16,10))

df_no_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] == 0]
df_with_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] > 0]
compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_label = 'No APREQ Updates: Percent = ' + str(len(df_no_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', APREQ Compliance = ' + str(compliance_no_update)[0:4] 
update_label = 'APREQ Updates: Percent = ' + str(len(df_with_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', APREQ Compliance = ' + str(compliance_update)[0:4] 
plt.subplot2grid((4,8), (0,2), rowspan=3, colspan=6)
plt.plot( df_no_update['eobt_compliance'] , df_no_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.4,color='blue', label=no_update_label ,markeredgecolor='black' )
plt.plot( df_with_update['eobt_compliance'] , df_with_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.4,color='orange',label=update_label,markeredgecolor='black' )
plt.xlim([-10,20])
plt.ylim([-10,10])
#plt.xlabel('<Actual Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)
#plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)
plt.title('Pre-Schedule = TRUE',fontsize=18)
plt.grid(True,alpha=0.5)
plt.legend()





plt.subplot2grid((4,8), (0,0), rowspan=3, colspan=2)
compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_mean = str(df_no_update['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['Compliance (minutes)'].std())[0:4]
update_mean = str(df_with_update['Compliance (minutes)'].mean())[0:4]
update_std = str(df_with_update['Compliance (minutes)'].std())[0:4]
no_update_label = 'No APREQ Updates: Mean = ' + no_update_mean + ', STD = ' + no_update_std 
update_label = 'APREQ Updates: Mean = ' + update_mean + ', STD = ' + update_std 
n,bins,patches = plt.hist(df_no_update['Compliance (minutes)'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,10],bins=20,orientation='horizontal' ,align='left')
n2,bins,patches = plt.hist(df_with_update['Compliance (minutes)'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,10],bins=20, orientation='horizontal' ,align='left')
#print(n)
max1 = max(n)
max2 = max(n2)
#plt.ylim([0,1.2*max([max1,max2])])
plt.legend()
plt.ylim([-10,10])
plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)



plt.subplot2grid((4,8), (3,2), rowspan=1, colspan=6)
no_update_mean = str(df_no_update['eobt_compliance'].mean())[0:4]
no_update_std = str(df_no_update['eobt_compliance'].std())[0:4]
update_mean = str(df_with_update['eobt_compliance'].mean())[0:4]
update_std = str(df_with_update['eobt_compliance'].std())[0:4]
no_update_label = 'No APREQ Updates: Mean = ' + no_update_mean + ', STD = ' + no_update_std 
update_label = 'APREQ Updates: Mean = ' + update_mean + ', STD = ' + update_std 
n,bins,patches = plt.hist(df_no_update['eobt_compliance'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,20],bins=30,orientation='vertical',align='left')
n2,bins,patches = plt.hist(df_with_update['eobt_compliance'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,20],bins=30, orientation='vertical',align='left')
plt.legend()
plt.xlim([-10,20])
plt.xlabel('<Actual Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)

plt.tight_layout()
plt.savefig('apreq_eobt_compliance_detailed.png')




#########################################################
#########################################################
#########################################################
##################### NEW FIGURE ########################
#########################################################
#########################################################
#########################################################




plt.figure(figsize=(16,10))



df_no_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] == 0]
df_with_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] > 0]

compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_label = 'No APREQ Updates: Percent = ' + str(len(df_no_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', APREQ Compliance = ' + str(compliance_no_update)[0:4] 
update_label = 'APREQ Updates: Percent = ' + str(len(df_with_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', APREQ Compliance = ' + str(compliance_update)[0:4] 
plt.subplot2grid((4,8), (0,2), rowspan=3, colspan=6)
plt.plot( df_no_update['eobt_compliance'] , df_no_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.4,color='blue', label=no_update_label ,markeredgecolor='black' )
plt.plot( df_with_update['eobt_compliance'] , df_with_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.4,color='orange',label=update_label,markeredgecolor='black' )
plt.xlim([-10,120])
plt.ylim([-10,10])
#plt.xlabel('<Actual Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)
#plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)
plt.title('Pre-Schedule = TRUE',fontsize=18)
plt.grid(True,alpha=0.5)
plt.legend()




plt.subplot2grid((4,8), (0,0), rowspan=3, colspan=2)
compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_mean = str(df_no_update['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['Compliance (minutes)'].std())[0:4]
update_mean = str(df_with_update['Compliance (minutes)'].mean())[0:4]
update_std = str(df_with_update['Compliance (minutes)'].std())[0:4]
no_update_label = 'No APREQ Updates: Mean = ' + no_update_mean + ', STD = ' + no_update_std 
update_label = 'APREQ Updates: Mean = ' + update_mean + ', STD = ' + update_std 
n,bins,patches = plt.hist(df_no_update['Compliance (minutes)'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,10],bins=20,orientation='horizontal' ,align='left')
n2,bins,patches = plt.hist(df_with_update['Compliance (minutes)'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,10],bins=20, orientation='horizontal',align='left')
#print(n)
max1 = max(n)
max2 = max(n2)
#plt.ylim([0,1.2*max([max1,max2])])
plt.legend()
plt.ylim([-10,10])
plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)



plt.subplot2grid((4,8), (3,2), rowspan=1, colspan=6)
no_update_mean = str(df_no_update['eobt_compliance'].mean())[0:4]
no_update_std = str(df_no_update['eobt_compliance'].std())[0:4]
update_mean = str(df_with_update['eobt_compliance'].mean())[0:4]
update_std = str(df_with_update['eobt_compliance'].std())[0:4]
no_update_label = 'No APREQ Updates: Mean = ' + no_update_mean + ', STD = ' + no_update_std 
update_label = 'APREQ Updates: Mean = ' + update_mean + ', STD = ' + update_std 
n,bins,patches = plt.hist(df_no_update['eobt_compliance'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,120],bins=130,orientation='vertical',align='left')
n2,bins,patches = plt.hist(df_with_update['eobt_compliance'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,120],bins=130, orientation='vertical',align='left')
plt.legend()
plt.xlim([-10,120])
plt.xlabel('<Actual Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)



plt.tight_layout()
plt.savefig('apreq_eobt_compliance_detailed_v2.png')






#########################################################
#########################################################
#########################################################
##################### NEW FIGURE ########################
#########################################################
#########################################################
#########################################################





plt.figure(figsize=(16,10))

df_no_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] == 0]
df_with_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] > 0]
compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_mean = str(df_no_update['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['Compliance (minutes)'].std())[0:4]
update_mean = str(df_with_update['Compliance (minutes)'].mean())[0:4]
update_std = str(df_with_update['Compliance (minutes)'].std())[0:4]
no_update_label = 'No APREQ Updates: Percent = ' + str(len(df_no_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_no_update)[0:4]
update_label = 'APREQ Updates: Percent = ' + str(len(df_with_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4]
plt.subplot2grid((4,16), (0,2), rowspan=3, colspan=6)
plt.plot( df_no_update['Number of APREQ Updates'] , df_no_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='blue', label=no_update_label ,markeredgecolor='black' )
plt.plot( df_with_update['Number of APREQ Updates'] , df_with_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='orange',label=update_label,markeredgecolor='black' )
plt.xlim([-1,6])
plt.ylim([-10,10])
# plt.xlabel('Number of APREQ Updates [Count]',fontsize=12)
# plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)
plt.grid(True,alpha=0.5)
plt.title('Pre-Schedule = TRUE',fontsize=18)
plt.legend(fontsize=10)

plt.subplot2grid((4,16), (0,0), rowspan=3, colspan=2)
compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_mean = str(df_no_update['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['Compliance (minutes)'].std())[0:4]
update_mean = str(df_with_update['Compliance (minutes)'].mean())[0:4]
update_std = str(df_with_update['Compliance (minutes)'].std())[0:4]
no_update_label = 'No APREQ Updates: Percent = ' + str(len(df_no_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_no_update)[0:4]
update_label = 'APREQ Updates: Percent = ' + str(len(df_with_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4]
n,bins,patches = plt.hist(df_no_update['Compliance (minutes)'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,10],bins=20 ,orientation='horizontal' ,align='left')
n2,bins,patches = plt.hist(df_with_update['Compliance (minutes)'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,10],bins=20 ,orientation='horizontal' ,align='left')

max1 = max(n)
max2 = max(n2)
#plt.ylim([0,1.2*max([max1,max2])])
#plt.legend()
plt.ylim([-10,10])
plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)


df_no_update = df_no_pre_schedule[ df_no_pre_schedule['Number of APREQ Updates'] == 0]
df_with_update = df_no_pre_schedule[ df_no_pre_schedule['Number of APREQ Updates'] > 0]
compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_mean = str(df_no_update['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['Compliance (minutes)'].std())[0:4]
update_mean = str(df_with_update['Compliance (minutes)'].mean())[0:4]
update_std = str(df_with_update['Compliance (minutes)'].std())[0:4]
no_update_label = 'No APREQ Updates: Percent = ' + str(len(df_no_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_no_update)[0:4] 
update_label = 'APREQ Updates: Percent = ' + str(len(df_with_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4] 
plt.subplot2grid((4,16), (0,8), rowspan=3, colspan=6)
plt.plot( df_no_update['Number of APREQ Updates'] , df_no_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='blue', label=no_update_label ,markeredgecolor='black' )
plt.plot( df_with_update['Number of APREQ Updates'] , df_with_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='orange',label=update_label,markeredgecolor='black' )
plt.xlim([-1,6])
plt.ylim([-10,10])
# plt.xlabel('Number of APREQ Updates [Count]',fontsize=12)
# plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)
plt.grid(True,alpha=0.5)
plt.title('Pre-Schedule = False',fontsize=18)
plt.legend(fontsize=10)

plt.subplot2grid((4,16), (0,14), rowspan=3, colspan=2)
compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_mean = str(df_no_update['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['Compliance (minutes)'].std())[0:4]
update_mean = str(df_with_update['Compliance (minutes)'].mean())[0:4]
update_std = str(df_with_update['Compliance (minutes)'].std())[0:4]
no_update_label = 'No APREQ Updates: Percent = ' + str(len(df_no_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_no_update)[0:4] + ', Mean = ' + no_update_mean + ', STD = ' + no_update_std 
update_label = 'APREQ Updates: Percent = ' + str(len(df_with_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4] + ', Mean = ' + update_mean + ', STD = ' + update_std 
n,bins,patches = plt.hist(df_no_update['Compliance (minutes)'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,10],bins=20,orientation='horizontal',align='left')
n2,bins,patches = plt.hist(df_with_update['Compliance (minutes)'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,10],bins=20 ,orientation='horizontal',align='left')

# max1 = max(n)
# max2 = max(n2)
# plt.ylim([0,1.2*max([max1,max2])])
# plt.legend()
plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)
plt.ylim([-10,10])




df_no_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] == 0]
df_with_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] > 0]

plt.subplot2grid((4,16), (3,2), rowspan=1, colspan=6)
n,bins,patches = plt.hist(df_no_update['Number of APREQ Updates'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,10],bins=20,orientation='vertical',align='left')
n2,bins,patches = plt.hist(df_with_update['Number of APREQ Updates'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,10],bins=20 ,orientation='vertical' ,align='left')
plt.xlim([-1,6])
plt.xlabel('Number of APREQ Updates [Count]',fontsize=12)




df_no_update = df_no_pre_schedule[ df_no_pre_schedule['Number of APREQ Updates'] == 0]
df_with_update = df_no_pre_schedule[ df_no_pre_schedule['Number of APREQ Updates'] > 0]

plt.subplot2grid((4,16), (3,8), rowspan=1, colspan=6)
n,bins,patches = plt.hist(df_no_update['Number of APREQ Updates'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,10],bins=20,orientation='vertical' ,align='left')
n2,bins,patches = plt.hist(df_with_update['Number of APREQ Updates'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,10],bins=20 ,orientation='vertical',align='left')
plt.xlim([-1,6])
plt.xlabel('Number of APREQ Updates [Count]',fontsize=12)


plt.tight_layout()
plt.savefig('apreq_number_updates_compliance_detailed.png')








#########################################################
#########################################################
#########################################################
##################### NEW FIGURE ########################
#########################################################
#########################################################
#########################################################


plt.figure(figsize=(16,10))

df_no_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] == 0]
df_with_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] > 0]

compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_mean = str(df_no_update['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['Compliance (minutes)'].std())[0:4]
update_mean = str(df_with_update['Compliance (minutes)'].mean())[0:4]
update_std = str(df_with_update['Compliance (minutes)'].std())[0:4]
no_update_label = 'No APREQ Updates: Percent = ' + str(len(df_no_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_no_update)[0:4] 
update_label = 'APREQ Updates: Percent = ' + str(len(df_with_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4] 

plt.subplot2grid((4,16), (0,2), rowspan=3, colspan=6)
plt.plot( df_no_update['TBFM Assigned Delay (minutes)'] , df_no_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.4,color='blue', label=no_update_label ,markeredgecolor='black' )
plt.plot( df_with_update['TBFM Assigned Delay (minutes)'] , df_with_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.4,color='orange',label=update_label,markeredgecolor='black' )
plt.xlim([-35,35])
plt.ylim([-10,10])
# plt.xlabel('TBFM Assigned Delay [Minutes]',fontsize=12)
# plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)
plt.title('Pre-Schedule = TRUE',fontsize=18)
plt.grid(True,alpha=0.5)
plt.legend()

plt.subplot2grid((4,16), (0,0), rowspan=3, colspan=2)
compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_mean = str(df_no_update['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['Compliance (minutes)'].std())[0:4]
update_mean = str(df_with_update['Compliance (minutes)'].mean())[0:4]
update_std = str(df_with_update['Compliance (minutes)'].std())[0:4]
no_update_label = 'No APREQ Updates: Percent = ' + str(len(df_no_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_no_update)[0:4] + ', Mean = ' + no_update_mean + ', STD = ' + no_update_std 
update_label = 'APREQ Updates: Percent = ' + str(len(df_with_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4] + ', Mean = ' + update_mean + ', STD = ' + update_std 


n,bins,patches = plt.hist(df_no_update['Compliance (minutes)'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,10],bins=20,orientation='horizontal',align='left')
n2,bins,patches = plt.hist(df_with_update['Compliance (minutes)'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,10],bins=20,orientation='horizontal',align='left')
max1 = max(n)
max2 = max(n2)
#plt.ylim([0,1.2*max([max1,max2])])
#plt.legend()
plt.ylim([-10,10])
plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)


df_no_update = df_no_pre_schedule[ df_no_pre_schedule['Number of APREQ Updates'] == 0]
df_with_update = df_no_pre_schedule[ df_no_pre_schedule['Number of APREQ Updates'] > 0]
compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_mean = str(df_no_update['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['Compliance (minutes)'].std())[0:4]
update_mean = str(df_with_update['Compliance (minutes)'].mean())[0:4]
update_std = str(df_with_update['Compliance (minutes)'].std())[0:4]
no_update_label = 'No APREQ Updates: Percent = ' + str(len(df_no_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_no_update)[0:4] 
update_label = 'APREQ Updates: Percent = ' + str(len(df_with_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4] 

plt.subplot2grid((4,16), (0,8), rowspan=3, colspan=6)
plt.plot( df_no_update['TBFM Assigned Delay (minutes)'] , df_no_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.4,color='blue', label=no_update_label ,markeredgecolor='black' )
plt.plot( df_with_update['TBFM Assigned Delay (minutes)'] , df_with_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.4,color='orange',label=update_label,markeredgecolor='black' )
plt.xlim([-35,35])
plt.ylim([-10,10])
plt.grid(True,alpha=0.5)
# plt.xlabel('TBFM Assigned Delay [Minutes]',fontsize=12)
# plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)
plt.title('Pre-Schedule = False',fontsize=18)
plt.legend()

plt.subplot2grid((4,16), (0,14), rowspan=3, colspan=2)
compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_mean = str(df_no_update['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['Compliance (minutes)'].std())[0:4]
update_mean = str(df_with_update['Compliance (minutes)'].mean())[0:4]
update_std = str(df_with_update['Compliance (minutes)'].std())[0:4]
no_update_label = 'No APREQ Updates: Percent = ' + str(len(df_no_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_no_update)[0:4] + ', Mean = ' + no_update_mean + ', STD = ' + no_update_std 
update_label = 'APREQ Updates: Percent = ' + str(len(df_with_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4] + ', Mean = ' + update_mean + ', STD = ' + update_std 


n,bins,patches = plt.hist(df_no_update['Compliance (minutes)'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,10],bins=20,orientation='horizontal',align='left')
n2,bins,patches = plt.hist(df_with_update['Compliance (minutes)'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,10],bins=20,orientation='horizontal' ,align='left')
max1 = max(n)
max2 = max(n2)
#plt.ylim([0,1.2*max([max1,max2])])

#plt.legend()
plt.ylim([-10,10])
plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)





df_no_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] == 0]
df_with_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] > 0]

no_update_mean = str(df_no_update['TBFM Assigned Delay (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['TBFM Assigned Delay (minutes)'].std())[0:4]
update_mean = str(df_with_update['TBFM Assigned Delay (minutes)'].mean())[0:4]
update_std = str(df_with_update['TBFM Assigned Delay (minutes)'].std())[0:4]
no_update_label = 'No APREQ Updates: Mean = ' + no_update_mean + ', STD = ' + no_update_std 
update_label = 'APREQ Updates: Mean = ' + update_mean + ', STD = ' + update_std 

plt.subplot2grid((4,16), (3,2), rowspan=1, colspan=6)
n,bins,patches = plt.hist(df_no_update['TBFM Assigned Delay (minutes)'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-35,35],bins=70,orientation='vertical',align='left')
n2,bins,patches = plt.hist(df_with_update['TBFM Assigned Delay (minutes)'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-35,35],bins=70 ,orientation='vertical' ,align='left')
plt.xlim([-35,35])
plt.xlabel('TBFM Assigned Delay [Minutes]',fontsize=12)
plt.legend()
max1 = max(n)
max2 = max(n2)
plt.ylim([0,1.6*max([max1,max2])])



df_no_update = df_no_pre_schedule[ df_no_pre_schedule['Number of APREQ Updates'] == 0]
df_with_update = df_no_pre_schedule[ df_no_pre_schedule['Number of APREQ Updates'] > 0]

no_update_mean = str(df_no_update['TBFM Assigned Delay (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['TBFM Assigned Delay (minutes)'].std())[0:4]
update_mean = str(df_with_update['TBFM Assigned Delay (minutes)'].mean())[0:4]
update_std = str(df_with_update['TBFM Assigned Delay (minutes)'].std())[0:4]
no_update_label = 'No APREQ Updates: Mean = ' + no_update_mean + ', STD = ' + no_update_std 
update_label = 'APREQ Updates: Mean = ' + update_mean + ', STD = ' + update_std

plt.subplot2grid((4,16), (3,8), rowspan=1, colspan=6)
n,bins,patches = plt.hist(df_no_update['TBFM Assigned Delay (minutes)'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-35,35],bins=70,orientation='vertical' ,align='left')
n2,bins,patches = plt.hist(df_with_update['TBFM Assigned Delay (minutes)'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-35,35],bins=70 ,orientation='vertical',align='left')
plt.xlim([-35,35])
plt.xlabel('TBFM Assigned Delay [Minutes]',fontsize=12)

plt.legend()
max1 = max(n)
max2 = max(n2)
plt.ylim([0,1.6*max([max1,max2])])

plt.tight_layout()
plt.savefig('apreq_delay_compliance_detailed.png')





#########################################################
#########################################################
#########################################################
##################### NEW FIGURE ########################
#########################################################
#########################################################
#########################################################



plt.figure(figsize=(16,10))

df_no_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] == 0]
df_with_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] > 0]

no_update_mean = str(df_no_update['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['Compliance (minutes)'].std())[0:4]
update_mean = str(df_with_update['Compliance (minutes)'].mean())[0:4]
update_std = str(df_with_update['Compliance (minutes)'].std())[0:4]
no_update_label = 'No APREQ Updates: Percent = ' + str(len(df_no_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_no_update)[0:4] + ', Mean = ' + no_update_mean + ', STD = ' + no_update_std 
update_label = 'APREQ Updates: Percent = ' + str(len(df_with_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4] + ', Mean = ' + update_mean + ', STD = ' + update_std 


plt.subplot2grid((4,8), (0,2), rowspan=3, colspan=6)
plt.plot( df_no_update['eobt_compliance'],df_no_update['Number of APREQ Updates'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='blue', label=no_update_label ,markeredgecolor='black' )
plt.plot(   df_with_update['eobt_compliance'],df_with_update['Number of APREQ Updates'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='orange',label=update_label,markeredgecolor='black' )
plt.xlim([-10,120])
plt.ylim([-1,9])
plt.grid(True,alpha=0.5)
#plt.ylabel('Number of APREQ Updates [Count]',fontsize=12)
#plt.xlabel('<Actual Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)
plt.title('Pre-Schedule = TRUE',fontsize=18)
plt.legend()

plt.subplot2grid((4,8), (3,2), rowspan=1, colspan=6)
#compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
#compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_label = 'No APREQ Updates: Mean = ' + str(df_no_update['eobt_compliance'].mean())[0:4] + ', STD = ' + str(df_no_update['eobt_compliance'].std())[0:4]
update_label = 'APREQ Updates: Mean = ' + str(df_with_update['eobt_compliance'].mean())[0:4] + ', STD = ' + str(df_with_update['eobt_compliance'].std())[0:4]
plt.hist(df_no_update['eobt_compliance'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,120],bins=130 )
plt.hist(df_with_update['eobt_compliance'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,120],bins=130 )
plt.legend()
plt.xlim([-10,120])
plt.xlabel('<Actual Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)






plt.subplot2grid((4,8), (0,0), rowspan=3, colspan=2)
df_no_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] == 0]
df_with_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] > 0]

n,bins,patches = plt.hist(df_no_update['Number of APREQ Updates'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-1,9],bins=10,orientation='horizontal' ,align='left')
n2,bins,patches = plt.hist(df_with_update['Number of APREQ Updates'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-1,9],bins=10 ,orientation='horizontal',align='left')
plt.ylim([-1,9])
plt.ylabel('Number of APREQ Updates [Count]',fontsize=12)


# df_no_update = df_no_pre_schedule[ df_no_pre_schedule['Number of APREQ Updates'] == 0]
# df_with_update = df_no_pre_schedule[ df_no_pre_schedule['Number of APREQ Updates'] > 0]
# plt.subplot(2,4,3)
# plt.plot( df_no_update['Number of APREQ Updates'] , df_no_update['eobt_compliance'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='blue', label='No Updates' ,markeredgecolor='black' )
# plt.plot( df_with_update['Number of APREQ Updates'] , df_with_update['eobt_compliance'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='orange',label='Updates',markeredgecolor='black' )
# plt.xlim([-1,6])
# plt.ylim([-10,10])
# plt.xlabel('Number of APREQ Updates [Count]',fontsize=12)
# plt.ylabel('<Actual Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)
# plt.title('Pre-Schedule = False',fontsize=18)
# plt.legend()

# plt.subplot(2,4,7)
# compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
# compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
# plt.hist(df_no_update['eobt_compliance'],color='blue',label='No Updates: Compliance = ' + str(compliance_no_update)[0:4],edgecolor='black',normed=True,alpha=0.6,range=[-10,10],bins=20 )
# plt.hist(df_with_update['eobt_compliance'],color='orange',label='Updates: Compliance = ' + str(compliance_update)[0:4],edgecolor='black',normed=True,alpha=0.6, range=[-10,10],bins=20 )
# plt.legend()
# plt.xlabel('<Actual Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)

plt.tight_layout()
plt.savefig('apreq_number_updates_eobt_compliance_detailed.png')





plt.figure(figsize=(16,10))

df_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] == 0]
df_with_update = df_pre_schedule[ df_pre_schedule['Number of APREQ Updates'] > 0]


compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_mean = str(df_no_update['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['Compliance (minutes)'].std())[0:4]
update_mean = str(df_with_update['Compliance (minutes)'].mean())[0:4]
update_std = str(df_with_update['Compliance (minutes)'].std())[0:4]
no_update_label = 'No APREQ Updates: Percent = ' + str(len(df_no_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_no_update)[0:4] + ', Mean = ' + no_update_mean + ', STD = ' + no_update_std 
update_label = 'APREQ Updates: Percent = ' + str(len(df_with_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4] + ', Mean = ' + update_mean + ', STD = ' + update_std 



plt.subplot2grid((4,8), (0,2), rowspan=3, colspan=6)
plt.plot( df_no_update['eobt_change'] , df_no_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='blue', label=no_update_label ,markeredgecolor='black' )
plt.plot( df_with_update['eobt_change'] , df_with_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='orange',label=update_label,markeredgecolor='black' )
plt.xlim([-10,30])
plt.ylim([-10,10])
#plt.xlabel('<EOBT at Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)
#plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)
plt.title('Pre-Schedule = TRUE',fontsize=18)
plt.grid(True,alpha=0.5)
plt.legend()

plt.subplot2grid((4,8), (0,0), rowspan=3, colspan=2)
compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_mean = str(df_no_update['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['Compliance (minutes)'].std())[0:4]
update_mean = str(df_with_update['Compliance (minutes)'].mean())[0:4]
update_std = str(df_with_update['Compliance (minutes)'].std())[0:4]
no_update_label = 'No Updates: Percent = ' + str(len(df_no_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_no_update)[0:4] + ', Mean = ' + no_update_mean + ', STD = ' + no_update_std 
update_label = 'Updates: Percent = ' + str(len(df_with_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4] + ', Mean = ' + update_mean + ', STD = ' + update_std 
plt.hist(df_no_update['Compliance (minutes)'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,10],bins=20,orientation='horizontal' ,align='left')
plt.hist(df_with_update['Compliance (minutes)'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,10],bins=20 ,orientation='horizontal' ,align='left')
plt.ylim([-10,10])
#plt.legend()
plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)


plt.subplot2grid((4,8), (3,2), rowspan=1, colspan=6)
no_update_label = 'No APREQ Updates: Mean = ' + str(df_no_update['eobt_change'].mean())[0:4] + ', STD = ' + str(df_no_update['eobt_change'].std())[0:4]
update_label = 'APREQ Updates: Mean = ' + str(df_with_update['eobt_change'].mean())[0:4] + ', STD = ' + str(df_with_update['eobt_change'].std())[0:4]
plt.hist(df_no_update['eobt_change'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,30],bins=40 ,align='left')
plt.hist(df_with_update['eobt_change'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,30],bins=40 ,align='left')
plt.xlabel('<EOBT at Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)
plt.xlim([-10,30])
plt.legend()


# df_no_update = df_no_pre_schedule[ df_no_pre_schedule['Number of APREQ Updates'] == 0]
# df_with_update = df_no_pre_schedule[ df_no_pre_schedule['Number of APREQ Updates'] > 0]
# plt.subplot(2,4,3)
# plt.plot( df_no_update['Number of APREQ Updates'] , df_no_update['eobt_compliance'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='blue', label='No Updates' ,markeredgecolor='black' )
# plt.plot( df_with_update['Number of APREQ Updates'] , df_with_update['eobt_compliance'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='orange',label='Updates',markeredgecolor='black' )
# plt.xlim([-1,6])
# plt.ylim([-10,10])
# plt.xlabel('Number of APREQ Updates [Count]',fontsize=12)
# plt.ylabel('<Actual Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)
# plt.title('Pre-Schedule = False',fontsize=18)
# plt.legend()

# plt.subplot(2,4,7)
# compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
# compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
# plt.hist(df_no_update['eobt_compliance'],color='blue',label='No Updates: Compliance = ' + str(compliance_no_update)[0:4],edgecolor='black',normed=True,alpha=0.6,range=[-10,10],bins=20 )
# plt.hist(df_with_update['eobt_compliance'],color='orange',label='Updates: Compliance = ' + str(compliance_update)[0:4],edgecolor='black',normed=True,alpha=0.6, range=[-10,10],bins=20 )
# plt.legend()
# plt.xlabel('<Actual Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)

plt.tight_layout()
plt.savefig('compliance_eobt_update_detailed.png')









plt.figure(figsize=(16,10))

df_no_update = df_pre_schedule[ df_pre_schedule['eobt_change'] == 0 ]
df_with_update = df_pre_schedule[ df_pre_schedule['eobt_change'] != 0 ]
compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_mean = str(df_no_update['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['Compliance (minutes)'].std())[0:4]
update_mean = str(df_with_update['Compliance (minutes)'].mean())[0:4]
update_std = str(df_with_update['Compliance (minutes)'].std())[0:4]
no_update_label = 'No EOBT Updates: Percent = ' + str(len(df_no_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_no_update)[0:4] + ', Mean = ' + no_update_mean + ', STD = ' + no_update_std 
update_label = 'EOBT Updates: Percent = ' + str(len(df_with_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4] + ', Mean = ' + update_mean + ', STD = ' + update_std 



plt.subplot2grid((4,8), (0,2), rowspan=3, colspan=6)
plt.plot( df_no_update['eobt_change'] , df_no_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='blue', label=no_update_label ,markeredgecolor='black' )
plt.plot( df_with_update['eobt_change'] , df_with_update['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='orange',label=update_label,markeredgecolor='black' )
plt.xlim([-10,30])
plt.ylim([-10,10])
#plt.xlabel('<EOBT at Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)
#plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)
plt.title('Pre-Schedule = TRUE',fontsize=18)
plt.legend()

plt.subplot2grid((4,8), (0,0), rowspan=3, colspan=2)
compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
no_update_mean = str(df_no_update['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_no_update['Compliance (minutes)'].std())[0:4]
update_mean = str(df_with_update['Compliance (minutes)'].mean())[0:4]
update_std = str(df_with_update['Compliance (minutes)'].std())[0:4]
no_update_label = 'No EOBT Updates: Percent = ' + str(len(df_no_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_no_update)[0:4] + ', Mean = ' + no_update_mean + ', STD = ' + no_update_std 
update_label = 'EOBT Updates: Percent = ' + str(len(df_with_update) / (len(df_with_update) + len(df_no_update)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4] + ', Mean = ' + update_mean + ', STD = ' + update_std 
plt.hist(df_no_update['Compliance (minutes)'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,10],bins=20,orientation='horizontal' ,align='left')
plt.hist(df_with_update['Compliance (minutes)'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,10],bins=20 ,orientation='horizontal' ,align='left')
#plt.legend()
plt.ylim([-10,10])
plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)



plt.subplot2grid((4,8), (3,2), rowspan=1, colspan=6)
no_update_label = 'No Updates: Mean = ' + str(df_no_update['eobt_change'].mean())[0:4] + ', STD = ' + str(df_no_update['eobt_change'].std())[0:4]
update_label = 'Updates: Mean = ' + str(df_with_update['eobt_change'].mean())[0:4] + ', STD = ' + str(df_with_update['eobt_change'].std())[0:4]
plt.hist(df_no_update['eobt_change'],color='blue',label=no_update_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,30],bins=40 ,align='left')
plt.hist(df_with_update['eobt_change'],color='orange',label=update_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,30],bins=40 ,align='left')
plt.xlabel('<EOBT at Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)
plt.xlim([-10,30])
#plt.legend()


# df_no_update = df_no_pre_schedule[ df_no_pre_schedule['Number of APREQ Updates'] == 0]
# df_with_update = df_no_pre_schedule[ df_no_pre_schedule['Number of APREQ Updates'] > 0]
# plt.subplot(2,4,3)
# plt.plot( df_no_update['Number of APREQ Updates'] , df_no_update['eobt_compliance'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='blue', label='No Updates' ,markeredgecolor='black' )
# plt.plot( df_with_update['Number of APREQ Updates'] , df_with_update['eobt_compliance'] , marker='o',linestyle='',markersize=8,alpha=0.2,color='orange',label='Updates',markeredgecolor='black' )
# plt.xlim([-1,6])
# plt.ylim([-10,10])
# plt.xlabel('Number of APREQ Updates [Count]',fontsize=12)
# plt.ylabel('<Actual Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)
# plt.title('Pre-Schedule = False',fontsize=18)
# plt.legend()

# plt.subplot(2,4,7)
# compliance_no_update = len(df_no_update[ df_no_update['Compliant'] == True ]) / float(len(df_no_update))
# compliance_update = len(df_with_update[ df_with_update['Compliant'] == True ]) / float(len(df_with_update))
# plt.hist(df_no_update['eobt_compliance'],color='blue',label='No Updates: Compliance = ' + str(compliance_no_update)[0:4],edgecolor='black',normed=True,alpha=0.6,range=[-10,10],bins=20 )
# plt.hist(df_with_update['eobt_compliance'],color='orange',label='Updates: Compliance = ' + str(compliance_update)[0:4],edgecolor='black',normed=True,alpha=0.6, range=[-10,10],bins=20 )
# plt.legend()
# plt.xlabel('<Actual Pushback> - <EOBT at Pre-Schedule> [Minutes]',fontsize=12)

plt.tight_layout()
plt.savefig('compliance_eobt_update_v2_detailed.png')









#########################################################
#########################################################
#########################################################
##################### NEW FIGURE ########################
#########################################################
#########################################################
#########################################################


plt.figure(figsize=(16,10))

df_negative_delay = df_pre_schedule[ df_pre_schedule['TBFM Assigned Delay (minutes)'] < 0]
df_positive_delay = df_pre_schedule[ df_pre_schedule['TBFM Assigned Delay (minutes)'] >= 0]

compliance_negative_delay = len(df_negative_delay[ df_negative_delay['Compliant'] == True ]) / float(len(df_negative_delay))
compliance_update = len(df_positive_delay[ df_positive_delay['Compliant'] == True ]) / float(len(df_positive_delay))
no_update_mean = str(df_negative_delay['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_negative_delay['Compliance (minutes)'].std())[0:4]
update_mean = str(df_positive_delay['Compliance (minutes)'].mean())[0:4]
update_std = str(df_positive_delay['Compliance (minutes)'].std())[0:4]
neg_delay_label = 'Negative TBFM Delay: Percent = ' + str(len(df_negative_delay) / (len(df_positive_delay) + len(df_negative_delay)))[0:4] + ', Compliance = ' + str(compliance_negative_delay)[0:4] 
pos_delay_label = 'Positive TBFM Delay: Percent = ' + str(len(df_positive_delay) / (len(df_positive_delay) + len(df_negative_delay)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4] 

plt.subplot2grid((4,16), (0,2), rowspan=3, colspan=6)
plt.plot( df_negative_delay['TBFM Assigned Delay (minutes)'] , df_negative_delay['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.4,color='blue', label=neg_delay_label ,markeredgecolor='black' )
plt.plot( df_positive_delay['TBFM Assigned Delay (minutes)'] , df_positive_delay['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.4,color='orange',label=pos_delay_label,markeredgecolor='black' )
plt.xlim([-35,35])
plt.ylim([-10,10])
# plt.xlabel('TBFM Assigned Delay [Minutes]',fontsize=12)
# plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)
plt.title('Pre-Schedule = TRUE',fontsize=18)
plt.grid(True,alpha=0.5)
plt.legend()

plt.subplot2grid((4,16), (0,0), rowspan=3, colspan=2)
compliance_negative_delay = len(df_negative_delay[ df_negative_delay['Compliant'] == True ]) / float(len(df_negative_delay))
compliance_update = len(df_positive_delay[ df_positive_delay['Compliant'] == True ]) / float(len(df_positive_delay))
no_update_mean = str(df_negative_delay['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_negative_delay['Compliance (minutes)'].std())[0:4]
update_mean = str(df_positive_delay['Compliance (minutes)'].mean())[0:4]
update_std = str(df_positive_delay['Compliance (minutes)'].std())[0:4]
neg_delay_label = 'Negative TBFM Delay: Percent = ' + str(len(df_negative_delay) / (len(df_positive_delay) + len(df_negative_delay)))[0:4] + ', Compliance = ' + str(compliance_negative_delay)[0:4] + ', Mean = ' + no_update_mean + ', STD = ' + no_update_std 
pos_delay_label = 'Positive TBFM Delay: Percent = ' + str(len(df_positive_delay) / (len(df_positive_delay) + len(df_negative_delay)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4] + ', Mean = ' + update_mean + ', STD = ' + update_std 


n,bins,patches = plt.hist(df_negative_delay['Compliance (minutes)'],color='blue',label=neg_delay_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,10],bins=20,orientation='horizontal',align='left')
n2,bins,patches = plt.hist(df_positive_delay['Compliance (minutes)'],color='orange',label=pos_delay_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,10],bins=20,orientation='horizontal',align='left')
max1 = max(n)
max2 = max(n2)
#plt.ylim([0,1.2*max([max1,max2])])
#plt.legend()
plt.ylim([-10,10])
plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)


df_negative_delay = df_no_pre_schedule[ df_no_pre_schedule['TBFM Assigned Delay (minutes)'] < 0]
df_positive_delay = df_no_pre_schedule[ df_no_pre_schedule['TBFM Assigned Delay (minutes)'] >= 0]

compliance_negative_delay = len(df_negative_delay[ df_negative_delay['Compliant'] == True ]) / float(len(df_negative_delay))
compliance_update = len(df_positive_delay[ df_positive_delay['Compliant'] == True ]) / float(len(df_positive_delay))
no_update_mean = str(df_negative_delay['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_negative_delay['Compliance (minutes)'].std())[0:4]
update_mean = str(df_positive_delay['Compliance (minutes)'].mean())[0:4]
update_std = str(df_positive_delay['Compliance (minutes)'].std())[0:4]
neg_delay_label = 'Negative TBFM Delay: Percent = ' + str(len(df_negative_delay) / (len(df_positive_delay) + len(df_negative_delay)))[0:4] + ', Compliance = ' + str(compliance_negative_delay)[0:4] 
pos_delay_label = 'Positive TBFM Delay: Percent = ' + str(len(df_positive_delay) / (len(df_positive_delay) + len(df_negative_delay)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4] 

plt.subplot2grid((4,16), (0,8), rowspan=3, colspan=6)
plt.plot( df_negative_delay['TBFM Assigned Delay (minutes)'] , df_negative_delay['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.4,color='blue', label=neg_delay_label ,markeredgecolor='black' )
plt.plot( df_positive_delay['TBFM Assigned Delay (minutes)'] , df_positive_delay['Compliance (minutes)'] , marker='o',linestyle='',markersize=8,alpha=0.4,color='orange',label=pos_delay_label,markeredgecolor='black' )
plt.xlim([-35,35])
plt.ylim([-10,10])
plt.grid(True,alpha=0.5)
# plt.xlabel('TBFM Assigned Delay [Minutes]',fontsize=12)
# plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)
plt.title('Pre-Schedule = False',fontsize=18)
plt.legend()

plt.subplot2grid((4,16), (0,14), rowspan=3, colspan=2)
compliance_negative_delay = len(df_negative_delay[ df_negative_delay['Compliant'] == True ]) / float(len(df_negative_delay))
compliance_update = len(df_positive_delay[ df_positive_delay['Compliant'] == True ]) / float(len(df_positive_delay))
no_update_mean = str(df_negative_delay['Compliance (minutes)'].mean())[0:4]
no_update_std = str(df_negative_delay['Compliance (minutes)'].std())[0:4]
update_mean = str(df_positive_delay['Compliance (minutes)'].mean())[0:4]
update_std = str(df_positive_delay['Compliance (minutes)'].std())[0:4]
neg_delay_label = 'Negative TBFM Delay: Percent = ' + str(len(df_negative_delay) / (len(df_positive_delay) + len(df_negative_delay)))[0:4] + ', Compliance = ' + str(compliance_negative_delay)[0:4] + ', Mean = ' + no_update_mean + ', STD = ' + no_update_std 
pos_delay_label = 'Positive TBFM Delay: Percent = ' + str(len(df_positive_delay) / (len(df_positive_delay) + len(df_negative_delay)))[0:4] + ', Compliance = ' + str(compliance_update)[0:4] + ', Mean = ' + update_mean + ', STD = ' + update_std 


n,bins,patches = plt.hist(df_negative_delay['Compliance (minutes)'],color='blue',label=neg_delay_label,edgecolor='black',normed=True,alpha=0.6,range=[-10,10],bins=20,orientation='horizontal',align='left')
n2,bins,patches = plt.hist(df_positive_delay['Compliance (minutes)'],color='orange',label=pos_delay_label,edgecolor='black',normed=True,alpha=0.6, range=[-10,10],bins=20,orientation='horizontal' ,align='left')
max1 = max(n)
max2 = max(n2)
#plt.ylim([0,1.2*max([max1,max2])])

#plt.legend()
plt.ylim([-10,10])
plt.ylabel('<ATOT> - <APREQ Time> [Minutes]',fontsize=12)





df_negative_delay = df_pre_schedule[ df_pre_schedule['TBFM Assigned Delay (minutes)'] < 0]
df_positive_delay = df_pre_schedule[ df_pre_schedule['TBFM Assigned Delay (minutes)'] >= 0]

no_update_mean = str(df_negative_delay['TBFM Assigned Delay (minutes)'].mean())[0:4]
no_update_std = str(df_negative_delay['TBFM Assigned Delay (minutes)'].std())[0:4]
update_mean = str(df_positive_delay['TBFM Assigned Delay (minutes)'].mean())[0:4]
update_std = str(df_positive_delay['TBFM Assigned Delay (minutes)'].std())[0:4]
neg_delay_label = 'Negative TBFM Delay: Mean = ' + no_update_mean + ', STD = ' + no_update_std 
pos_delay_label = 'Positive TBFM Delay: Mean = ' + update_mean + ', STD = ' + update_std 

plt.subplot2grid((4,16), (3,2), rowspan=1, colspan=6)
n,bins,patches = plt.hist(df_negative_delay['TBFM Assigned Delay (minutes)'],color='blue',label=neg_delay_label,edgecolor='black',normed=True,alpha=0.6,range=[-35,35],bins=70,orientation='vertical',align='left')
n2,bins,patches = plt.hist(df_positive_delay['TBFM Assigned Delay (minutes)'],color='orange',label=pos_delay_label,edgecolor='black',normed=True,alpha=0.6, range=[-35,35],bins=70 ,orientation='vertical' ,align='left')
plt.xlim([-35,35])
plt.xlabel('TBFM Assigned Delay [Minutes]',fontsize=12)
plt.legend()
max1 = max(n)
max2 = max(n2)
plt.ylim([0,1.6*max([max1,max2])])



df_negative_delay = df_no_pre_schedule[ df_no_pre_schedule['TBFM Assigned Delay (minutes)'] < 0]
df_positive_delay = df_no_pre_schedule[ df_no_pre_schedule['TBFM Assigned Delay (minutes)'] >= 0]

no_update_mean = str(df_negative_delay['TBFM Assigned Delay (minutes)'].mean())[0:4]
no_update_std = str(df_negative_delay['TBFM Assigned Delay (minutes)'].std())[0:4]
update_mean = str(df_positive_delay['TBFM Assigned Delay (minutes)'].mean())[0:4]
update_std = str(df_positive_delay['TBFM Assigned Delay (minutes)'].std())[0:4]
neg_delay_label = 'Negative TBFM Delay: Mean = ' + no_update_mean + ', STD = ' + no_update_std 
pos_delay_label = 'Positive TBFM Delay: Mean = ' + update_mean + ', STD = ' + update_std

plt.subplot2grid((4,16), (3,8), rowspan=1, colspan=6)
n,bins,patches = plt.hist(df_negative_delay['TBFM Assigned Delay (minutes)'],color='blue',label=neg_delay_label,edgecolor='black',normed=True,alpha=0.6,range=[-35,35],bins=70,orientation='vertical' ,align='left')
n2,bins,patches = plt.hist(df_positive_delay['TBFM Assigned Delay (minutes)'],color='orange',label=pos_delay_label,edgecolor='black',normed=True,alpha=0.6, range=[-35,35],bins=70 ,orientation='vertical',align='left')
plt.xlim([-35,35])
plt.xlabel('TBFM Assigned Delay [Minutes]',fontsize=12)

plt.legend()
max1 = max(n)
max2 = max(n2)
plt.ylim([0,1.6*max([max1,max2])])

plt.tight_layout()
plt.savefig('apreq_delay_compliance_detailed_v2.png')


