#This python script reads in the correlation array, Force variance and lag time data, determines the indices for naive-placement protocols and calculates the optimal time allocation
#
#Steven Large
#February 9th 2018

import os
import numpy as np
import matplotlib.pyplot as plt

import CorrelationFit
import Plotting

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


def MasterParameterTuple(A,B,C,D):

	MasterList = []

	for index in range(len(A)-2): 				#Want to discard parameter for final and initial CP vals

		MasterList.append(A[index+1])
		MasterList.append(B[index+1])
		MasterList.append(C[index+1])
		MasterList.append(D[index+1])

	MasterTuple = tuple(MasterList)

	return MasterTuple


def CostFunction(TimeVals,A,B,C,D):

	Func = 0

	for index in range(len(TimeVals)):

		Func = Func + A[index]*np.exp(-B[index]*TimeVals[index]) + C[index]*np.exp(-D[index]*TimeVals[index]) #CorrelationFit.Function(TimeVals[index],A[index],B[index],C[index],D[index])

	return float(Func)


def CostFunction2(TimeVals,Parameters):

	Func = 0

	for index in range(len(TimeVals)):

		Func = Func + Parameters[0][index]*np.exp(-Parameters[1][index]*TimeVals[index]) + Parameters[2][index]*np.exp(-Parameters[3][index]*TimeVals[index])

	return Func


def CostFunction3(TimeVals, *argv):

	Func = 0

	#print "COST FUNCTION argv -->" + str(argv)
	#print "COST FUNCTION TimeVals -->" + str(TimeVals)

	for index in range(len(TimeVals)):

		Func = Func + argv[4*index]*np.exp(-argv[4*index + 1]*TimeVals[index]) + argv[4*index + 2]*np.exp(-argv[4*index + 3]*TimeVals[index])

	return Func


def CostFunction3Alt(TimeVals, argv):

	Func = 0

	print "COST FUNCTION argv -->" + str(argv)
	print "COST FUNCTION TimeVals -->" + str(TimeVals)

	for index in range(len(TimeVals)):

		Func = Func + argv[4*index]*np.exp(-argv[4*index + 1]*TimeVals[index]) + argv[4*index + 2]*np.exp(-argv[4*index + 3]*TimeVals[index])

	return Func


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


ReadPath = "CorrelationMesh/"

Filename_CorrArray = "CorrelationMesh.dat"
Filename_CP = "CPVals.dat"
Filename_LagTime = "LagTime.dat"

print "Reading in CPVals -----"
CPVals = ReadVector(ReadPath,Filename_CP)
print "Reading in LagTime -----"
LagTime = ReadVector(ReadPath,Filename_LagTime)
print "Reading in CorrelationMesh -----"
CorrelationMesh = ReadCorrelationArray(ReadPath,Filename_CorrArray)

print "\n\nData Read into memory\n\n"

CPMin = CPVals[0]
CPMax = CPVals[-1]

NumCPVals = 9

#global TotalTime

TotalTime = 1000

CPStepSize = (CPMax - CPMin)/(NumCPVals-1)

CP_Counter = CPMin
CPStep = []

for index in range(NumCPVals):

	CPStep.append(CP_Counter)
	CP_Counter = CP_Counter + CPStepSize

#CPStep.append(CP_Counter)

print "CP Step values are --> " + str(CPStep)

CPIndexArray = []

print "\n\nFinding CP Index values -----\n\n"

for index in range(len(CPStep)):

	CPIndexArray.append(FindIndex(CPVals,CPStep[index]))


A_Array = []
B_Array = []
C_Array = []
D_Array = []

print "Calculating fit parameters -----\n\n"

for index in range(len(CPIndexArray)):

	Parameters = CorrelationFit.Driver(LagTime,CorrelationMesh[CPIndexArray[index]])
	A_Array.append(Parameters[0])
	B_Array.append(Parameters[1])
	C_Array.append(Parameters[2])
	D_Array.append(Parameters[3])

Plotting.PlotFunctionFits(CorrelationMesh,CPIndexArray,A_Array,B_Array,C_Array,D_Array,LagTime)

X_Data = np.asarray(LagTime)

TimeAlloc = []

NumTimeVals = NumCPVals - 2

NaiveTimeAlloc = float(TotalTime)/float(NumTimeVals)

for index in range(NumTimeVals):
	TimeAlloc.append(NaiveTimeAlloc)

#ParameterTuple = (A_Array,B_Array,C_Array,D_Array)

TimeAlloc_Tuple = tuple(TimeAlloc)

Parameter_Tuple = MasterParameterTuple(A_Array,B_Array,C_Array,D_Array)

print "Parameter Tuple --> " + str(Parameter_Tuple)
print "TimeAlloc_Tuple --> " + str(TimeAlloc_Tuple)

print "TimeAllocSum --> " + str(sum(TimeAlloc_Tuple))

#Cons = ({'type':'eq','fun':FixedTimeCons})
Cons = ({'type':'eq','fun':lambda TimeAlloc_Tuple: sum(TimeAlloc_Tuple) - TotalTime})
Bnds = CreateBoundTuple(len(TimeAlloc))


print "Bound Tuple --> " + str(Bnds)

print "Time Allocation --> \t" + str(TimeAlloc)

CostTest = CostFunction3Alt(TimeAlloc_Tuple,Parameter_Tuple)

print "Initial Cost --> \t" + str(CostTest)

print "\n\nStarting Optimization -----\n\n\n"

#OptimalResult = scipy.optimize.minimize(CostFunction2,TimeAlloc,method='SLSQP')

OptimalResult = scipy.optimize.minimize(CostFunction3, TimeAlloc_Tuple, args=Parameter_Tuple, method='SLSQP', bounds=Bnds, constraints=Cons)

print "Optimium --> " + str(OptimalResult.x)















