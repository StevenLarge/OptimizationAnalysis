#This is a refined Python script that optimizes the spatial palcement of CP values in discrete nonequilibrium protocols
#
#Steven Large
#February 18th 2018

import os
import numpy as np
from math import *

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


def CostFunction_CP(CPVals, TimeIndex, CPArray, CorrelationTuple):

	TempCPDiff = []

	for index in range(len(CPVals)-1):
		TempCPDiff.append(abs(CPVals[index+1]-CPVals[index]))

	Func = 0
	dX = 0.005

	BoundaryCost = TempCPDiff[0]*TempCPDiff[0]*CorrelationTuple[0][0]
	TemporalCost = 0
	SpatialCost = 0

	for index in range(len(TempCPDiff)-1):

		CPIndex = FindIndex(CPArray,CPVals[index+1])
		SlopeTime = (float(1)/dX)*(CorrelationTuple[CPIndex][TimeIndex] - CorrelationTuple[CPIndex-1][TimeIndex])
		SlopeSpace = (float(1)/dX)*(CorrelationTuple[CPIndex][0] - CorrelationTuple[CPIndex-1][0])
		TemporalCost = TemporalCost + TempCPDiff[index]*TempCPDiff[index+1]*(CorrelationTuple[CPIndex][TimeIndex] + SlopeTime*(CPVals[index+1] - CPArray[CPIndex]))
		SpatialCost = SpatialCost + 0.5*TempCPDiff[index+1]*TempCPDiff[index+1]*(CorrelationTuple[CPIndex][0] + SlopeSpace*(CPVals[index+1] - CPArray[CPIndex]))

	Func = BoundaryCost + SpatialCost + TemporalCost

	return Func


def CostFunction(CPDiffVals, CPStart, TimeIndex, CPArray, CorrelationTuple):

	TempCPVals = [CPStart]
	CPCounter = float(CPStart)

	Func = 0
	dX = 0.005
	dT = 0.1

	for index in range(len(CPDiffVals)): 										#Reconstruct the CP values from the starting point and the sequence of differences
		CPCounter = CPCounter + CPDiffVals[index]
		TempCPVals.append(CPCounter)


	BoundaryCost = CPDiffVals[0]*CPDiffVals[0]*CorrelationTuple[0][0]			#The boundary cost has no time dependence
	TemporalCost = float(0)
	SpatialCost = float(0)


	for index in range(len(CPDiffVals)-1):

		CPIndex = FindIndex(CPArray,TempCPVals[index+1])
		SlopeTime = (float(1)/float(dT))*(CorrelationTuple[CPIndex][TimeIndex] - CorrelationTuple[CPIndex-1][TimeIndex])
		SlopeSpace = (float(1)/float(dX))*(CorrelationTuple[CPIndex][0] - CorrelationTuple[CPIndex-1][0])
		#SlopeTime = 0.0
		#SlopeSpace = 0.0
		TemporalCost = TemporalCost + CPDiffVals[index]*CPDiffVals[index+1]*(CorrelationTuple[CPIndex][TimeIndex] + SlopeTime*(TempCPVals[index+1] - CPArray[CPIndex]))
		SpatialCost = SpatialCost + 0.5*CPDiffVals[index+1]*CPDiffVals[index+1]*(CorrelationTuple[CPIndex][0] + SlopeSpace*(TempCPVals[index+1] - CPArray[CPIndex]))

	Func = BoundaryCost + SpatialCost + TemporalCost

	return Func


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

def CreateBoundTuple_CP(NumVals,CPMin,CPMax):

	Bound = (CPMin,CPMax)

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

	OptimalResult,NaiveCPAlloc,TimeAlloc = Driver_PreRead(NumCPVals,TotalTime,CPVals,LagTime,CorrelationMesh)

	return OptimalResult,NaiveCPAlloc,TimeAlloc


def Driver_PreRead(NumCPVals,TotalTime,CPVals,LagTime,CorrelationMesh): 			

	#CPMin = CPVals[0]
	#CPMax = CPVals[-1]

	CPMin = -1
	CPMax = 1

	CPStepSize = float(CPMax - CPMin)/float(NumCPVals-1)
	TotalCPDist = float(CPMax - CPMin)

	CP_Counter = CPMin
	CPStep = []

	for index in range(NumCPVals):
		CPStep.append(CP_Counter)
		CP_Counter = CP_Counter + CPStepSize

	CPAlloc = CPStep

	#CPDiff = []

	#for index in range(len(CPAlloc)-1):
	#	CPDiff.append(CPAlloc[index+1]-CPAlloc[index])

	#CPAlloc.remove(CPAlloc[0])
	#CPAlloc.remove(CPAlloc[-1])

	TimeAlloc = []
	NumTimeVals = NumCPVals - 2
	NaiveTimeAlloc = TotalTime/float(NumTimeVals)

	TimeIndex = FindIndex(LagTime,NaiveTimeAlloc)

	for index in range(NumTimeVals):
		TimeAlloc.append(NaiveTimeAlloc)

	NaiveCPAlloc = CPAlloc

	CPTuple = tuple(CPVals)
	CorrelationArray_Tuple = CorrelationTuple(CorrelationMesh)
	#CPDiff_Tuple = tuple(CPDiff)
	CPStep_Tuple = tuple(CPStep)

	CPStart = -1

	#Parameter_Tuple = (CPStart,TimeIndex,CPTuple,CorrelationArray_Tuple)
	Parameter_Tuple = (TimeIndex,CPTuple,CorrelationArray_Tuple)

	#Cons = ({'type':'eq','fun':lambda CPDiff_Tuple : sum(CPDiff_Tuple) - TotalCPDist})
	#Bnds = CreateBoundTuple(len(CPDiff_Tuple),TotalCPDist)

	Cons = ({'type':'eq','fun':lambda CPStep_Tuple : CPStep_Tuple[0] - CPMin},{'type':'eq','fun':lambda CPStep_Tuple : CPStep_Tuple[-1] - CPMax})
	Bnds = CreateBoundTuple_CP(len(CPStep_Tuple),CPMin,CPMax)

	OptimalResult = scipy.optimize.minimize(CostFunction_CP, CPStep_Tuple, args=Parameter_Tuple, method="SLSQP", bounds=Bnds, constraints=Cons)

	return OptimalResult, NaiveCPAlloc, TimeAlloc







