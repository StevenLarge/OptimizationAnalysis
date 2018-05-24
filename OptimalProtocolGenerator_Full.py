#This python script generates the Fully-Optimal protocols Discrete nonequilibrium control simulations
#
#Steven Large
#March 5th 2018

import numpy as np
import scipy.optimize

import os

import OptimizeFull as FullOpt
import WriteData

#WritePathBase = "Protocols_"
WritePathBase = "/Users/stevelarge/Research/DiscreteControl/LinkedCode_CPP/Equilibrium_FromCluster/Protocols_Mar21/Protocols_"

#NumberCPVals = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
#ProtocolTimes = [1,5,10,50,100,500]

#NumberCPVals = [25]
#NumberCPVals = [4,8,16,32,64,128,256,512]
NumberCPVals = [512]

#ProtocolTimes = [1,5,10,50,100,500]
#ProtocolTimes = [600,800,1000,1200,1400,1600,1800,2000]
#ProtocolTimes = [2200,2400,2600,2800,3000,3200,3400]
#ProtocolTimes = [10,50,200,400,600,800,1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000]
#ProtocolTimes = [3200,3600,3800,4000,4200,4400,4600,4800,5000]
ProtocolTimes = [200]

#Param_Ext = ["9_15/","105_15/","12_15/","15_15/"]
#Param_Ext = ["9_15/","12_15/","15_15/"]
Param_Ext = ["12_15/"]

CPStart = -1

PaddingTime = 100

#CorrelationPath_Base = "CorrelationMesh"
CorrelationPath_Base = "/Users/stevelarge/Research/DiscreteControl/LinkedCode_CPP/Equilibrium_FromCluster/CorrelationMesh_"
FilenameCorr = "CorrelationMesh_2.dat"
FilenameCP = "CPVals_2.dat"
FilenameLagTime = "LagTime_2.dat"

FullOptimizerIterations = 2

for ParameterIndex in range(len(Param_Ext)):

	WritePath = WritePathBase + Param_Ext[ParameterIndex]
	WritePathLog = WritePath + "Logs/"
	CorrelationPath = CorrelationPath_Base + Param_Ext[ParameterIndex]

	CorrelationArray = FullOpt.ReadCorrelationArray(CorrelationPath,FilenameCorr)
	LagTime_Vector = FullOpt.ReadVector(CorrelationPath,FilenameLagTime)
	CPVals_Vector = FullOpt.ReadVector(CorrelationPath,FilenameCP)

	print "\n\n\t----- Corr Read -----\n"


	for index1 in range(len(NumberCPVals)):

		for index2 in range(len(ProtocolTimes)):

			OptimalCP,OptimalTime,NaiveCP,NaiveTime,CostTracker = FullOpt.Driver_PreRead_Brute(FullOptimizerIterations,NumberCPVals[index1],ProtocolTimes[index2],CPVals_Vector,LagTime_Vector,CorrelationArray)

			print "\t\t----- Proto Time --> " + str(ProtocolTimes[index2]) + "\n"

			OptimalTime.append(PaddingTime)
			OptimalTime.insert(0,PaddingTime)
			NaiveTime.append(PaddingTime)
			NaiveTime.insert(0,PaddingTime)

			WriteNameFull = "FullOpt_CP" + str(NumberCPVals[index1]) + "_T" + str(ProtocolTimes[index2]) + ".dat"
			WriteNameLog = "OptimizerLogFile-Full_CP" + str(NumberCPVals[index1]) + "_T" + str(ProtocolTimes[index2]) + ".dat"

			WriteData.WriteProtocol(WritePath,WriteNameFull,OptimalCP,OptimalTime)
			WriteData.OptimizerLog_Cost(WritePathLog,WriteNameLog,CostTracker)



