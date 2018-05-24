#This is a refined python script to perform the temporal optimization of a Discrete nonequilbirium control protocol
#
#Steven Large
#February 19th 2018

import os
import numpy as np

import scipy.optimize


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


def CostFunction(TimeVals, CPIndex, TimeArray, CorrelationTuple):

	Func = 0

	for index in range(len(TimeVals)): 						#Linear interpolation between meshed values

		TimeIndex = FindIndex(TimeArray,TimeVals[index])
		Slope = 0.5*10*(CorrelationTuple[CPIndex[index]][TimeIndex+1] - CorrelationTuple[CPIndex[index]][TimeIndex-1])
		Func = Func + (CorrelationTuple[CPIndex[index]][TimeIndex] + Slope*(TimeVals[index] - TimeArray[TimeIndex]))

	return Func


def CorrelationTuple(CorrelationArray):

	HalfTuple = []

	for index in range(len(CorrelationArray)):
		HalfTuple.append(tuple(CorrelationArray[index]))

	CorrelationTuple = tuple(HalfTuple)

	return CorrelationTuple


def CreateBoundTuple(NumVals):

	Bound = (0,None)

	MasterList = []

	for index in range(NumVals):
		MasterList.append(Bound)

	MasterTuple = tuple(MasterList)

	return MasterTuple


def Driver(NumCPVals,TotalTime,ReadPath="/Users/stevelarge/Research/DiscreteControl/LinkedCode_CPP/Equilibrium_FromCluster/CorrelationMesh_9_15/",
		   Filename_CorrArray="CorrelationMesh_2.dat",
		   Filename_CP="CPVals_2.dat",
		   Filename_LagTime="LagTime_2.dat"):

	CPVals = ReadVector(ReadPath,Filename_CP)
	LagTime = ReadVector(ReadPath,Filename_LagTime)
	CorrelationMesh = ReadCorrelationArray(ReadPath,Filename_CorrArray)

	OptimalResult,NaiveTimeAlloc,CPStep = Driver_PreRead(NumCPVals,TotalTime,CPVals,LagTime,CorrelationMesh)

	return OptimalResult, NaiveTimeAlloc, CPStep
	
	
def Driver_PreRead(NumCPVals,TotalTime,CPVals,LagTime,CorrelationMesh): 			#This is the same as "Driver" but has the correlation matrix and CP vals ect already read in

	#CPMin = CPVals[0]
	#CPMax = CPVals[-1]

	CPMin = -1
	CPMax = 1

	#CPStepSize = (CPMax - CPMin)/float(NumCPVals - 1)
	CPStepSize = float((CPMax - CPMin))/float(NumCPVals - 1)

	CP_Counter = CPMin
	CPStep = []

	for index in range(NumCPVals):
		CPStep.append(CP_Counter)
		CP_Counter = CP_Counter + CPStepSize

	CPIndexArray = []

	for index in range(len(CPStep)):
		CPIndexArray.append(FindIndex(CPVals,CPStep[index]))

	CPIndexArray.remove(CPIndexArray[0]) 								#Remove Padding-index values from the array
	CPIndexArray.remove(CPIndexArray[-1])

	TimeAlloc = []
	NumTimeVals = NumCPVals - 2
	NaiveTimeAlloc = TotalTime/float(NumTimeVals)

	for index in range(NumTimeVals):
		TimeAlloc.append(NaiveTimeAlloc)

	NaiveTimeAlloc = TimeAlloc

	LagTimeTuple = tuple(LagTime)
	CPIndexTuple = tuple(CPIndexArray)
	TimeAlloc_Tuple = tuple(TimeAlloc)
	CorrelationArray_Tuple = CorrelationTuple(CorrelationMesh)

	Parameter_Tuple = (CPIndexTuple,LagTimeTuple,CorrelationArray_Tuple)

	Cons = ({'type':'eq','fun':lambda TimeAlloc_Tuple : sum(TimeAlloc_Tuple) - TotalTime})
	Bnds = CreateBoundTuple(len(TimeAlloc))

	OptimalResult = scipy.optimize.minimize(CostFunction, TimeAlloc_Tuple, args=Parameter_Tuple, method='SLSQP', bounds=Bnds, constraints=Cons) #, options={'maxiter':500,'ftol':1e-07})

	return OptimalResult, NaiveTimeAlloc, CPStep

	
def Driver_PreRead_COBYLA(NumCPVals,TotalTime,CPVals,LagTime,CorrelationMesh): 			#This is the same as "Driver" but has the correlation matrix and CP vals ect already read in

	#CPMin = CPVals[0]
	#CPMax = CPVals[-1]

	CPMin = -1
	CPMax = 1

	#CPStepSize = (CPMax - CPMin)/float(NumCPVals - 1)
	CPStepSize = float((CPMax - CPMin))/float(NumCPVals - 1)

	CP_Counter = CPMin
	CPStep = []

	for index in range(NumCPVals):
		CPStep.append(CP_Counter)
		CP_Counter = CP_Counter + CPStepSize

	CPIndexArray = []

	for index in range(len(CPStep)):
		CPIndexArray.append(FindIndex(CPVals,CPStep[index]))

	CPIndexArray.remove(CPIndexArray[0]) 								#Remove Padding-index values from the array
	CPIndexArray.remove(CPIndexArray[-1])

	TimeAlloc = []
	NumTimeVals = NumCPVals - 2
	NaiveTimeAlloc = TotalTime/float(NumTimeVals)

	for index in range(NumTimeVals):
		TimeAlloc.append(NaiveTimeAlloc)

	NaiveTimeAlloc = TimeAlloc

	LagTimeTuple = tuple(LagTime)
	CPIndexTuple = tuple(CPIndexArray)
	TimeAlloc_Tuple = tuple(TimeAlloc)
	CorrelationArray_Tuple = CorrelationTuple(CorrelationMesh)

	Parameter_Tuple = (CPIndexTuple,LagTimeTuple,CorrelationArray_Tuple)

	#Cons = ({'type':'eq','fun':lambda TimeAlloc_Tuple : sum(TimeAlloc_Tuple) - TotalTime}) 			#Assumes that the RHS is greater than or equal to zero by default
	Cons = ({'type':'ineq','fun':lambda TimeAlloc_Tuple : TotalTime - sum(TimeAlloc_Tuple)})
	Bnds = CreateBoundTuple(len(TimeAlloc))

	OptimalResult = scipy.optimize.minimize(CostFunction, TimeAlloc_Tuple, args=Parameter_Tuple, method='COBYLA', bounds=Bnds, constraints=Cons) #, options={'maxiter':500,'ftol':1e-07})

	return OptimalResult, NaiveTimeAlloc, CPStep


	
def Driver_PreRead_SLSQP(NumCPVals,TotalTime,CPVals,LagTime,CorrelationMesh): 			#This is the same as "Driver" but has the correlation matrix and CP vals ect already read in

	#CPMin = CPVals[0]
	#CPMax = CPVals[-1]

	CPMin = -1
	CPMax = 1

	#CPStepSize = (CPMax - CPMin)/float(NumCPVals - 1)
	CPStepSize = float((CPMax - CPMin))/float(NumCPVals - 1)

	CP_Counter = CPMin
	CPStep = []

	for index in range(NumCPVals):
		CPStep.append(CP_Counter)
		CP_Counter = CP_Counter + CPStepSize

	CPIndexArray = []

	for index in range(len(CPStep)):
		CPIndexArray.append(FindIndex(CPVals,CPStep[index]))

	CPIndexArray.remove(CPIndexArray[0]) 								#Remove Padding-index values from the array
	CPIndexArray.remove(CPIndexArray[-1])

	TimeAlloc = []
	NumTimeVals = NumCPVals - 2
	NaiveTimeAlloc = TotalTime/float(NumTimeVals)

	for index in range(NumTimeVals):
		TimeAlloc.append(NaiveTimeAlloc)

	NaiveTimeAlloc = TimeAlloc

	LagTimeTuple = tuple(LagTime)
	CPIndexTuple = tuple(CPIndexArray)
	TimeAlloc_Tuple = tuple(TimeAlloc)
	CorrelationArray_Tuple = CorrelationTuple(CorrelationMesh)

	Parameter_Tuple = (CPIndexTuple,LagTimeTuple,CorrelationArray_Tuple)

	#Cons = ({'type':'eq','fun':lambda TimeAlloc_Tuple : sum(TimeAlloc_Tuple) - TotalTime}) 			#Assumes that the RHS is greater than or equal to zero by default
	Cons = ({'type':'ineq','fun':lambda TimeAlloc_Tuple : TotalTime - sum(TimeAlloc_Tuple)})
	Bnds = CreateBoundTuple(len(TimeAlloc))

	OptimalResult = scipy.optimize.minimize(CostFunction, TimeAlloc_Tuple, args=Parameter_Tuple, method='SLSQP', bounds=Bnds, constraints=Cons) #, options={'maxiter':500,'ftol':1e-07})

	return OptimalResult, NaiveTimeAlloc, CPStep
