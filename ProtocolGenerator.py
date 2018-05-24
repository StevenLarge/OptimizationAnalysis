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

	OptCPVals,NaiveTime,CPVals = OptSpace.Driver(NumCPVals,TotalTime)

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


CPVals,Times = GenerateNaiveProtocol(10,100)
CPVals_Opt,Times_Opt = GenerateTimeOptProtocol(10,100)
CPVals_Space,Times_Space = GenerateSpaceOptProtocol(10,100)

print str(len(CPVals))
print str(len(CPVals_Opt))
print str(len(Times))
print str(len(Times_Opt))
print str(len(CPVals_Space))
print str(len(Times_Space))

CumulTimes = []
CumulTimes_Opt = []
TimeAcc = 0
TimeAcc_Opt = 0
for index in range(len(Times)-1):
	CumulTimes.append(TimeAcc)
	CumulTimes_Opt.append(TimeAcc_Opt)
	TimeAcc += Times[index+1]
	TimeAcc_Opt += Times_Opt[index+1]


sns.set(style='darkgrid',palette='muted',color_codes=True)

fig,ax = plt.subplots(1,1)
ax.plot(CumulTimes,CPVals[0:len(CPVals)-1],'r--',linewidth=2.5,alpha=0.6)
ax.plot(CumulTimes_Opt,CPVals_Opt[0:len(CPVals)-1],'b--',linewidth=2.5,alpha=0.6)
ax.plot(CumulTimes,CPVals_Space[0:len(CPVals)-1],'g--',linewidth=2.5,alpha=0.6)
ax.plot(CumulTimes,CPVals[0:len(CPVals)-1],'ro')
ax.plot(CumulTimes_Opt,CPVals_Opt[0:len(CPVals)-1],'bo')
ax.plot(CumulTimes,CPVals_Space[0:len(CPVals)-1],'go')


plt.show()
plt.close()
