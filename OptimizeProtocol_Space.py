#This is the time optimization module that takes in an argument "Protocol" which is the naive time spent at each CP value and optimizes the spatial allocation from an input correlation matrix
#
#Steven Large
#Februrary 11th 2018

import os
import numpy as np

import scipy.optimize

import matplotlib.pyplot as plt

import CorrelationFit
import Plotting


def ReadCorrelationArray(Path,Filename):

	CompleteName = os.path.join(Path,Filename)

	CorrelationArray = []

	file1 = open(CompleteName,'r')
	TotalData = file1.readlines()
	file1.close()

	for index1 in range(len(TotalData)):
		Parsed = TotalData[index1].split()
		CorrelationArray.append([])
		for index2 in range(len(Parsed)):
			CorrelationArray[index1].append(eval(Parsed[index2]))

	return CorrelationArray


def ReadVector(Path,Filename):

	CompleteName = os.path.join(Path,Filename)

	Data = []

	file1 = open(CompleteName,'r')
	TempData = file1.readlines()
	file1.close()

	for index in range(len(TempData)):
		Parsed = TempData[index].split()
		Data.append(eval(Parsed[0]))

	return Data


def ReadCorrelationArray(Path,Filename):

	CompleteName = os.path.join(Path,Filename)

	CorrelationArray = []

	file1 = open(CompleteName,'r')
	TotalData = file1.readlines()
	file1.close()

	for index1 in range(len(TotalData)):
		Parsed = TotalData[index1].split()
		CorrelationArray.append([])
		for index2 in range(len(Parsed)):
			CorrelationArray[index1].append(eval(Parsed[index2]))

	return CorrelationArray


def ReadVector(Path,Filename):

	CompleteName = os.path.join(Path,Filename)

	Data = []

	file1 = open(CompleteName,'r')
	TempData = file1.readlines()
	file1.close()

	for index in range(len(TempData)):
		Parsed = TempData[index].split()
		Data.append(eval(Parsed[0]))

	return Data


def FindIndex(Array,Value):

	IndexArray = []

	TargetIndex = min(range(len(Array)), key=lambda i: abs(Value - Array[i]))

	return TargetIndex


def CostFunction(TimeVals, *argv):

	Func = 0

	for index in range(len(TimeVals)):

		Func = Func + argv[4*index]*np.exp(-argv[4*index + 1]*TimeVals[index]) + argv[4*index + 2]*np.exp(-argv[4*index + 3]*TimeVals[index])

	return Func



def CostFunction2(CPVals, TimeIndex, CPArray, CorrelationTuple):

	Func = 0
	TimeIndex = []

	dX = 0.05 												#This value will change

	for index in range(len(CPVals)): 						#Linear interpolation between meshed values

		CPIndex = FindIndex(CPArray,CPVals[index])
		Slope = 0.5*(float(1)/dX)*(CorrelationTuple[CPIndex+1][TimeIndex] - CorrelationTuple[CPIndex-1][TimeIndex])
		Func = Func + CorrelationTuple[CPIndex][TimeIndex] + Slope*(CPVals[index] - CPArray[CPIndex])

	return Func


def CostFunction3(CPDiffVals, CPStart, TimeIndex, CPArray, CorrelationTuple):

	TempCPVals = [CPStart]
	CPCounter = CPStart

	Func = 0
	dX = 0.5

	for index in range(len(CPDiffVals)): 										#Reconstruct the CP values from the starting point and the sequence of differences
		CPCounter = CPCounter + CPDiffVals[index]
		TempCPVals.append(CPCounter)


	BoundaryCost = CPDiffVals[0]*CPDiffVals[0]*CorrelationTuple[0][0]			#The boundary cost has no time dependence
	TemporalCost = 0
	SpatialCost = 0


	for index in range(len(CPDiffVals)-1):

		CPIndex = FindIndex(CPArray,TempCPVals[index+1])
		Slope = 0.5*(float(1)/dX)*(CorrelationTuple[CPIndex+1][TimeIndex] - CorrelationTuple[CPIndex-1][TimeIndex])
		TemporalCost = TemporalCost + CPDiffVals[index]*CPDiffVals[index+1]*(CorrelationTuple[CPIndex][TimeIndex] + Slope*(TempCPVals[index+1] - CPArray[CPIndex]))
		SpatialCost = SpatialCost + CPDiffVals[index+1]*CPDiffVals[index+1]*CorrelationTuple[CPIndex][0]

	Func = BoundaryCost + SpatialCost + TemporalCost

	return Func


def CorrelationTuple(CorrelationArray):

	HalfTuple = []

	for index in range(len(CorrelationArray)):
		HalfTuple.append(tuple(CorrelationArray[index]))

	CorrelationTuple = tuple(HalfTuple)

	return CorrelationTuple


def FixedTimeCons(TimeVals):

	Val = 0

	for index in range(len(TimeVals)):

		Val = Val + TimeVals[index]

	return Val - TotalTime


def CreateBoundTuple(NumVals,CPMax):

	Bound = (0,CPMax)

	MasterList = []

	for index in range(NumVals):
		MasterList.append(Bound)

	MasterTuple = tuple(MasterList)

	return MasterTuple


def Driver(NumCPVals,TotalTime,ReadPath="CorrelationMesh/",
		   Filename_CorrArray="CorrelationMesh.dat",
		   Filename_CP="CPVals.dat",
		   Filename_LagTime="LagTime.dat"):

	CPVals = ReadVector(ReadPath,Filename_CP)
	LagTime = ReadVector(ReadPath,Filename_LagTime)
	CorrelationMesh = ReadCorrelationArray(ReadPath,Filename_CorrArray)

	CPMin = CPVals[0]
	CPMax = CPVals[-1]

	CPMin = CPVals[0]
	CPMax = CPVals[-1]

	CPStepSize = (CPMax - CPMin)/(NumCPVals-1)

	CP_Counter = CPMin
	CPStep = []

	for index in range(NumCPVals):
		CPStep.append(CP_Counter)
		CP_Counter = CP_Counter + CPStepSize

	CPIndexArray = []

	for index in range(len(CPStep)):
		CPIndexArray.append(FindIndex(CPVals,CPStep[index]))

	A_Array = []
	B_Array = []
	C_Array = []
	D_Array = []

	for index in range(len(CPIndexArray)):

		Parameters = CorrelationFit.Driver(LagTime,CorrelationMesh[CPIndexArray[index]])
		A_Array.append(Parameters[0])
		B_Array.append(Parameters[1])
		C_Array.append(Parameters[2])
		D_Array.append(Parameters[3])

	X_Data = np.asarray(LagTime)

	TimeAlloc = []
	NumTimeVals = NumCPVals - 2
	NaiveTimeAlloc = TotalTime/NumTimeVals

	for index in range(NumTimeVals):
		TimeAlloc.append(NaiveTimeAlloc)

	NaiveTimeAlloc = TimeAlloc

	TimeAlloc_Tuple = tuple(TimeAlloc)
	Parameter_Tuple = MasterParameterTuple(A_Array,B_Array,C_Array,D_Array)

	Cons = ({'type':'eq','fun':lambda TimeAlloc_Tuple : sum(TimeAlloc_Tuple) - TotalTime})
	Bnds = CreateBoundTuple(len(TimeAlloc))

	OptimalResult = scipy.optimize.minimize(CostFunction, TimeAlloc_Tuple, args=Parameter_Tuple, method='SLSQP', bounds=Bnds, constraints=Cons)

	return OptimalResult, NaiveTimeAlloc, CPStep



def Driver_PreRead_NoFit(NumCPVals,TotalTime,CPVals,LagTime,CorrelationMesh): 			#This is the same as "Driver" but has the correlation matrix and CP vals ect already read in

	CPMin = CPVals[0]
	CPMax = CPVals[-1]

	CPStepSize = (CPMax - CPMin)/(NumCPVals-1)
	TotalCPDist = (CPMax - CPMin)

	CP_Counter = CPMin
	CPStep = []

	for index in range(NumCPVals):
		CPStep.append(CP_Counter)
		CP_Counter = CP_Counter + CPStepSize

	#print "\t\tCPStep --> " + str(CPStep) + "\n\n"

	#CPIndexArray = []


	#for index in range(len(CPStep)):
	#	CPIndexArray.append(FindIndex(CPVals,CPStep[index]))

	#CPIndexArray.remove(CPIndexArray[0]) 							#Remove Padding-index values from the array
	#CPIndexArray.remove(CPIndexArray[-1])

	CPAlloc = CPStep

	CPDiff = []

	for index in range(len(CPAlloc)-1):
		CPDiff.append(CPAlloc[index+1]-CPAlloc[index])

	CPAlloc.remove(CPAlloc[0])
	CPAlloc.remove(CPAlloc[-1])

	TimeAlloc = []
	NumTimeVals = NumCPVals - 2
	NaiveTimeAlloc = TotalTime/NumTimeVals

	TimeIndex = FindIndex(LagTime,NaiveTimeAlloc)

	for index in range(NumTimeVals):
		TimeAlloc.append(NaiveTimeAlloc)

	#NaiveTimeAlloc = TimeAlloc

	NaiveCPAlloc = CPAlloc
	NaiveCPAlloc.append(1)
	NaiveCPAlloc.insert(0,-1)

	#LagTimeTuple = tuple(LagTime)
	#CPIndexTuple = tuple(CPIndexArray)
	CPTuple = tuple(CPVals)
	#TimeAlloc_Tuple = tuple(TimeAlloc)
	#CPAlloc_Tuple = tuple(CPAlloc)
	CorrelationArray_Tuple = CorrelationTuple(CorrelationMesh)

	CPDiff_Tuple = tuple(CPDiff)

	CPStart = -1

	#Parameter_Tuple = (CPIndexTuple,LagTimeTuple)
	#Parameter_Tuple = (CPIndexTuple,LagTimeTuple,CorrelationArray_Tuple)
	Parameter_Tuple = (CPStart,TimeIndex,CPTuple,CorrelationArray_Tuple)

	#Cons = ({'type':'eq','fun':lambda TimeAlloc_Tuple : sum(TimeAlloc_Tuple) - TotalTime})
	#Bnds = CreateBoundTuple(len(TimeAlloc))

	Cons = ({'type':'eq','fun':lambda CPDiff_Tuple : sum(CPDiff_Tuple) - TotalCPDist})
	Bnds = CreateBoundTuple(len(CPDiff_Tuple),TotalCPDist)

	print "Constraints --> " + str(Cons) + "\n\n"
	print "Bounds --> " + str(Bnds) + "\n\n"

	Cost = CostFunction3(CPDiff_Tuple,Parameter_Tuple[0],Parameter_Tuple[1],Parameter_Tuple[2],Parameter_Tuple[3])

	print "Cost --> " + str(Cost) + "\n\n"

	#OptimalResult = scipy.optimize.minimize(CostFunction2, TimeAlloc_Tuple, args=Parameter_Tuple, method='SLSQP', bounds=Bnds, constraints=Cons)

	OptimalResult = scipy.optimize.minimize(CostFunction3, CPDiff_Tuple, args=Parameter_Tuple, method="SLSQP", bounds=Bnds, constraints=Cons)

	#OptimalResult = 1

	return OptimalResult, NaiveCPAlloc, TimeAlloc



ReadPath = "CorrelationMesh/"
Filename_CP = "CPVals.dat"
Filename_LagTime = "LagTime.dat"
Filename_CorrArray = "CorrelationMesh.dat"
Filename_ForceVar = "FisherInformation.dat"

CPVals = ReadVector(ReadPath,Filename_CP)
LagTime = ReadVector(ReadPath,Filename_LagTime)
CorrelationMesh = ReadCorrelationArray(ReadPath,Filename_CorrArray)

NumCPVals = 7
TotalTime = 1000

OptimalResult,NaiveCPAlloc,TimeAlloc = Driver_PreRead_NoFit(NumCPVals,TotalTime,CPVals,LagTime,CorrelationMesh)

OptimalCPDiff = list(OptimalResult.x)

OptimalCP = [-1]
CPCounter = -1

for index in range(len(OptimalCPDiff)):
	CPCounter = CPCounter + OptimalCPDiff[index]
	OptimalCP.append(CPCounter)

TimeAlloc.append(100)
TimeAlloc.insert(0,100)

plt.plot(OptimalCP,TimeAlloc,'b--')
plt.plot(NaiveCPAlloc,TimeAlloc,'r--')
plt.plot(OptimalCP,TimeAlloc,'bo')
plt.plot(NaiveCPAlloc,TimeAlloc,'ro')

plt.show()
plt.close()


