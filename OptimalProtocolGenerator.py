#This python script generates the optimal protocol data for discrete nonequilibrium simulations
#
#Steven Large
#February 12th 2018

import os
import timeit

import matplotlib.pyplot as plt

#import OptimizeProtocol_Time as TimeOpt
import OptimizeTime as TimeOpt
import OptimizeSpace as SpaceOpt
import OptimizeFull as FullOpt

import WriteData


Start = timeit.default_timer()

WritePath = "/Users/stevelarge/Research/DiscreteControl/LinkedCode_CPP/NonEquilibrium_Cluster/Protocols/"
WritePathLog = "/Users/stevelarge/Research/DiscreteControl/LinkedCode_CPP/NonEquilibrium_Cluster/Protocols/Logs/"

#NumberCPVals = [5,7,9,11,13,15,17,19,21,23,25]
#ProtocolTimes = [10,50,100,500,1000,5000,10000,50000]

#NumberCPVals = [5,7,9,11,13,15,17,19,21,23,25]
NumberCPVals = [23,25]
ProtocolTimes = [1,5,10,50,100,500]#,1000,5000]#,10000,50000]

#NumberCPVals = [9]
#ProtocolTimes = [500]

CPStart = -1

PaddingTime = 100

FullOptimizerIterations = 5

CorrelationPath = "/Users/stevelarge/Research/DiscreteControl/LinkedCode_CPP/Equilibrium_FromCluster/CorrelationMesh_12_15/"
FilenameCorr = "CorrelationMesh.dat"
FilenameCP = "CPVals.dat"
FilenameLagTime = "LagTime.dat"

CorrelationArray = TimeOpt.ReadCorrelationArray(CorrelationPath,FilenameCorr)
LagTime_Vector = TimeOpt.ReadVector(CorrelationPath,FilenameLagTime)
CPVals_Vector = TimeOpt.ReadVector(CorrelationPath,FilenameCP)

print "\n\n----- Data Finished Loading -----\n\n"

#for index1 in range(len(NumberCPVals)):

#	for index2 in range(len(ProtocolTimes)):

#		OptimalResult,NaiveTime,CPVals = TimeOpt.Driver_PreRead(NumberCPVals[index1],ProtocolTimes[index2],CPVals_Vector,LagTime_Vector,CorrelationArray)

#		OptimalTime = list(OptimalResult.x)

#		OptimalTime.append(PaddingTime)
#		OptimalTime.insert(0,PaddingTime)
#		NaiveTime.append(PaddingTime)
#		NaiveTime.insert(0,PaddingTime)

#		WriteNameTime = "TimeOpt_CP" + str(NumberCPVals[index1]) + "_T" + str(ProtocolTimes[index2]) + ".dat"
#		WriteNameNaive = "Naive_CP" + str(NumberCPVals[index1]) + "_T" + str(ProtocolTimes[index2]) + ".dat" 
#		WriteNameLog = "OptimizerLogFile-Time_CP" + str(NumberCPVals[index1]) + "_T" + str(ProtocolTimes[index2]) + ".dat"

#		WriteData.WriteProtocol(WritePath,WriteNameTime,CPVals,OptimalTime)
#		WriteData.WriteProtocol(WritePath,WriteNameNaive,CPVals,NaiveTime)
#		WriteData.OptimizerLog(WritePathLog,WriteNameLog,OptimalResult)

#		print "\t\t\tTime --> NCP " + str(NumberCPVals[index1]) + "\t\t Time " + str(ProtocolTimes[index2])



#print "\n\n\n\t\t-----Finished Optimizing Time -----\n\n\n"


#for index1 in range(len(NumberCPVals)):

#	for index2 in range(len(ProtocolTimes)):

#		OptimalResult,NaiveCP,TimeAlloc = SpaceOpt.Driver_PreRead(NumberCPVals[index1],ProtocolTimes[index2],CPVals_Vector,LagTime_Vector,CorrelationArray)

#		OptimalSpace = list(OptimalResult.x)
#		OptimalCP = [CPStart]
#		CPCounter = CPStart

#		for index3 in range(len(OptimalSpace)):
#			CPCounter = CPCounter + OptimalSpace[index3]
#			OptimalCP.append(CPCounter)

#		TimeAlloc.append(PaddingTime)
#		TimeAlloc.insert(0,PaddingTime)
#		NaiveCP.append(1)
#		NaiveCP.insert(0,-1)

#		WriteNameSpace = "SpaceOpt_CP" + str(NumberCPVals[index1]) + "_T" + str(ProtocolTimes[index2]) + ".dat"
#		WriteNameLog = "OptimizerLogFile-Space_CP" + str(NumberCPVals[index1]) + "_T" + str(ProtocolTimes[index2]) + ".dat"

#		WriteData.WriteProtocol(WritePath,WriteNameSpace,OptimalCP,TimeAlloc)
#		WriteData.OptimizerLog(WritePathLog,WriteNameLog,OptimalResult)

#		print "\t\t\tSpace --> NCP " + str(NumberCPVals[index1]) + "\t\t Time " + str(ProtocolTimes[index2])



#print "\n\n\t\t-----Finished Optimizing Space-----\n"



for index1 in range(len(NumberCPVals)):

	for index2 in range(len(ProtocolTimes)):

		OptimalCP,OptimalTime,NaiveCP,NaiveTime = FullOpt.Driver_PreRead_Brute(FullOptimizerIterations,NumberCPVals[index1],ProtocolTimes[index2],CPVals_Vector,LagTime_Vector,CorrelationArray)

		OptimalTime.append(PaddingTime)
		OptimalTime.insert(0,PaddingTime)
		NaiveTime.append(PaddingTime)
		NaiveTime.insert(0,PaddingTime)

		WriteNameFull = "FullOpt_CP" + str(NumberCPVals[index1]) + "_T" + str(ProtocolTimes[index2]) + ".dat"

		WriteData.WriteProtocol(WritePath,WriteNameFull,OptimalCP,OptimalTime)

		print "\t\t\tFull --> NCP " + str(NumberCPVals[index1]) + "\t\t Time " + str(ProtocolTimes[index2])


Stop = timeit.default_timer()

print "\n\n----- Optimal Protocol Generation Finished -----\n\n"

print "Execution Time --> " + str(Stop - Start) + " seconds\n\n"

