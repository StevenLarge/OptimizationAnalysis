#This Python script performs the full optimization of a Discrete nonequilibrium protocol based on iterated optimization of time and space components
#
#Steven Large
#February 18th 2018

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



def SpatialCostFunction(CPDiffVals, CPStart, TimeIndexArray, CPArray, CorrelationTuple):

	TempCPVals = [CPStart]
	CPCounter = CPStart

	Func = 0
	dX = 0.005

	for index in range(len(CPDiffVals)): 										#Reconstruct the CP values from the starting point and the sequence of differences
		CPCounter = CPCounter + CPDiffVals[index]
		TempCPVals.append(CPCounter)

	BoundaryCost = 0.5*CPDiffVals[0]*CPDiffVals[0]*CorrelationTuple[0][0]			#The boundary cost has no time dependence
	TemporalCost = 0
	SpatialCost = 0

	for index in range(len(CPDiffVals)-1):

		CPIndex = FindIndex(CPArray,TempCPVals[index+1])
		SlopeTime = (float(1)/float(dX))*(CorrelationTuple[CPIndex+1][TimeIndexArray[index]] - CorrelationTuple[CPIndex][TimeIndexArray[index]])
		SlopeSpace = (float(1)/float(dX))*(CorrelationTuple[CPIndex+1][0] - CorrelationTuple[CPIndex][0])
		TemporalCost = TemporalCost + CPDiffVals[index]*CPDiffVals[index+1]*(CorrelationTuple[CPIndex][TimeIndexArray[index]] + SlopeTime*(TempCPVals[index+1] - CPArray[CPIndex]))
		SpatialCost = SpatialCost + 0.5*CPDiffVals[index+1]*CPDiffVals[index+1]*(CorrelationTuple[CPIndex][0] + SlopeSpace*(TempCPVals[index+1] - CPArray[CPIndex]))

	Func = BoundaryCost + SpatialCost + TemporalCost

	return Func



def SpatialCostFunctionInfinite(CPDiffVals, CPStart, TimeIndexArray, CPArray, CorrelationTuple):

	TempCPVals = [CPStart]
	CPCounter = CPStart

	SpatialCost = 0

	dX = 0.005

	for index in range(len(CPDiffVals)): 										#Reconstruct the CP values from the starting point and the sequence of differences
		CPCounter = CPCounter + CPDiffVals[index]
		TempCPVals.append(CPCounter)

	for index in range(len(CPDiffVals)):
		CPIndex = FindIndex(CPArray,TempCPVals[index])
		#SlopeSpace = (float(1)/dX)*(CorrelationTuple[CPIndex+1][0] - CorrelationTuple[CPIndex][0])
		SlopeSpace = float(0.0)
		SpatialCost = SpatialCost + 0.5*CPDiffVals[index]*CPDiffVals[index]*(CorrelationTuple[CPIndex][0] + SlopeSpace*(TempCPVals[index] - CPArray[CPIndex]))

	return SpatialCost


def CostFunction(InputTuple, CPStart, NumTimeAlloc, TimeArray, CPArray, CorrelationTuple):

	TimeVals = InputTuple[0:NumTimeAlloc]
	CPDiffVals = InputTuple[NumTimeAlloc:len(InputTuple)]

	#print "\t\tTime Vals --> " + str(TimeVals)
	#print "\t\tCPDiffVals --> " + str(CPDiffVals) + "\n\n"

	TempCPVals = [CPStart]
	CPCounter = CPStart

	dX = 0.005
	dT = 0.1

	for index in range(len(CPDiffVals)): 										#Reconstruct the CP values from the starting point and the sequence of differences
		CPCounter = CPCounter + CPDiffVals[index]
		TempCPVals.append(CPCounter)

	#print "TempCPVals --> " + str(TempCPVals) + "\n\n"

	BoundaryCost = CPDiffVals[0]*CPDiffVals[0]*CorrelationTuple[0][0]			#The boundary cost has no time dependence
	TemporalCost = 0
	SpatialCost = 0

	for index in range(len(CPDiffVals)-1):

		TimeIndex = FindIndex(TimeArray,TimeVals[index])
		CPIndex = FindIndex(CPArray,TempCPVals[index+1])
		SpaceSlopeZero = 0.5*(float(1)/dX)*(CorrelationTuple[CPIndex+1][TimeIndex] - CorrelationTuple[CPIndex-1][TimeIndex])
		SpaceSlope = 0.5*(float(1)/dX)*(CorrelationTuple[CPIndex+1][TimeIndex] - CorrelationTuple[CPIndex-1][TimeIndex])
		TimeSlope = 0.5*(float(1)/dT)*(CorrelationTuple[CPIndex][TimeIndex+1] - CorrelationTuple[CPIndex][TimeIndex-1])

		TemporalCost = TemporalCost + CPDiffVals[index]*CPDiffVals[index+1]*(CorrelationTuple[CPIndex][TimeIndex] + SpaceSlope*(TempCPVals[index+1] - CPArray[CPIndex]) + TimeSlope*(TimeVals[index] - TimeArray[TimeIndex]))
		SpatialCost = SpatialCost + CPDiffVals[index+1]*CPDiffVals[index+1]*(CorrelationTuple[CPIndex][0] + SpaceSlopeZero*(TempCPVals[index+1] - CPArray[CPIndex]))

	TotalCost = BoundaryCost + SpatialCost + TemporalCost

	return TotalCost


def TemporalCostFunction(TimeVals, CPIndex, TimeArray, CorrelationTuple):

	Func = 0

	for index in range(len(TimeVals)): 						#Linear interpolation between meshed values

		TimeIndex = FindIndex(TimeArray,TimeVals[index])
		Slope = 0.5*10*(CorrelationTuple[CPIndex[index]][TimeIndex+1] - CorrelationTuple[CPIndex[index]][TimeIndex-1])
		Func = Func + CorrelationTuple[CPIndex[index]][TimeIndex] + Slope*(TimeVals[index] - TimeArray[TimeIndex])

	return Func
	#return 1


def CorrelationTuple(CorrelationArray):

	HalfTuple = []

	for index in range(len(CorrelationArray)):
		HalfTuple.append(tuple(CorrelationArray[index]))

	CorrelationTuple = tuple(HalfTuple)

	return CorrelationTuple


def CreateBoundTuple(TotalNumBnds,CPMax,NumTimeVals):

	BoundTime = (0,None)
	BoundCP = (0,CPMax)

	MasterList = []

	for index in range(NumTimeVals):
		MasterList.append(BoundTime)

	for index in range(TotalNumBnds - NumTimeVals):
		MasterList.append(BoundCP)

	MasterTuple = tuple(MasterList)

	return MasterTuple


def CreateSpatialBounds(NumCPDiff,CPMax):

	Bound = (0,CPMax)

	MasterList = []

	for index in range(NumCPDiff):
		MasterList.append(Bound)

	MasterTuple = tuple(MasterList)

	return MasterTuple


def CreateTemporalBounds(NumTimes):

	Bound = (0,None)

	MasterList = []

	for index in range(NumTimes):
		MasterList.append(Bound)

	MasterTuple = tuple(MasterList)

	return MasterList


def Driver_PreRead_Brute(Iterations,NumCPVals,TotalTime,CPVals,LagTime,CorrelationMesh): 			
	
	#CPMin = CPVals[0]
	#CPMax = CPVals[-1]

	CPMin = -1
	CPMax = 1

	CPStepSize = float(CPMax - CPMin)/float(NumCPVals-1)
	TotalCPDist = float(CPMax - CPMin)

	CP_Counter = -1
	CPStep = []

	for index in range(NumCPVals):
		CPStep.append(CP_Counter)
		CP_Counter = CP_Counter + CPStepSize

	CPAlloc = CPStep

	CPDiff = []

	for index in range(len(CPAlloc)-1):
		CPDiff.append(CPAlloc[index+1]-CPAlloc[index])

	CPAlloc.remove(CPAlloc[0])
	CPAlloc.remove(CPAlloc[-1])

	TimeAlloc = []
	NumTimeVals = NumCPVals - 2
	NaiveTimeAlloc = TotalTime/float(NumTimeVals)

	for index in range(NumTimeVals):
		TimeAlloc.append(NaiveTimeAlloc)

	NaiveTimeAlloc = TimeAlloc
	NaiveCPAlloc = CPAlloc
	#NaiveCPDiff = CPDiff

	CP_Tuple = tuple(CPVals)
	LagTime_Tuple = tuple(LagTime)
	CorrelationArray_Tuple = tuple(CorrelationMesh)

	CPDiff_Tuple = tuple(CPDiff)
	TimeAlloc_Tuple = tuple(TimeAlloc)

	Cons_Space = ({'type':'eq','fun':lambda CPDiff_Tuple : sum(CPDiff_Tuple) - TotalCPDist})
	Cons_Time = ({'type':'eq','fun':lambda TimeAlloc_Tuple : sum(TimeAlloc_Tuple) - TotalTime})

	Bnds_Space = CreateSpatialBounds(len(CPDiff_Tuple),2)
	Bnds_Time = CreateTemporalBounds(len(TimeAlloc_Tuple))

	CPStart = float(-1)

	CostTracker = []

	for index in range(Iterations):

		TimeIndexArray = []

		for index2 in range(len(TimeAlloc)):
			TimeIndexArray.append(FindIndex(LagTime,TimeAlloc_Tuple[index2]))

		TimeIndex_Tuple = tuple(TimeIndexArray)

		SpaceParameter_Tuple = (CPStart, TimeIndex_Tuple, CP_Tuple, CorrelationArray_Tuple)

		#if index!=0:
		OptimalResult = scipy.optimize.minimize(SpatialCostFunctionInfinite, CPDiff_Tuple, args=SpaceParameter_Tuple, method="SLSQP", bounds=Bnds_Space, constraints=Cons_Space, options={'ftol':1e-07})

		CostTracker.append(OptimalResult.fun)

		OptimalCPDiff = list(OptimalResult.x)
		CPDiff_Tuple = tuple(OptimalCPDiff)

		#else:
		#	OptimalCPDiff = CPDiff

		CPArray = [CPStart]
		CPCounter = CPStart

		for index2 in range(len(OptimalCPDiff)):
			CPCounter = CPCounter + OptimalCPDiff[index2]
			CPArray.append(CPCounter)

		CPIndexArray = []

		for index2 in range(len(CPArray)):
			CPIndexArray.append(FindIndex(CPVals,CPArray[index2]))

		CPIndexArray.remove(CPIndexArray[0])
		CPIndexArray.remove(CPIndexArray[-1])

		CPIndex_Tuple = tuple(CPIndexArray)


		TimeParameter_Tuple = (CPIndex_Tuple,LagTime_Tuple,CorrelationArray_Tuple)


		OptimalResult = scipy.optimize.minimize(TemporalCostFunction, TimeAlloc_Tuple, args=TimeParameter_Tuple, method='SLSQP', bounds=Bnds_Time, constraints=Cons_Time)

		CostTracker.append(OptimalResult.fun)

		TimeAlloc = list(OptimalResult.x)


	OptimalCPDiff = list(CPDiff_Tuple)
	OptimalTime = list(TimeAlloc)

	OptimalCP = [CPStart]
	CPCounter = CPStart
	for index in range(len(OptimalCPDiff)):
		CPCounter = CPCounter + OptimalCPDiff[index]
		OptimalCP.append(CPCounter)

	NaiveCPAlloc.append(1)
	NaiveCPAlloc.insert(0,-1)

	return OptimalCP, OptimalTime, NaiveCPAlloc, NaiveTimeAlloc, CostTracker



def Driver_PreRead(NumCPVals,TotalTime,CPVals,LagTime,CorrelationMesh): 			
	
	#CPMin = CPVals[0]
	#CPMax = CPVals[-1]

	CPMin = -1
	CPMax = 1

	CPStepSize = float((CPMax - CPMin))/float(NumCPVals-1)
	TotalCPDist = float(CPMax - CPMin)

	CP_Counter = CPMin
	CPStep = []

	for index in range(NumCPVals):
		CPStep.append(CP_Counter)
		CP_Counter = CP_Counter + CPStepSize

	CPAlloc = CPStep

	CPDiff = []

	for index in range(len(CPAlloc)-1):
		CPDiff.append(CPAlloc[index+1]-CPAlloc[index])

	CPAlloc.remove(CPAlloc[0])
	CPAlloc.remove(CPAlloc[-1])

	TimeAlloc = []
	NumTimeVals = NumCPVals - 2
	NaiveTimeAlloc = float(TotalTime)/float(NumTimeVals)

	TimeIndex = FindIndex(LagTime,NaiveTimeAlloc)

	for index in range(NumTimeVals):
		TimeAlloc.append(NaiveTimeAlloc)

	NaiveCPAlloc = CPAlloc

	InputData = []
	for index in range(len(TimeAlloc)):
		InputData.append(TimeAlloc[index])

	for index in range(len(CPDiff)):
		InputData.append(CPDiff[index])

	#InputData = [tuple(NaiveTimeAlloc),tuple(CPDiff)]
	#InputData = []
	#InputData.append(tuple(TimeAlloc))
	#InputData.append(tuple(CPDiff))

	Input_Tuple = tuple(InputData)
	CP_Tuple = tuple(CPVals)
	LagTime_Tuple = tuple(LagTime)
	CorrelationArray_Tuple = CorrelationTuple(CorrelationMesh)
	CPDiff_Tuple = tuple(CPDiff)

	CPStart = -1
	NumTimeAlloc = len(TimeAlloc)

	Parameter_Tuple = (CPStart,NumTimeAlloc,LagTime_Tuple,CP_Tuple,CorrelationArray_Tuple)

	Cons = ({'type':'eq','fun':lambda Input_Tuple : sum(Input_Tuple[0:NumTimeAlloc]) - TotalTime},
			{'type':'eq','fun':lambda Input_Tuple : sum(Input_Tuple[NumTimeAlloc:len(Input_Tuple)]) - TotalCPDist})

	Bnds = CreateBoundTuple(len(Input_Tuple),TotalCPDist,NumTimeAlloc)

	print "Bounds --> " + str(Bnds) + "\n"

	#OBJECTIVE FUNCTION MUST RETURN A SCALAR ERROR

	OptimalResult = scipy.optimize.minimize(CostFunction, Input_Tuple, args=Parameter_Tuple, method="SLSQP", bounds=Bnds, constraints=Cons)

	#OptimalResult = 1

	OptimalResult_Time = OptimalResult.x[0:NumTimeAlloc]
	OptimalResult_Space = OptimalResult.x[NumTimeAlloc:len(OptimalResult.x)]

	print "\n\t\tOptimalTimes --> \t" + str(OptimalResult_Time)
	print "\n\t\tOptimal Diff --> \t" + str(OptimalResult_Space) + "\n\n"

	return OptimalResult, OptimalResult_Space, OptimalResult_Time, NaiveCPAlloc, TimeAlloc



