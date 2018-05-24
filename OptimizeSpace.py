#This is a refined Python script that optimizes the spatial palcement of CP values in discrete nonequilibrium protocols
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


def CostFunction(CPDiffVals, CPStart, TimeIndex, CPArray, CorrelationTuple):

	TempCPVals = [CPStart]
	CPCounter = CPStart

	Func = 0
	dX = 0.005

	for index in range(len(CPDiffVals)): 											#Reconstruct the CP values from the starting point and the sequence of differences
		CPCounter = CPCounter + CPDiffVals[index]
		TempCPVals.append(CPCounter)

	BoundaryCost = 0.5*CPDiffVals[0]*CPDiffVals[0]*CorrelationTuple[0][0]			#The boundary cost has no time dependence
	TemporalCost = 0
	SpatialCost = 0

	for index in range(len(CPDiffVals)-1):

		CPIndex = FindIndex(CPArray,TempCPVals[index+1])
		SlopeTime = 0.5*(float(1)/dX)*(CorrelationTuple[CPIndex+1][TimeIndex] - CorrelationTuple[CPIndex][TimeIndex])
		SlopeSpace = 0.5*(float(1)/dX)*(CorrelationTuple[CPIndex+1][0] - CorrelationTuple[CPIndex][0])
		TemporalCost = TemporalCost + CPDiffVals[index]*CPDiffVals[index+1]*(CorrelationTuple[CPIndex][TimeIndex] + SlopeTime*(TempCPVals[index+1] - CPArray[CPIndex]))
		SpatialCost = SpatialCost + 0.5*CPDiffVals[index+1]*CPDiffVals[index+1]*(CorrelationTuple[CPIndex][0] + SlopeSpace*(TempCPVals[index+1] - CPArray[CPIndex]))

	Func = BoundaryCost + SpatialCost + TemporalCost

	return Func


def CostFunctionInfinite(CPDiffVals, CPStart, TimeIndex, CPArray, CorrelationTuple):

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


def CorrelationTuple(CorrelationArray):

	HalfTuple = []

	for index in range(len(CorrelationArray)):
		HalfTuple.append(tuple(CorrelationArray[index]))

	CorrelationTuple = tuple(HalfTuple)

	return CorrelationTuple


def CreateBoundTuple(NumVals,CPMax):

	Bound = (0,CPMax)

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

	OptimalResult,NaiveCPAlloc,TimeAlloc = Driver_PreRead(NumCPVals,TotalTime,CPVals,LagTime,CorrelationMesh)

	return OptimalResult,NaiveCPAlloc,TimeAlloc


def Driver_PreRead(NumCPVals,TotalTime,CPVals,LagTime,CorrelationMesh): 			

	#CPMin = CPVals[0]
	#CPMax = CPVals[-1]

	CPMin = -1
	CPMax = 1

	CPStepSize = float((CPMax - CPMin))/float(NumCPVals-1)
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

	TimeIndex = FindIndex(LagTime,NaiveTimeAlloc)

	for index in range(NumTimeVals):
		TimeAlloc.append(NaiveTimeAlloc)

	NaiveCPAlloc = CPAlloc

	CPTuple = tuple(CPVals)
	CorrelationArray_Tuple = CorrelationTuple(CorrelationMesh)
	CPDiff_Tuple = tuple(CPDiff)

	CPStart = float(-1.0)

	Parameter_Tuple = (CPStart,TimeIndex,CPTuple,CorrelationArray_Tuple)

	Cons = ({'type':'eq','fun':lambda CPDiff_Tuple : sum(CPDiff_Tuple) - TotalCPDist})
	Bnds = CreateBoundTuple(len(CPDiff_Tuple),TotalCPDist)

	OptimalResult = scipy.optimize.minimize(CostFunctionInfinite, CPDiff_Tuple, args=Parameter_Tuple, method="SLSQP", bounds=Bnds, constraints=Cons, options={'ftol':1e-07})

	return OptimalResult, NaiveCPAlloc, TimeAlloc







