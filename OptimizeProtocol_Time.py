#This is the time optimization module that takes in an argument "Protocol" which is a set of discrete CPVals and optimizes the time allocation from an input correlation matrix
#
#Steven Large
#Februrary 11th 2018

import os
import numpy as np

import scipy.optimize

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


def FindIndex(Array,Value):

	IndexArray = []

	TargetIndex = min(range(len(Array)), key=lambda i: abs(Value - Array[i]))

	return TargetIndex


def CostFunction(TimeVals, *argv):

	Func = 0

	for index in range(len(TimeVals)):

		Func = Func + argv[4*index]*np.exp(-argv[4*index + 1]*TimeVals[index]) + argv[4*index + 2]*np.exp(-argv[4*index + 3]*TimeVals[index])

	return Func


def CostFunction2(TimeVals, CPIndex, TimeArray, CorrelationTuple):

	Func = 0
	TimeIndex = []

	for index in range(len(TimeVals)): 						#Linear interpolation between meshed values

		TimeIndex = FindIndex(TimeArray,TimeVals[index])
		Slope = 0.5*10*(CorrelationTuple[CPIndex[index]][TimeIndex+1] - CorrelationTuple[CPIndex[index]][TimeIndex-1])
		Func = Func + CorrelationTuple[CPIndex[index]][TimeIndex] + Slope*(TimeVals[index] - TimeArray[TimeIndex])

	return Func


def CorrelationTuple(CorrelationArray):

	HalfTuple = []

	for index in range(len(CorrelationArray)):
		HalfTuple.append(tuple(CorrelationArray[index]))

	CorrelationTuple = tuple(HalfTuple)

	return CorrelationTuple


def MasterParameterTuple(A,B,C,D):

	MasterList = []

	for index in range(len(A)-2): 				#Want to discard parameter for final and initial CP vals

		MasterList.append(A[index+1])
		MasterList.append(B[index+1])
		MasterList.append(C[index+1])
		MasterList.append(D[index+1])

	MasterTuple = tuple(MasterList)

	return MasterTuple


def FixedTimeCons(TimeVals):

	Val = 0

	for index in range(len(TimeVals)):

		Val = Val + TimeVals[index]

	return Val - TotalTime


def CreateBoundTuple(NumVals):

	Bound = (0,None)

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



def Driver_PreRead(NumCPVals,TotalTime,CPVals,LagTime,CorrelationMesh): 			#This is the same as "Driver" but has the correlation matrix and CP vals ect already read in

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

	CPMin = CPVals[0]
	CPMax = CPVals[-1]

	CPStepSize = (CPMax - CPMin)/(NumCPVals-1)

	CP_Counter = CPMin
	CPStep = []

	for index in range(NumCPVals):
		CPStep.append(CP_Counter)
		CP_Counter = CP_Counter + CPStepSize

	print "\t\tCPStep --> " + str(CPStep) + "\n\n"

	CPIndexArray = []

	for index in range(len(CPStep)):
		CPIndexArray.append(FindIndex(CPVals,CPStep[index]))

	CPIndexArray.remove(CPIndexArray[0]) 							#Remove Padding-index values from the array
	CPIndexArray.remove(CPIndexArray[-1])

	TimeAlloc = []
	NumTimeVals = NumCPVals - 2
	NaiveTimeAlloc = TotalTime/NumTimeVals

	for index in range(NumTimeVals):
		TimeAlloc.append(NaiveTimeAlloc)

	NaiveTimeAlloc = TimeAlloc

	LagTimeTuple = tuple(LagTime)
	CPIndexTuple = tuple(CPIndexArray)
	TimeAlloc_Tuple = tuple(TimeAlloc)
	CorrelationArray_Tuple = CorrelationTuple(CorrelationMesh)

	#Parameter_Tuple = (CPIndexTuple,LagTimeTuple)
	Parameter_Tuple = (CPIndexTuple,LagTimeTuple,CorrelationArray_Tuple)

	Cons = ({'type':'eq','fun':lambda TimeAlloc_Tuple : sum(TimeAlloc_Tuple) - TotalTime})
	Bnds = CreateBoundTuple(len(TimeAlloc))

	OptimalResult = scipy.optimize.minimize(CostFunction2, TimeAlloc_Tuple, args=Parameter_Tuple, method='SLSQP', bounds=Bnds, constraints=Cons)

	return OptimalResult, NaiveTimeAlloc, CPStep

