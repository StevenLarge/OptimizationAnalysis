#This python script generates the Space-Optimized protocols Discrete nonequilibrium control simulations
#
#Steven Large
#March 5th 2018

import numpy as np
import scipy.optimize

import os

import OptimizeSpace as SpaceOpt
import WriteData

#WritePathBase = "Protocols_"
WritePathBase = "/Users/stevelarge/Research/DiscreteControl/LinkedCode_CPP/Equilibrium_FromCluster/Protocols_Mar21/Protocols_"

#NumberCPVals = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
#ProtocolTimes = [1,5,10,50,100,500]
#NumberCPVals = [5,9,13,17,21,25,29,33,37,41,45,49,53,57,61,65,69,73,77,81,85,89,93,97,101]
NumberCPVals = [4,8,16,32,64,128,256,512]
ProtocolTimes = [200]

Param_Ext = ["9_15/","12_15/","15_15/"]
#Param_Ext = ["15_15/"]

CPStart = -1

PaddingTime = 100

#CorrelationPath_Base = "CorrelationMesh_"
CorrelationPath_Base = "/Users/stevelarge/Research/DiscreteControl/LinkedCode_CPP/Equilibrium_FromCluster/CorrelationMesh_"
FilenameCorr = "CorrelationMesh_2.dat"
FilenameCP = "CPVals_2.dat"
FilenameLagTime = "LagTime_2.dat"


for ParameterIndex in range(len(Param_Ext)):

	print "--\n"

	WritePath = WritePathBase + Param_Ext[ParameterIndex]
	WritePathLog = WritePath + "Logs/"
	CorrelationPath = CorrelationPath_Base + Param_Ext[ParameterIndex]

	CorrelationArray = SpaceOpt.ReadCorrelationArray(CorrelationPath,FilenameCorr)
	LagTime_Vector = SpaceOpt.ReadVector(CorrelationPath,FilenameLagTime)
	CPVals_Vector = SpaceOpt.ReadVector(CorrelationPath,FilenameCP)

	print "----- Corr Read -----\n"

	for index1 in range(len(NumberCPVals)):

		print "\t\t----- CPVals " + str(NumberCPVals[index1]) + " -----\n"

		for index2 in range(len(ProtocolTimes)):

			OptimalResult,NaiveCP,TimeAlloc = SpaceOpt.Driver_PreRead(NumberCPVals[index1],ProtocolTimes[index2],CPVals_Vector,LagTime_Vector,CorrelationArray)

			OptimalSpace = list(OptimalResult.x)
			OptimalCP = [CPStart]
			CPCounter = CPStart

			for index3 in range(len(OptimalSpace)):
				CPCounter = CPCounter + OptimalSpace[index3]
				OptimalCP.append(CPCounter)

			TimeAlloc.append(PaddingTime)
			TimeAlloc.insert(0,PaddingTime)
			NaiveCP.append(1)
			NaiveCP.insert(0,-1)

			WriteNameSpace = "SpaceOpt_CP" + str(NumberCPVals[index1]) + "_T" + str(ProtocolTimes[index2]) + ".dat"
			WriteNameLog = "OptimizerLogFile-Space_CP" + str(NumberCPVals[index1]) + "_T" + str(ProtocolTimes[index2]) + ".dat"

			WriteData.WriteProtocol(WritePath,WriteNameSpace,OptimalCP,TimeAlloc)
			WriteData.OptimizerLog(WritePathLog,WriteNameLog,OptimalResult)




