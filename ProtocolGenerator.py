#This python script generates examples of discrete protocol classes
#
#Steven Large
#May23rd 2018

import os
import numpy as np
from math import *
import matplotlib.pyplot as plt
import seaborn as sns

import OptimizeTime as OptTime
import OptimizeSpace as OptSpace

def GenerateNaiveProtocol(NumCPVals,TotalTime):

	CPDist = 2.0
	CPMin = -1.0
	CPMax = 1.0

	CPVals = []
	Times = []

	CPDiff = CPDist/float(NumCPVals-1)

	CurrCP = CPMin

	for index in range(NumCPVals):
		CPVals.append(CurrCP)
		CurrCP += CPDiff

	PaddingTime = 100
	StepTime = TotalTime/float(NumCPVals - 2)

	Times.append(PaddingTime)

	for index in range(NumCPVals - 2):
		Times.append(StepTime)

	Times.append(PaddingTime)

	#print "CPVals\t\tTimes\n\n"

	#for index in range(len(CPVals)):
	#	print str(CPVals[index]) + "\t\t" + str(Times[index]) + "\n"

	return CPVals,Times


def GenerateTimeOptProtocol(NumCPVals,TotalTime):

	PaddingTime = 100

	OptLagTimes,NaiveTime,CPVals = OptTime.Driver(NumCPVals,TotalTime)

	OptLagTimes = list(OptLagTimes.x)

	OptLagTimes.append(PaddingTime)
	OptLagTimes.insert(0,PaddingTime)

	return CPVals,OptLagTimes


def GenerateSpaceOptProtocol(NumCPVals,TotalTime):

	PaddingTime = 100

	OptCPVals,CPVals,NaiveTime = OptSpace.Driver(NumCPVals,TotalTime)

	OptCPVals = list(OptCPVals.x)

	NaiveTime.append(PaddingTime)
	NaiveTime.insert(0,PaddingTime)

	CPVals = []
	CurrCP = -1
	for index in range(len(OptCPVals)):
		CPVals.append(CurrCP)
		CurrCP = CurrCP + OptCPVals[index]

	CPVals.append(OptCPVals[-1])

	return CPVals,NaiveTime


def GenerateFullOptProtocol(NumCPVals,TotalTime):

	CPVals = []
	Times = []

def GenerateTrajectory(CPVals,CumulTimes):

	TimeRange = []
	CPTraj = []
	CurrTime = CumulTimes[0]

	TimeRange.append(0)
	CPTraj.append(CPVals[0])

	for index in range(len(CPVals)-2):

		while(CurrTime <= CumulTimes[index+1]):

			CurrTime += 0.01
			TimeRange.append(CurrTime)
			CPTraj.append(CPVals[index+1])

	TimeRange.append(CurrTime + 0.01)
	CPTraj.append(CPVals[-1])


	return CPTraj,TimeRange




CPVals_N1,Times_N1 = GenerateNaiveProtocol(5,100)
CPVals_N2,Times_N2 = GenerateNaiveProtocol(10,100)
CPVals_N3,Times_N3 = GenerateNaiveProtocol(20,100)
CPVals_N4,Times_N4 = GenerateNaiveProtocol(40,100)

CPVals_T1,Times_T1 = GenerateTimeOptProtocol(5,100)
CPVals_T2,Times_T2 = GenerateTimeOptProtocol(10,100)
CPVals_T3,Times_T3 = GenerateTimeOptProtocol(20,100)
CPVals_T4,Times_T4 = GenerateTimeOptProtocol(40,100)

CPVals_S1,Times_S1 = GenerateSpaceOptProtocol(5,100)
CPVals_S2,Times_S2 = GenerateSpaceOptProtocol(10,100)
CPVals_S3,Times_S3 = GenerateSpaceOptProtocol(20,100)
CPVals_S4,Times_S4 = GenerateSpaceOptProtocol(40,100)

CumulTimes_N1 = []
CumulTimes_N2 = []
CumulTimes_N3 = []
CumulTimes_N4 = []

CumulTimes_T1 = []
CumulTimes_T2 = []
CumulTimes_T3 = []
CumulTimes_T4 = []

CumulTimes_S1 = []
CumulTimes_S2 = []
CumulTimes_S3 = []
CumulTimes_S4 = []

TimeAcc_N = 0
TimeAcc_T = 0
TimeAcc_S = 0

for index in range(len(Times_N1)-1):
	CumulTimes_N1.append(TimeAcc_N)
	CumulTimes_T1.append(TimeAcc_T)
	CumulTimes_S1.append(TimeAcc_S)
	TimeAcc_N += Times_N1[index+1]
	TimeAcc_T += Times_T1[index+1]
	TimeAcc_S += Times_S1[index+1]

TimeAcc_N = 0
TimeAcc_T = 0
TimeAcc_S = 0

for index in range(len(Times_N2)-1):
	CumulTimes_N2.append(TimeAcc_N)
	CumulTimes_T2.append(TimeAcc_T)
	CumulTimes_S2.append(TimeAcc_S)
	TimeAcc_N += Times_N2[index+1]
	TimeAcc_T += Times_T2[index+1]
	TimeAcc_S += Times_S2[index+1]

TimeAcc_N = 0
TimeAcc_T = 0
TimeAcc_S = 0

for index in range(len(Times_N3)-1):
	CumulTimes_N3.append(TimeAcc_N)
	CumulTimes_T3.append(TimeAcc_T)
	CumulTimes_S3.append(TimeAcc_S)
	TimeAcc_N += Times_N3[index+1]
	TimeAcc_T += Times_T3[index+1]
	TimeAcc_S += Times_S3[index+1]


TimeAcc_N = 0
TimeAcc_T = 0
TimeAcc_S = 0

for index in range(len(Times_N4)-1):
	CumulTimes_N4.append(TimeAcc_N)
	CumulTimes_T4.append(TimeAcc_T)
	CumulTimes_S4.append(TimeAcc_S)
	TimeAcc_N += Times_N4[index+1]
	TimeAcc_T += Times_T4[index+1]
	TimeAcc_S += Times_S4[index+1]

CPTraj_N1,CPTime_N1 = GenerateTrajectory(CPVals_N1,CumulTimes_N1)
CPTraj_N2,CPTime_N2 = GenerateTrajectory(CPVals_N2,CumulTimes_N2)
CPTraj_N3,CPTime_N3 = GenerateTrajectory(CPVals_N3,CumulTimes_N3)
CPTraj_N4,CPTime_N4 = GenerateTrajectory(CPVals_N4,CumulTimes_N4)

CPTraj_T1,CPTime_T1 = GenerateTrajectory(CPVals_T1,CumulTimes_T1)
CPTraj_T2,CPTime_T2 = GenerateTrajectory(CPVals_T2,CumulTimes_T2)
CPTraj_T3,CPTime_T3 = GenerateTrajectory(CPVals_T3,CumulTimes_T3)
CPTraj_T4,CPTime_T4 = GenerateTrajectory(CPVals_T4,CumulTimes_T4)

CPTraj_S1,CPTime_S1 = GenerateTrajectory(CPVals_S1,CumulTimes_S1)
CPTraj_S2,CPTime_S2 = GenerateTrajectory(CPVals_S2,CumulTimes_S2)
CPTraj_S3,CPTime_S3 = GenerateTrajectory(CPVals_S3,CumulTimes_S3)
CPTraj_S4,CPTime_S4 = GenerateTrajectory(CPVals_S4,CumulTimes_S4)


sns.set(style='darkgrid',palette='muted',color_codes=True)

fig,ax = plt.subplots(1,4,sharex=True,sharey=True)
#ax[0].plot(CumulTimes_N1,CPVals_N1[0:len(CPVals_N1)-1],'r--',linewidth=2.5,alpha=0.5)
ax[0].plot(CPTime_N1,CPTraj_N1,'r--',linewidth=2.5,alpha=0.5)
ax[0].plot(CumulTimes_N1,CPVals_N1[0:len(CPVals_N1)-1],'ro')

#ax[1].plot(CumulTimes_N2,CPVals_N2[0:len(CPVals_N2)-1],'r--',linewidth=2.5,alpha=0.5)
ax[1].plot(CPTime_N2,CPTraj_N2,'r--',linewidth=2.5,alpha=0.5)
ax[1].plot(CumulTimes_N2,CPVals_N2[0:len(CPVals_N2)-1],'ro')

#ax[2].plot(CumulTimes_N3,CPVals_N3[0:len(CPVals_N3)-1],'r--',linewidth=2.5,alpha=0.5)
ax[2].plot(CPTime_N3,CPTraj_N3,'r--',linewidth=2.5,alpha=0.5)
ax[2].plot(CumulTimes_N3,CPVals_N3[0:len(CPVals_N3)-1],'ro')

#ax[3].plot(CumulTimes_N4,CPVals_N4[0:len(CPVals_N4)-1],'r--',linewidth=2.5,alpha=0.5)
ax[3].plot(CPTime_N4,CPTraj_N4,'r--',linewidth=2.5,alpha=0.5)
ax[3].plot(CumulTimes_N4,CPVals_N4[0:len(CPVals_N4)-1],'ro')

ax[0].set_xlabel(r"Accumulated Time $t^*$",fontsize=17)
ax[0].set_ylabel(r"Control parameter $\lambda^*$",fontsize=17)

plt.show()
plt.close()

fig,ax = plt.subplots(1,4,sharex=True,sharey=True)
#ax[0].plot(CumulTimes_T1,CPVals_T1[0:len(CPVals_T1)-1],'b--',linewidth=2.5,alpha=0.5)
ax[0].plot(CPTime_T1,CPTraj_T1,'b--',linewidth=2.5,alpha=0.5)
ax[0].plot(CumulTimes_T1,CPVals_T1[0:len(CPVals_T1)-1],'bo')

#ax[1].plot(CumulTimes_T2,CPVals_T2[0:len(CPVals_T2)-1],'b--',linewidth=2.5,alpha=0.5)
ax[1].plot(CPTime_T2,CPTraj_T2,'b--',linewidth=2.5,alpha=0.5)
ax[1].plot(CumulTimes_T2,CPVals_T2[0:len(CPVals_T2)-1],'bo')

#ax[2].plot(CumulTimes_T3,CPVals_T3[0:len(CPVals_T3)-1],'b--',linewidth=2.5,alpha=0.5)
ax[2].plot(CPTime_T3,CPTraj_T3,'b--',linewidth=2.5,alpha=0.5)
ax[2].plot(CumulTimes_T3,CPVals_T3[0:len(CPVals_T3)-1],'bo')

#ax[3].plot(CumulTimes_T4,CPVals_T4[0:len(CPVals_T4)-1],'b--',linewidth=2.5,alpha=0.5)
ax[3].plot(CPTime_T4,CPTraj_T4,'b--',linewidth=2.5,alpha=0.5)
ax[3].plot(CumulTimes_T4,CPVals_T4[0:len(CPVals_T4)-1],'bo')

ax[0].set_xlabel(r"Accumulated Time $t^*$",fontsize=17)
ax[0].set_ylabel(r"Control parameter $\lambda^*$",fontsize=17)

plt.show()
plt.close()



fig,ax = plt.subplots(1,4,sharex=True,sharey=True)
#ax[0].plot(CumulTimes_S1,CPVals_S1[0:len(CPVals_S1)-1],'g--',linewidth=2.5,alpha=0.5)
ax[0].plot(CPTime_S1,CPTraj_S1,'g--',linewidth=2.5,alpha=0.5)
ax[0].plot(CumulTimes_S1,CPVals_S1[0:len(CPVals_S1)-1],'go')

#ax[1].plot(CumulTimes_S2,CPVals_S2[0:len(CPVals_S2)-1],'g--',linewidth=2.5,alpha=0.5)
ax[1].plot(CPTime_S2,CPTraj_S2,'g--',linewidth=2.5,alpha=0.5)
ax[1].plot(CumulTimes_S2,CPVals_S2[0:len(CPVals_S2)-1],'go')

#ax[2].plot(CumulTimes_S3,CPVals_S3[0:len(CPVals_S3)-1],'g--',linewidth=2.5,alpha=0.5)
ax[2].plot(CPTime_S3,CPTraj_S3,'g--',linewidth=2.5,alpha=0.5)
ax[2].plot(CumulTimes_S3,CPVals_S3[0:len(CPVals_S3)-1],'go')

#ax[3].plot(CumulTimes_S4,CPVals_S4[0:len(CPVals_S4)-1],'g--',linewidth=2.5,alpha=0.5)
ax[3].plot(CPTime_S4,CPTraj_S4,'g--',linewidth=2.5,alpha=0.5)
ax[3].plot(CumulTimes_S4,CPVals_S4[0:len(CPVals_S4)-1],'go')

ax[0].set_xlabel(r"Accumulated Time $t^*$",fontsize=17)
ax[0].set_ylabel(r"Control parameter $\lambda^*$",fontsize=17)

plt.show()
plt.close()


'''
fig,ax = plt.subplots(1,1)
ax.plot(CumulTimes,CPVals[0:len(CPVals)-1],'r--',linewidth=2.5,alpha=0.6)
ax.plot(CumulTimes_Opt,CPVals_Opt[0:len(CPVals)-1],'b--',linewidth=2.5,alpha=0.6)
ax.plot(CumulTimes,CPVals_Space[0:len(CPVals)-1],'g--',linewidth=2.5,alpha=0.6)
ax.plot(CumulTimes,CPVals[0:len(CPVals)-1],'ro')
ax.plot(CumulTimes_Opt,CPVals_Opt[0:len(CPVals)-1],'bo')
ax.plot(CumulTimes,CPVals_Space[0:len(CPVals)-1],'go')


plt.show()
plt.close()
'''