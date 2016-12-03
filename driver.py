# XPS Python class
#
#  for XPS-Q8 Firmware Precision Platform V1.2.x
#
#  See Programmer's manual for more information on XPS function calls

import socket

class XPS:
	# Defines
	MAX_NB_SOCKETS = 100

	# Global variables
	__sockets = {}
	__usedSockets = {}
	__nbSockets = 0

	# Initialization Function
	def __init__ (self):
		XPS.__nbSockets = 0
		for socketId in range(self.MAX_NB_SOCKETS):
			XPS.__usedSockets[socketId] = 0

	# Send command and get return
	def __sendAndReceive (self, socketId, command):
		try:
			XPS.__sockets[socketId].send(command)
			ret = XPS.__sockets[socketId].recv(1024)
			while (ret.find(b',EndOfAPI') == -1):
				ret += XPS.__sockets[socketId].recv(1024)
			print("Entire response: {}".format(ret))
		except socket.timeout:
			return [-2, '']
		except socket.error (errNb, errString):
			print('Socket error : ' + errString)
			return [-2, '']

		for i in range(len(ret)):
			if (ret[i:i+1] == b','):
				return [int(ret[0:i]), ret[i+1:-9]]

	# TCP_ConnectToServer
	def TCP_ConnectToServer (self, IP, port, timeOut):
		socketId = 0
		if (XPS.__nbSockets < self.MAX_NB_SOCKETS):
			while (XPS.__usedSockets[socketId] == 1 and socketId < self.MAX_NB_SOCKETS):
				socketId += 1
			if (socketId == self.MAX_NB_SOCKETS):
				return -1
		else:
			return -1

		XPS.__usedSockets[socketId] = 1
		XPS.__nbSockets += 1
		try:
			XPS.__sockets[socketId] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			XPS.__sockets[socketId].connect((IP, port))
			XPS.__sockets[socketId].settimeout(timeOut)
			XPS.__sockets[socketId].setblocking(1)
		except socket.error:
			return -1

		return socketId

	# TCP_SetTimeout
	def TCP_SetTimeout (self, socketId, timeOut):
		if (XPS.__usedSockets[socketId] == 1):
			XPS.__sockets[socketId].settimeout(timeOut)

	# TCP_CloseSocket
	def TCP_CloseSocket (self, socketId):
		if (socketId >= 0 and socketId < self.MAX_NB_SOCKETS):
			try:
				XPS.__sockets[socketId].close()
				XPS.__usedSockets[socketId] = 0
				XPS.__nbSockets -= 1
			except socket.error:
				pass

	# GetLibraryVersion
	def GetLibraryVersion (self):
		return ['XPS-Q8 Firmware Precision Platform V1.2.x']

	# ControllerMotionKernelMinMaxTimeLoadGet :  Get controller motion kernel minimum and maximum time load
	def ControllerMotionKernelMinMaxTimeLoadGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ControllerMotionKernelMinMaxTimeLoadGet(double *,double *,double *,double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(8):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# ControllerMotionKernelMinMaxTimeLoadReset :  Reset controller motion kernel min/max time load
	def ControllerMotionKernelMinMaxTimeLoadReset (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ControllerMotionKernelMinMaxTimeLoadReset()'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# ControllerMotionKernelTimeLoadGet :  Get controller motion kernel time load
	def ControllerMotionKernelTimeLoadGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ControllerMotionKernelTimeLoadGet(double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# ControllerRTTimeGet :  Get controller corrector period and calculation time
	def ControllerRTTimeGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ControllerRTTimeGet(double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# ControllerSlaveStatusGet :  Read slave controller status
	def ControllerSlaveStatusGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ControllerSlaveStatusGet(int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# ControllerSlaveStatusStringGet :  Return the slave controller status string
	def ControllerSlaveStatusStringGet (self, socketId, SlaveControllerStatusCode):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ControllerSlaveStatusStringGet(' + str(SlaveControllerStatusCode).encode() + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# ControllerSynchronizeCorrectorISR :  Synchronize controller corrector ISR
	def ControllerSynchronizeCorrectorISR (self, socketId, ModeString):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ControllerSynchronizeCorrectorISR(' + ModeString.encode() + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# ControllerStatusGet :  Get controller current status and reset the status
	def ControllerStatusGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ControllerStatusGet(int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# ControllerStatusRead :  Read controller current status
	def ControllerStatusRead (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ControllerStatusRead(int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# ControllerStatusStringGet :  Return the controller status string
	def ControllerStatusStringGet (self, socketId, ControllerStatusCode):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ControllerStatusStringGet(' + str(ControllerStatusCode).encode() + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# ElapsedTimeGet :  Return elapsed time from controller power on
	def ElapsedTimeGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ElapsedTimeGet(double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# ErrorStringGet :  Return the error string corresponding to the error code
	def ErrorStringGet (self, socketId, ErrorCode):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ErrorStringGet(' + str(ErrorCode) + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# FirmwareVersionGet :  Return firmware version
	def FirmwareVersionGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'FirmwareVersionGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# TCLScriptExecute :  Execute a TCL script from a TCL file
	def TCLScriptExecute (self, socketId, TCLFileName, TaskName, ParametersList):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TCLScriptExecute(' + TCLFileName + ',' + TaskName + ',' + ParametersList + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# TCLScriptExecuteAndWait :  Execute a TCL script from a TCL file and wait the end of execution to return
	def TCLScriptExecuteAndWait (self, socketId, TCLFileName, TaskName, InputParametersList):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TCLScriptExecuteAndWait(' + TCLFileName + ',' + TaskName + ',' + InputParametersList + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# TCLScriptExecuteWithPriority :  Execute a TCL script with defined priority
	def TCLScriptExecuteWithPriority (self, socketId, TCLFileName, TaskName, TaskPriorityLevel, ParametersList):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TCLScriptExecuteWithPriority(' + TCLFileName + ',' + TaskName + ',' + TaskPriorityLevel + ',' + ParametersList + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# TCLScriptKill :  Kill TCL Task
	def TCLScriptKill (self, socketId, TaskName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TCLScriptKill(' + TaskName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# TCLScriptKillAll :  Kill all TCL Tasks
	def TCLScriptKillAll (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'TCLScriptKillAll()'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# TimerGet :  Get a timer
	def TimerGet (self, socketId, TimerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TimerGet(' + TimerName + ',int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# TimerSet :  Set a timer
	def TimerSet (self, socketId, TimerName, FrequencyTicks):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TimerSet(' + TimerName + ',' + str(FrequencyTicks) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# Reboot :  Reboot the controller
	def Reboot (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'Reboot()'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# Login :  Log in
	def Login (self, socketId, Name, Password):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'Login(' + Name + ',' + Password + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# CloseAllOtherSockets :  Close all socket beside the one used to send this command
	def CloseAllOtherSockets (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'CloseAllOtherSockets()'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# HardwareDateAndTimeGet :  Return hardware date and time
	def HardwareDateAndTimeGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'HardwareDateAndTimeGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# HardwareDateAndTimeSet :  Set hardware date and time
	def HardwareDateAndTimeSet (self, socketId, DateAndTime):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'HardwareDateAndTimeSet(' + DateAndTime + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# EventAdd :  ** OBSOLETE ** Add an event
	def EventAdd (self, socketId, PositionerName, EventName, EventParameter, ActionName, ActionParameter1, ActionParameter2, ActionParameter3):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'EventAdd(' + PositionerName + ',' + EventName + ',' + EventParameter + ',' + ActionName + ',' + ActionParameter1 + ',' + ActionParameter2 + ',' + ActionParameter3 + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# EventGet :  ** OBSOLETE ** Read events and actions list
	def EventGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'EventGet(' + PositionerName + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# EventRemove :  ** OBSOLETE ** Delete an event
	def EventRemove (self, socketId, PositionerName, EventName, EventParameter):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'EventRemove(' + PositionerName + ',' + EventName + ',' + EventParameter + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# EventWait :  ** OBSOLETE ** Wait an event
	def EventWait (self, socketId, PositionerName, EventName, EventParameter):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'EventWait(' + PositionerName + ',' + EventName + ',' + EventParameter + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# EventExtendedConfigurationTriggerSet :  Configure one or several events
	def EventExtendedConfigurationTriggerSet (self, socketId, ExtendedEventName, EventParameter1, EventParameter2, EventParameter3, EventParameter4):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'EventExtendedConfigurationTriggerSet('
		for i in range(len(ExtendedEventName)):
			if (i > 0):
				command += ','
			command += ExtendedEventName[i] + ',' + EventParameter1[i] + ',' + EventParameter2[i] + ',' + EventParameter3[i] + ',' + EventParameter4[i]
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# EventExtendedConfigurationTriggerGet :  Read the event configuration
	def EventExtendedConfigurationTriggerGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'EventExtendedConfigurationTriggerGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# EventExtendedConfigurationActionSet :  Configure one or several actions
	def EventExtendedConfigurationActionSet (self, socketId, ExtendedActionName, ActionParameter1, ActionParameter2, ActionParameter3, ActionParameter4):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'EventExtendedConfigurationActionSet('
		for i in range(len(ExtendedActionName)):
			if (i > 0):
				command += ','
			command += ExtendedActionName[i] + ',' + ActionParameter1[i] + ',' + ActionParameter2[i] + ',' + ActionParameter3[i] + ',' + ActionParameter4[i]
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# EventExtendedConfigurationActionGet :  Read the action configuration
	def EventExtendedConfigurationActionGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'EventExtendedConfigurationActionGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# EventExtendedStart :  Launch the last event and action configuration and return an ID
	def EventExtendedStart (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'EventExtendedStart(int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# EventExtendedAllGet :  Read all event and action configurations
	def EventExtendedAllGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'EventExtendedAllGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# EventExtendedGet :  Read the event and action configuration defined by ID
	def EventExtendedGet (self, socketId, ID):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'EventExtendedGet(' + str(ID) + ',char *,char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# EventExtendedRemove :  Remove the event and action configuration defined by ID
	def EventExtendedRemove (self, socketId, ID):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'EventExtendedRemove(' + str(ID) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# EventExtendedWait :  Wait events from the last event configuration
	def EventExtendedWait (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'EventExtendedWait()'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# GatheringConfigurationGet : Read different mnemonique type
	def GatheringConfigurationGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'GatheringConfigurationGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# GatheringConfigurationSet :  Configuration acquisition
	def GatheringConfigurationSet (self, socketId, Type):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GatheringConfigurationSet('
		for i in range(len(Type)):
			if (i > 0):
				command += ','
			command += Type[i]
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GatheringCurrentNumberGet :  Maximum number of samples and current number during acquisition
	def GatheringCurrentNumberGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'GatheringCurrentNumberGet(int *,int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GatheringStopAndSave :  Stop acquisition and save data
	def GatheringStopAndSave (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'GatheringStopAndSave()'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# GatheringDataAcquire :  Acquire a configured data
	def GatheringDataAcquire (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'GatheringDataAcquire()'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# GatheringDataGet :  Get a data line from gathering buffer
	def GatheringDataGet (self, socketId, IndexPoint):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GatheringDataGet(' + str(IndexPoint) + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GatheringDataMultipleLinesGet :  Get multiple data lines from gathering buffer
	def GatheringDataMultipleLinesGet (self, socketId, IndexPoint, NumberOfLines):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GatheringDataMultipleLinesGet(' + str(IndexPoint) + ',' + str(NumberOfLines) + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GatheringReset :  Empty the gathered data in memory to start new gathering from scratch
	def GatheringReset (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'GatheringReset()'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# GatheringRun :  Start a new gathering
	def GatheringRun (self, socketId, DataNumber, Divisor):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GatheringRun(' + str(DataNumber) + ',' + str(Divisor) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GatheringRunAppend :  Re-start the stopped gathering to add new data
	def GatheringRunAppend (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'GatheringRunAppend()'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# GatheringStop :  Stop the data gathering (without saving to file)
	def GatheringStop (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'GatheringStop()'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# GatheringExternalConfigurationSet :  Configuration acquisition
	def GatheringExternalConfigurationSet (self, socketId, Type):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GatheringExternalConfigurationSet('
		for i in range(len(Type)):
			if (i > 0):
				command += ','
			command += Type[i]
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GatheringExternalConfigurationGet :  Read different mnemonique type
	def GatheringExternalConfigurationGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'GatheringExternalConfigurationGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# GatheringExternalCurrentNumberGet :  Maximum number of samples and current number during acquisition
	def GatheringExternalCurrentNumberGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'GatheringExternalCurrentNumberGet(int *,int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GatheringExternalDataGet :  Get a data line from external gathering buffer
	def GatheringExternalDataGet (self, socketId, IndexPoint):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GatheringExternalDataGet(' + str(IndexPoint) + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GatheringExternalStopAndSave :  Stop acquisition and save data
	def GatheringExternalStopAndSave (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'GatheringExternalStopAndSave()'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# GlobalArrayGet :  Get global array value
	def GlobalArrayGet (self, socketId, Number):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GlobalArrayGet(' + str(Number) + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GlobalArraySet :  Set global array value
	def GlobalArraySet (self, socketId, Number, ValueString):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GlobalArraySet(' + str(Number) + ',' + ValueString + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# DoubleGlobalArrayGet :  Get double global array value
	def DoubleGlobalArrayGet (self, socketId, Number):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'DoubleGlobalArrayGet(' + str(Number) + ',double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# DoubleGlobalArraySet :  Set double global array value
	def DoubleGlobalArraySet (self, socketId, Number, DoubleValue):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'DoubleGlobalArraySet(' + str(Number) + ',' + str(DoubleValue) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GPIOAnalogGet :  Read analog input or analog output for one or few input
	def GPIOAnalogGet (self, socketId, GPIOName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GPIOAnalogGet('
		for i in range(len(GPIOName)):
			if (i > 0):
				command += ','
			command += GPIOName[i] + ',' + 'double *'
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(len(GPIOName)):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GPIOAnalogSet :  Set analog output for one or few output
	def GPIOAnalogSet (self, socketId, GPIOName, AnalogOutputValue):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GPIOAnalogSet('
		for i in range(len(GPIOName)):
			if (i > 0):
				command += ','
			command += GPIOName[i] + ',' + str(AnalogOutputValue[i])
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GPIOAnalogGainGet :  Read analog input gain (1, 2, 4 or 8) for one or few input
	def GPIOAnalogGainGet (self, socketId, GPIOName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GPIOAnalogGainGet('
		for i in range(len(GPIOName)):
			if (i > 0):
				command += ','
			command += GPIOName[i] + ',' + 'int *'
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(len(GPIOName)):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GPIOAnalogGainSet :  Set analog input gain (1, 2, 4 or 8) for one or few input
	def GPIOAnalogGainSet (self, socketId, GPIOName, AnalogInputGainValue):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GPIOAnalogGainSet('
		for i in range(len(GPIOName)):
			if (i > 0):
				command += ','
			command += GPIOName[i] + ',' + str(AnalogInputGainValue[i])
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GPIODigitalGet :  Read digital output or digital input
	def GPIODigitalGet (self, socketId, GPIOName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GPIODigitalGet(' + GPIOName + ',unsigned short *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# GPIODigitalSet :  Set Digital Output for one or few output TTL
	def GPIODigitalSet (self, socketId, GPIOName, Mask, DigitalOutputValue):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GPIODigitalSet(' + GPIOName + ',' + str(Mask) + ',' + str(DigitalOutputValue) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupAccelerationSetpointGet :  Return setpoint accelerations
	def GroupAccelerationSetpointGet (self, socketId, GroupName, nbElement):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupAccelerationSetpointGet(' + GroupName + ','
		for i in range(nbElement):
			if (i > 0):
				command += ','
			command += 'double *'
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(nbElement):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GroupAnalogTrackingModeEnable :  Enable Analog Tracking mode on selected group
	def GroupAnalogTrackingModeEnable (self, socketId, GroupName, Type):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupAnalogTrackingModeEnable(' + GroupName + ',' + Type + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupAnalogTrackingModeDisable :  Disable Analog Tracking mode on selected group
	def GroupAnalogTrackingModeDisable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupAnalogTrackingModeDisable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupCorrectorOutputGet :  Return corrector outputs
	def GroupCorrectorOutputGet (self, socketId, GroupName, nbElement):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupCorrectorOutputGet(' + GroupName + ','
		for i in range(nbElement):
			if (i > 0):
				command += ','
			command += 'double *'
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(nbElement):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GroupCurrentFollowingErrorGet :  Return current following errors
	def GroupCurrentFollowingErrorGet (self, socketId, GroupName, nbElement):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupCurrentFollowingErrorGet(' + GroupName + ','
		for i in range(nbElement):
			if (i > 0):
				command += ','
			command += 'double *'
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(nbElement):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GroupHomeSearch :  Start home search sequence
	def GroupHomeSearch (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupHomeSearch(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupHomeSearchAndRelativeMove :  Start home search sequence and execute a displacement
	def GroupHomeSearchAndRelativeMove (self, socketId, GroupName, TargetDisplacement):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupHomeSearchAndRelativeMove(' + GroupName + ','
		for i in range(len(TargetDisplacement)):
			if (i > 0):
				command += ','
			command += str(TargetDisplacement[i])
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupInitialize :  Start the initialization
	def GroupInitialize (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupInitialize(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupInitializeNoEncoderReset :  Start the initialization with no encoder reset
	def GroupInitializeNoEncoderReset (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupInitializeNoEncoderReset(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupInitializeWithEncoderCalibration :  Start the initialization with encoder calibration
	def GroupInitializeWithEncoderCalibration (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupInitializeWithEncoderCalibration(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupInterlockDisable :  Set group interlock disable
	def GroupInterlockDisable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupInterlockDisable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupInterlockEnable :  Set group interlock enable
	def GroupInterlockEnable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupInterlockEnable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupJogParametersSet :  Modify Jog parameters on selected group and activate the continuous move
	def GroupJogParametersSet (self, socketId, GroupName, Velocity, Acceleration):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupJogParametersSet(' + GroupName + ','
		for i in range(len(Velocity)):
			if (i > 0):
				command += ','
			command += str(Velocity[i]) + ',' + str(Acceleration[i])
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupJogParametersGet :  Get Jog parameters on selected group
	def GroupJogParametersGet (self, socketId, GroupName, nbElement):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupJogParametersGet(' + GroupName + ','
		for i in range(nbElement):
			if (i > 0):
				command += ','
			command += 'double *' + ',' + 'double *'
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(nbElement*2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GroupJogCurrentGet :  Get Jog current on selected group
	def GroupJogCurrentGet (self, socketId, GroupName, nbElement):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupJogCurrentGet(' + GroupName + ','
		for i in range(nbElement):
			if (i > 0):
				command += ','
			command += 'double *' + ',' + 'double *'
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(nbElement*2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GroupJogModeEnable :  Enable Jog mode on selected group
	def GroupJogModeEnable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupJogModeEnable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupJogModeDisable :  Disable Jog mode on selected group
	def GroupJogModeDisable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupJogModeDisable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupKill :  Kill the group
	def GroupKill (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupKill(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupMotionDisable :  Set Motion disable on selected group
	def GroupMotionDisable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupMotionDisable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupMotionEnable :  Set Motion enable on selected group
	def GroupMotionEnable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupMotionEnable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupMotionStatusGet :  Return group or positioner status
	def GroupMotionStatusGet (self, socketId, GroupName, nbElement):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupMotionStatusGet(' + GroupName + ','
		for i in range(nbElement):
			if (i > 0):
				command += ','
			command += 'int *'
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(nbElement):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GroupMoveAbort :  Abort a move
	def GroupMoveAbort (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupMoveAbort(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupMoveAbortFast :  Abort quickly a move
	def GroupMoveAbortFast (self, socketId, GroupName, AccelerationMultiplier):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupMoveAbortFast(' + GroupName + ',' + str(AccelerationMultiplier) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupMoveAbsolute :  Do an absolute move
	def GroupMoveAbsolute (self, socketId, GroupName, TargetPosition):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupMoveAbsolute(' + GroupName + ','
		for i in range(len(TargetPosition)):
			if (i > 0):
				command += ','
			command += str(TargetPosition[i])
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupMoveRelative :  Do a relative move
	def GroupMoveRelative (self, socketId, GroupName, TargetDisplacement):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupMoveRelative(' + GroupName + ','
		for i in range(len(TargetDisplacement)):
			if (i > 0):
				command += ','
			command += str(TargetDisplacement[i])
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupPositionCorrectedProfilerGet :  Return corrected profiler positions
	def GroupPositionCorrectedProfilerGet (self, socketId, GroupName, PositionX, PositionY):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupPositionCorrectedProfilerGet(' + GroupName + ',' + str(PositionX) + ',' + str(PositionY) + ',double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GroupPositionCurrentGet :  Return current positions
	def GroupPositionCurrentGet (self, socketId, GroupName, nbElement):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupPositionCurrentGet(' + GroupName + ','
		for i in range(nbElement):
			if (i > 0):
				command += ','
			command += 'double *'
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(nbElement):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GroupPositionPCORawEncoderGet :  Return PCO raw encoder positions
	def GroupPositionPCORawEncoderGet (self, socketId, GroupName, PositionX, PositionY):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupPositionPCORawEncoderGet(' + GroupName + ',' + str(PositionX) + ',' + str(PositionY) + ',double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GroupPositionSetpointGet :  Return setpoint positions
	def GroupPositionSetpointGet (self, socketId, GroupName, nbElement):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupPositionSetpointGet(' + GroupName + ','
		for i in range(nbElement):
			if (i > 0):
				command += ','
			command += 'double *'
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(nbElement):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GroupPositionTargetGet :  Return target positions
	def GroupPositionTargetGet (self, socketId, GroupName, nbElement):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupPositionTargetGet(' + GroupName + ','
		for i in range(nbElement):
			if (i > 0):
				command += ','
			command += 'double *'
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(nbElement):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GroupReferencingActionExecute :  Execute an action in referencing mode
	def GroupReferencingActionExecute (self, socketId, PositionerName, ReferencingAction, ReferencingSensor, ReferencingParameter):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupReferencingActionExecute(' + PositionerName + ',' + ReferencingAction + ',' + ReferencingSensor + ',' + str(ReferencingParameter) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupReferencingStart :  Enter referencing mode
	def GroupReferencingStart (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupReferencingStart(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupReferencingStop :  Exit referencing mode
	def GroupReferencingStop (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupReferencingStop(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupStatusGet :  Return group status
	def GroupStatusGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupStatusGet(' + GroupName + ',int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# GroupStatusStringGet :  Return the group status string corresponding to the group status code
	def GroupStatusStringGet (self, socketId, GroupStatusCode):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupStatusStringGet(' + str(GroupStatusCode) + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupVelocityCurrentGet :  Return current velocities
	def GroupVelocityCurrentGet (self, socketId, GroupName, nbElement):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupVelocityCurrentGet(' + GroupName + ','
		for i in range(nbElement):
			if (i > 0):
				command += ','
			command += 'double *'
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(nbElement):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# KillAll :  Put all groups in 'Not initialized' state
	def KillAll (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'KillAll()'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# RestartApplication :  Restart the Controller
	def RestartApplication (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'RestartApplication()'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# PositionerAnalogTrackingPositionParametersGet :  Read dynamic parameters for one axe of a group for a future analog tracking position
	def PositionerAnalogTrackingPositionParametersGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerAnalogTrackingPositionParametersGet(' + PositionerName + ',char *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerAnalogTrackingPositionParametersSet :  Update dynamic parameters for one axe of a group for a future analog tracking position
	def PositionerAnalogTrackingPositionParametersSet (self, socketId, PositionerName, GPIOName, Offset, Scale, Velocity, Acceleration):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerAnalogTrackingPositionParametersSet(' + PositionerName + ',' + GPIOName + ',' + str(Offset) + ',' + str(Scale) + ',' + str(Velocity) + ',' + str(Acceleration) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerAnalogTrackingVelocityParametersGet :  Read dynamic parameters for one axe of a group for a future analog tracking velocity
	def PositionerAnalogTrackingVelocityParametersGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerAnalogTrackingVelocityParametersGet(' + PositionerName + ',char *,double *,double *,double *,int *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(6):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerAnalogTrackingVelocityParametersSet :  Update dynamic parameters for one axe of a group for a future analog tracking velocity
	def PositionerAnalogTrackingVelocityParametersSet (self, socketId, PositionerName, GPIOName, Offset, Scale, DeadBandThreshold, Order, Velocity, Acceleration):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerAnalogTrackingVelocityParametersSet(' + PositionerName + ',' + GPIOName + ',' + str(Offset) + ',' + str(Scale) + ',' + str(DeadBandThreshold) + ',' + str(Order) + ',' + str(Velocity) + ',' + str(Acceleration) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerBacklashGet :  Read backlash value and status
	def PositionerBacklashGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerBacklashGet(' + PositionerName + ',double *,char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerBacklashSet :  Set backlash value
	def PositionerBacklashSet (self, socketId, PositionerName, BacklashValue):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerBacklashSet(' + PositionerName + ',' + str(BacklashValue) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerBacklashEnable :  Enable the backlash
	def PositionerBacklashEnable (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerBacklashEnable(' + PositionerName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerBacklashDisable :  Disable the backlash
	def PositionerBacklashDisable (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerBacklashDisable(' + PositionerName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCompensatedPCOAbort :  Abort CIE08 compensated PCO mode
	def PositionerCompensatedPCOAbort (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensatedPCOAbort(' + PositionerName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCompensatedPCOCurrentStatusGet :  Get current status of CIE08 compensated PCO mode
	def PositionerCompensatedPCOCurrentStatusGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensatedPCOCurrentStatusGet(' + PositionerName + ',int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# PositionerCompensatedPCOEnable :  Enable CIE08 compensated PCO mode execution
	def PositionerCompensatedPCOEnable (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensatedPCOEnable(' + PositionerName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCompensatedPCOFromFile :  Load file to CIE08 compensated PCO data buffer
	def PositionerCompensatedPCOFromFile (self, socketId, PositionerName, DataFileName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensatedPCOFromFile(' + PositionerName + ',' + DataFileName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCompensatedPCOLoadToMemory :  Load data lines to CIE08 compensated PCO data buffer
	def PositionerCompensatedPCOLoadToMemory (self, socketId, PositionerName, DataLines):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensatedPCOLoadToMemory(' + PositionerName + ',' + DataLines + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCompensatedPCOMemoryReset :  Reset CIE08 compensated PCO data buffer
	def PositionerCompensatedPCOMemoryReset (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensatedPCOMemoryReset(' + PositionerName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCompensatedPCOPrepare :  Prepare data for CIE08 compensated PCO mode
	def PositionerCompensatedPCOPrepare (self, socketId, PositionerName, ScanDirection, StartPosition):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensatedPCOPrepare(' + PositionerName + ',' + ScanDirection + ','
		for i in range(len(StartPosition)):
			if (i > 0):
				command += ','
			command += str(StartPosition[i])
		command += ')'

		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCompensatedPCOSet :  Set data to CIE08 compensated PCO data buffer
	def PositionerCompensatedPCOSet (self, socketId, PositionerName, Start, Stop, Distance, Width):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensatedPCOSet(' + PositionerName + ',' + str(Start) + ',' + str(Stop) + ',' + str(Distance) + ',' + str(Width) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCompensationFrequencyNotchsGet :  Read frequency compensation notch filters parameters
	def PositionerCompensationFrequencyNotchsGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensationFrequencyNotchsGet(' + PositionerName + ',double *,double *,double *,double *,double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(9):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerCompensationFrequencyNotchsSet :  Update frequency compensation notch filters parameters
	def PositionerCompensationFrequencyNotchsSet (self, socketId, PositionerName, NotchFrequency1, NotchBandwidth1, NotchGain1, NotchFrequency2, NotchBandwidth2, NotchGain2, NotchFrequency3, NotchBandwidth3, NotchGain3):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensationFrequencyNotchsSet(' + PositionerName + ',' + str(NotchFrequency1) + ',' + str(NotchBandwidth1) + ',' + str(NotchGain1) + ',' + str(NotchFrequency2) + ',' + str(NotchBandwidth2) + ',' + str(NotchGain2) + ',' + str(NotchFrequency3) + ',' + str(NotchBandwidth3) + ',' + str(NotchGain3) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCompensationLowPassTwoFilterGet :  Read second order low-pass filter parameters
	def PositionerCompensationLowPassTwoFilterGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensationLowPassTwoFilterGet(' + PositionerName + ',double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# PositionerCompensationLowPassTwoFilterSet :  Update second order low-pass filter parameters
	def PositionerCompensationLowPassTwoFilterSet (self, socketId, PositionerName, CutOffFrequency):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensationLowPassTwoFilterSet(' + PositionerName + ',' + str(CutOffFrequency) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCompensationNotchModeFiltersGet :  Read notch mode filters parameters
	def PositionerCompensationNotchModeFiltersGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensationNotchModeFiltersGet(' + PositionerName + ',double *,double *,double *,double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(8):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerCompensationNotchModeFiltersSet :  Update notch mode filters parameters
	def PositionerCompensationNotchModeFiltersSet (self, socketId, PositionerName, NotchModeFr1, NotchModeFa1, NotchModeZr1, NotchModeZa1, NotchModeFr2, NotchModeFa2, NotchModeZr2, NotchModeZa2):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensationNotchModeFiltersSet(' + PositionerName + ',' + str(NotchModeFr1) + ',' + str(NotchModeFa1) + ',' + str(NotchModeZr1) + ',' + str(NotchModeZa1) + ',' + str(NotchModeFr2) + ',' + str(NotchModeFa2) + ',' + str(NotchModeZr2) + ',' + str(NotchModeZa2) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCompensationPhaseCorrectionFiltersGet :  Read phase correction filters parameters
	def PositionerCompensationPhaseCorrectionFiltersGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensationPhaseCorrectionFiltersGet(' + PositionerName + ',double *,double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(6):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerCompensationPhaseCorrectionFiltersSet :  Update phase correction filters parameters
	def PositionerCompensationPhaseCorrectionFiltersSet (self, socketId, PositionerName, PhaseCorrectionFn1, PhaseCorrectionFd1, PhaseCorrectionGain1, PhaseCorrectionFn2, PhaseCorrectionFd2, PhaseCorrectionGain2):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensationPhaseCorrectionFiltersSet(' + PositionerName + ',' + str(PhaseCorrectionFn1) + ',' + str(PhaseCorrectionFd1) + ',' + str(PhaseCorrectionGain1) + ',' + str(PhaseCorrectionFn2) + ',' + str(PhaseCorrectionFd2) + ',' + str(PhaseCorrectionGain2) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCompensationSpatialPeriodicNotchsGet :  Read spatial compensation notch filters parameters
	def PositionerCompensationSpatialPeriodicNotchsGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensationSpatialPeriodicNotchsGet(' + PositionerName + ',double *,double *,double *,double *,double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(9):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerCompensationSpatialPeriodicNotchsSet :  Update spatial compensation notch filters parameters
	def PositionerCompensationSpatialPeriodicNotchsSet (self, socketId, PositionerName, SpatialNotchStep1, SpatialNotchBandwidth1, SpatialNotchGain1, SpatialNotchStep2, SpatialNotchBandwidth2, SpatialNotchGain2, SpatialNotchStep3, SpatialNotchBandwidth3, SpatialNotchGain3):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCompensationSpatialPeriodicNotchsSet(' + PositionerName + ',' + str(SpatialNotchStep1) + ',' + str(SpatialNotchBandwidth1) + ',' + str(SpatialNotchGain1) + ',' + str(SpatialNotchStep2) + ',' + str(SpatialNotchBandwidth2) + ',' + str(SpatialNotchGain2) + ',' + str(SpatialNotchStep3) + ',' + str(SpatialNotchBandwidth3) + ',' + str(SpatialNotchGain3) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCorrectorNotchFiltersSet :  Update filters parameters
	def PositionerCorrectorNotchFiltersSet (self, socketId, PositionerName, NotchFrequency1, NotchBandwidth1, NotchGain1, NotchFrequency2, NotchBandwidth2, NotchGain2):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorNotchFiltersSet(' + PositionerName + ',' + str(NotchFrequency1) + ',' + str(NotchBandwidth1) + ',' + str(NotchGain1) + ',' + str(NotchFrequency2) + ',' + str(NotchBandwidth2) + ',' + str(NotchGain2) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCorrectorNotchFiltersGet :  Read filters parameters
	def PositionerCorrectorNotchFiltersGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorNotchFiltersGet(' + PositionerName + ',double *,double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(6):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerCorrectorPIDBaseSet :  Update PIDBase parameters
	def PositionerCorrectorPIDBaseSet (self, socketId, PositionerName, MovingMass, StaticMass, Viscosity, Stiffness):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorPIDBaseSet(' + PositionerName + ',' + str(MovingMass) + ',' + str(StaticMass) + ',' + str(Viscosity) + ',' + str(Stiffness) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCorrectorPIDBaseGet :  Read PIDBase parameters
	def PositionerCorrectorPIDBaseGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorPIDBaseGet(' + PositionerName + ',double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerCorrectorPIDFFAccelerationSet :  Update corrector parameters
	def PositionerCorrectorPIDFFAccelerationSet (self, socketId, PositionerName, ClosedLoopStatus, KP, KI, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardAcceleration, KFeedForwardJerk):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorPIDFFAccelerationSet(' + PositionerName + ',' + str(ClosedLoopStatus) + ',' + str(KP) + ',' + str(KI) + ',' + str(KD) + ',' + str(KS) + ',' + str(IntegrationTime) + ',' + str(DerivativeFilterCutOffFrequency) + ',' + str(GKP) + ',' + str(GKI) + ',' + str(GKD) + ',' + str(KForm) + ',' + str(KFeedForwardAcceleration) + ',' + str(KFeedForwardJerk) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCorrectorPIDFFAccelerationGet :  Read corrector parameters
	def PositionerCorrectorPIDFFAccelerationGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorPIDFFAccelerationGet(' + PositionerName + ',bool *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(13):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerCorrectorP2IDFFAccelerationSet :  Update corrector parameters
	def PositionerCorrectorP2IDFFAccelerationSet (self, socketId, PositionerName, ClosedLoopStatus, KP, KI, KI2, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardAcceleration, KFeedForwardJerk, SetpointPositionDelay):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorP2IDFFAccelerationSet(' + PositionerName + ',' + str(ClosedLoopStatus) + ',' + str(KP) + ',' + str(KI) + ',' + str(KI2) + ',' + str(KD) + ',' + str(KS) + ',' + str(IntegrationTime) + ',' + str(DerivativeFilterCutOffFrequency) + ',' + str(GKP) + ',' + str(GKI) + ',' + str(GKD) + ',' + str(KForm) + ',' + str(KFeedForwardAcceleration) + ',' + str(KFeedForwardJerk) + ',' + str(SetpointPositionDelay) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCorrectorP2IDFFAccelerationGet :  Read corrector parameters
	def PositionerCorrectorP2IDFFAccelerationGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorP2IDFFAccelerationGet(' + PositionerName + ',bool *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(15):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerCorrectorPIDFFVelocitySet :  Update corrector parameters
	def PositionerCorrectorPIDFFVelocitySet (self, socketId, PositionerName, ClosedLoopStatus, KP, KI, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardVelocity):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorPIDFFVelocitySet(' + PositionerName + ',' + str(ClosedLoopStatus) + ',' + str(KP) + ',' + str(KI) + ',' + str(KD) + ',' + str(KS) + ',' + str(IntegrationTime) + ',' + str(DerivativeFilterCutOffFrequency) + ',' + str(GKP) + ',' + str(GKI) + ',' + str(GKD) + ',' + str(KForm) + ',' + str(KFeedForwardVelocity) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCorrectorPIDFFVelocityGet :  Read corrector parameters
	def PositionerCorrectorPIDFFVelocityGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorPIDFFVelocityGet(' + PositionerName + ',bool *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(12):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerCorrectorPIDDualFFVoltageSet :  Update corrector parameters
	def PositionerCorrectorPIDDualFFVoltageSet (self, socketId, PositionerName, ClosedLoopStatus, KP, KI, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, KFeedForwardVelocity, KFeedForwardAcceleration, Friction):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorPIDDualFFVoltageSet(' + PositionerName + ',' + str(ClosedLoopStatus) + ',' + str(KP) + ',' + str(KI) + ',' + str(KD) + ',' + str(KS) + ',' + str(IntegrationTime) + ',' + str(DerivativeFilterCutOffFrequency) + ',' + str(GKP) + ',' + str(GKI) + ',' + str(GKD) + ',' + str(KForm) + ',' + str(KFeedForwardVelocity) + ',' + str(KFeedForwardAcceleration) + ',' + str(Friction) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCorrectorPIDDualFFVoltageGet :  Read corrector parameters
	def PositionerCorrectorPIDDualFFVoltageGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorPIDDualFFVoltageGet(' + PositionerName + ',bool *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(14):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerCorrectorPIPositionSet :  Update corrector parameters
	def PositionerCorrectorPIPositionSet (self, socketId, PositionerName, ClosedLoopStatus, KP, KI, IntegrationTime):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorPIPositionSet(' + PositionerName + ',' + str(ClosedLoopStatus) + ',' + str(KP) + ',' + str(KI) + ',' + str(IntegrationTime) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCorrectorPIPositionGet :  Read corrector parameters
	def PositionerCorrectorPIPositionGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorPIPositionGet(' + PositionerName + ',bool *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerCorrectorSR1AccelerationSet :  Update corrector parameters
	def PositionerCorrectorSR1AccelerationSet (self, socketId, PositionerName, ClosedLoopStatus, KP, KI, KV, ObserverFrequency, CompensationGainVelocity, CompensationGainAcceleration, CompensationGainJerk):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorSR1AccelerationSet(' + PositionerName + ',' + str(ClosedLoopStatus) + ',' + str(KP) + ',' + str(KI) + ',' + str(KV) + ',' + str(ObserverFrequency) + ',' + str(CompensationGainVelocity) + ',' + str(CompensationGainAcceleration) + ',' + str(CompensationGainJerk) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCorrectorSR1AccelerationGet :  Read corrector parameters
	def PositionerCorrectorSR1AccelerationGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorSR1AccelerationGet(' + PositionerName + ',bool *,double *,double *,double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(8):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerCorrectorSR1ObserverAccelerationSet :  Update SR1 corrector observer parameters
	def PositionerCorrectorSR1ObserverAccelerationSet (self, socketId, PositionerName, ParameterA, ParameterB, ParameterC):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorSR1ObserverAccelerationSet(' + PositionerName + ',' + str(ParameterA) + ',' + str(ParameterB) + ',' + str(ParameterC) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCorrectorSR1ObserverAccelerationGet :  Read SR1 corrector observer parameters
	def PositionerCorrectorSR1ObserverAccelerationGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorSR1ObserverAccelerationGet(' + PositionerName + ',double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(3):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerCorrectorSR1OffsetAccelerationSet :  Update SR1 corrector output acceleration offset
	def PositionerCorrectorSR1OffsetAccelerationSet (self, socketId, PositionerName, AccelerationOffset):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorSR1OffsetAccelerationSet(' + PositionerName + ',' + str(AccelerationOffset) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCorrectorSR1OffsetAccelerationGet :  Read SR1 corrector output acceleration offset
	def PositionerCorrectorSR1OffsetAccelerationGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorSR1OffsetAccelerationGet(' + PositionerName + ',double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# PositionerCorrectorTypeGet :  Read corrector type
	def PositionerCorrectorTypeGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorTypeGet(' + PositionerName + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCurrentVelocityAccelerationFiltersSet :  Set current velocity and acceleration cut off frequencies
	def PositionerCurrentVelocityAccelerationFiltersSet (self, socketId, PositionerName, CurrentVelocityCutOffFrequency, CurrentAccelerationCutOffFrequency):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCurrentVelocityAccelerationFiltersSet(' + PositionerName + ',' + str(CurrentVelocityCutOffFrequency) + ',' + str(CurrentAccelerationCutOffFrequency) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerCurrentVelocityAccelerationFiltersGet :  Get current velocity and acceleration cut off frequencies
	def PositionerCurrentVelocityAccelerationFiltersGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCurrentVelocityAccelerationFiltersGet(' + PositionerName + ',double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerDriverFiltersGet :  Get driver filters parameters
	def PositionerDriverFiltersGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerDriverFiltersGet(' + PositionerName + ',double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(5):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerDriverFiltersSet :  Set driver filters parameters
	def PositionerDriverFiltersSet (self, socketId, PositionerName, KI, NotchFrequency, NotchBandwidth, NotchGain, LowpassFrequency):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerDriverFiltersSet(' + PositionerName + ',' + str(KI) + ',' + str(NotchFrequency) + ',' + str(NotchBandwidth) + ',' + str(NotchGain) + ',' + str(LowpassFrequency) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerDriverPositionOffsetsGet :  Get driver stage and gage position offset
	def PositionerDriverPositionOffsetsGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerDriverPositionOffsetsGet(' + PositionerName + ',double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerDriverStatusGet :  Read positioner driver status
	def PositionerDriverStatusGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerDriverStatusGet(' + PositionerName + ',int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# PositionerDriverStatusStringGet :  Return the positioner driver status string corresponding to the positioner error code
	def PositionerDriverStatusStringGet (self, socketId, PositionerDriverStatus):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerDriverStatusStringGet(' + str(PositionerDriverStatus) + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerEncoderAmplitudeValuesGet :  Read analog interpolated encoder amplitude values
	def PositionerEncoderAmplitudeValuesGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerEncoderAmplitudeValuesGet(' + PositionerName + ',double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerEncoderCalibrationParametersGet :  Read analog interpolated encoder calibration parameters
	def PositionerEncoderCalibrationParametersGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerEncoderCalibrationParametersGet(' + PositionerName + ',double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerErrorGet :  Read and clear positioner error code
	def PositionerErrorGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerErrorGet(' + PositionerName + ',int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# PositionerErrorRead :  Read only positioner error code without clear it
	def PositionerErrorRead (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerErrorRead(' + PositionerName + ',int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# PositionerErrorStringGet :  Return the positioner status string corresponding to the positioner error code
	def PositionerErrorStringGet (self, socketId, PositionerErrorCode):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerErrorStringGet(' + str(PositionerErrorCode) + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerExcitationSignalGet :  Get excitation signal mode
	def PositionerExcitationSignalGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerExcitationSignalGet(' + PositionerName + ',int *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerExcitationSignalSet :  Set excitation signal mode
	def PositionerExcitationSignalSet (self, socketId, PositionerName, Mode, Frequency, Amplitude, Time):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerExcitationSignalSet(' + PositionerName + ',' + str(Mode) + ',' + str(Frequency) + ',' + str(Amplitude) + ',' + str(Time) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerHardwareStatusGet :  Read positioner hardware status
	def PositionerHardwareStatusGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerHardwareStatusGet(' + PositionerName + ',int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# PositionerHardwareStatusStringGet :  Return the positioner hardware status string corresponding to the positioner error code
	def PositionerHardwareStatusStringGet (self, socketId, PositionerHardwareStatus):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerHardwareStatusStringGet(' + str(PositionerHardwareStatus) + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerHardInterpolatorFactorGet :  Get hard interpolator parameters
	def PositionerHardInterpolatorFactorGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerHardInterpolatorFactorGet(' + PositionerName + ',int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# PositionerHardInterpolatorFactorSet :  Set hard interpolator parameters
	def PositionerHardInterpolatorFactorSet (self, socketId, PositionerName, InterpolationFactor):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerHardInterpolatorFactorSet(' + PositionerName + ',' + str(InterpolationFactor) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerHardInterpolatorPositionGet :  Read external latch position
	def PositionerHardInterpolatorPositionGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerHardInterpolatorPositionGet(' + PositionerName + ',double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# PositionerMaximumVelocityAndAccelerationGet :  Return maximum velocity and acceleration of the positioner
	def PositionerMaximumVelocityAndAccelerationGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerMaximumVelocityAndAccelerationGet(' + PositionerName + ',double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerMotionDoneGet :  Read motion done parameters
	def PositionerMotionDoneGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerMotionDoneGet(' + PositionerName + ',double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(5):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerMotionDoneSet :  Update motion done parameters
	def PositionerMotionDoneSet (self, socketId, PositionerName, PositionWindow, VelocityWindow, CheckingTime, MeanPeriod, TimeOut):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerMotionDoneSet(' + PositionerName + ',' + str(PositionWindow) + ',' + str(VelocityWindow) + ',' + str(CheckingTime) + ',' + str(MeanPeriod) + ',' + str(TimeOut) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerPositionCompareAquadBAlwaysEnable :  Enable AquadB signal in always mode
	def PositionerPositionCompareAquadBAlwaysEnable (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerPositionCompareAquadBAlwaysEnable(' + PositionerName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerPositionCompareAquadBWindowedGet :  Read position compare AquadB windowed parameters
	def PositionerPositionCompareAquadBWindowedGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerPositionCompareAquadBWindowedGet(' + PositionerName + ',double *,double *,bool *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(3):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerPositionCompareAquadBWindowedSet :  Set position compare AquadB windowed parameters
	def PositionerPositionCompareAquadBWindowedSet (self, socketId, PositionerName, MinimumPosition, MaximumPosition):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerPositionCompareAquadBWindowedSet(' + PositionerName + ',' + str(MinimumPosition) + ',' + str(MaximumPosition) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerPositionCompareGet :  Read position compare parameters
	def PositionerPositionCompareGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerPositionCompareGet(' + PositionerName + ',double *,double *,double *,bool *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerPositionCompareSet :  Set position compare parameters
	def PositionerPositionCompareSet (self, socketId, PositionerName, MinimumPosition, MaximumPosition, PositionStep):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerPositionCompareSet(' + PositionerName + ',' + str(MinimumPosition) + ',' + str(MaximumPosition) + ',' + str(PositionStep) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerPositionCompareEnable :  Enable position compare
	def PositionerPositionCompareEnable (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerPositionCompareEnable(' + PositionerName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerPositionCompareDisable :  Disable position compare
	def PositionerPositionCompareDisable (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerPositionCompareDisable(' + PositionerName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerPositionComparePulseParametersGet :  Get position compare PCO pulse parameters
	def PositionerPositionComparePulseParametersGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerPositionComparePulseParametersGet(' + PositionerName + ',double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerPositionComparePulseParametersSet :  Set position compare PCO pulse parameters
	def PositionerPositionComparePulseParametersSet (self, socketId, PositionerName, PCOPulseWidth, EncoderSettlingTime):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerPositionComparePulseParametersSet(' + PositionerName + ',' + str(PCOPulseWidth) + ',' + str(EncoderSettlingTime) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerPositionCompareScanAccelerationLimitGet :  Get position compare scan acceleration limit
	def PositionerPositionCompareScanAccelerationLimitGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerPositionCompareScanAccelerationLimitGet(' + PositionerName + ',double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# PositionerPositionCompareScanAccelerationLimitSet :  Set position compare scan acceleration limit
	def PositionerPositionCompareScanAccelerationLimitSet (self, socketId, PositionerName, ScanAccelerationLimit):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerPositionCompareScanAccelerationLimitSet(' + PositionerName + ',' + str(ScanAccelerationLimit) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerPreCorrectorExcitationSignalGet :  Get pre-corrector excitation signal mode
	def PositionerPreCorrectorExcitationSignalGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerPreCorrectorExcitationSignalGet(' + PositionerName + ',double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(3):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerPreCorrectorExcitationSignalSet :  Set pre-corrector excitation signal mode
	def PositionerPreCorrectorExcitationSignalSet (self, socketId, PositionerName, Frequency, Amplitude, Time):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerPreCorrectorExcitationSignalSet(' + PositionerName + ',' + str(Frequency) + ',' + str(Amplitude) + ',' + str(Time) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerRawEncoderPositionGet :  Get the raw encoder position
	def PositionerRawEncoderPositionGet (self, socketId, PositionerName, UserEncoderPosition):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerRawEncoderPositionGet(' + PositionerName + ',' + str(UserEncoderPosition) + ',double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# PositionersEncoderIndexDifferenceGet :  Return the difference between index of primary axis and secondary axis (only after homesearch)
	def PositionersEncoderIndexDifferenceGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionersEncoderIndexDifferenceGet(' + PositionerName + ',double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# PositionerSGammaExactVelocityAjustedDisplacementGet :  Return adjusted displacement to get exact velocity
	def PositionerSGammaExactVelocityAjustedDisplacementGet (self, socketId, PositionerName, DesiredDisplacement):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerSGammaExactVelocityAjustedDisplacementGet(' + PositionerName + ',' + str(DesiredDisplacement) + ',double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# PositionerSGammaParametersGet :  Read dynamic parameters for one axe of a group for a future displacement
	def PositionerSGammaParametersGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerSGammaParametersGet(' + PositionerName + ',double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerSGammaParametersSet :  Update dynamic parameters for one axe of a group for a future displacement
	def PositionerSGammaParametersSet (self, socketId, PositionerName, Velocity, Acceleration, MinimumTjerkTime, MaximumTjerkTime):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerSGammaParametersSet(' + PositionerName + ',' + str(Velocity) + ',' + str(Acceleration) + ',' + str(MinimumTjerkTime) + ',' + str(MaximumTjerkTime) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerSGammaPreviousMotionTimesGet :  Read SettingTime and SettlingTime
	def PositionerSGammaPreviousMotionTimesGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerSGammaPreviousMotionTimesGet(' + PositionerName + ',double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerStageParameterGet :  Return the stage parameter
	def PositionerStageParameterGet (self, socketId, PositionerName, ParameterName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerStageParameterGet(' + PositionerName + ',' + ParameterName + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerStageParameterSet :  Save the stage parameter
	def PositionerStageParameterSet (self, socketId, PositionerName, ParameterName, ParameterValue):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerStageParameterSet(' + PositionerName + ',' + ParameterName + ',' + ParameterValue + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerTimeFlasherGet :  Read time flasher parameters
	def PositionerTimeFlasherGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerTimeFlasherGet(' + PositionerName + ',double *,double *,double *,bool *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerTimeFlasherSet :  Set time flasher parameters
	def PositionerTimeFlasherSet (self, socketId, PositionerName, MinimumPosition, MaximumPosition, TimeInterval):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerTimeFlasherSet(' + PositionerName + ',' + str(MinimumPosition) + ',' + str(MaximumPosition) + ',' + str(TimeInterval) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerTimeFlasherEnable :  Enable time flasher
	def PositionerTimeFlasherEnable (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerTimeFlasherEnable(' + PositionerName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerTimeFlasherDisable :  Disable time flasher
	def PositionerTimeFlasherDisable (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerTimeFlasherDisable(' + PositionerName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerUserTravelLimitsGet :  Read UserMinimumTarget and UserMaximumTarget
	def PositionerUserTravelLimitsGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerUserTravelLimitsGet(' + PositionerName + ',double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerUserTravelLimitsSet :  Update UserMinimumTarget and UserMaximumTarget
	def PositionerUserTravelLimitsSet (self, socketId, PositionerName, UserMinimumTarget, UserMaximumTarget):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerUserTravelLimitsSet(' + PositionerName + ',' + str(UserMinimumTarget) + ',' + str(UserMaximumTarget) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerWarningFollowingErrorSet :  Set positioner warning following error limit
	def PositionerWarningFollowingErrorSet (self, socketId, PositionerName, WarningFollowingError):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerWarningFollowingErrorSet(' + PositionerName + ',' + str(WarningFollowingError) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# PositionerWarningFollowingErrorGet :  Get positioner warning following error limit
	def PositionerWarningFollowingErrorGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerWarningFollowingErrorGet(' + PositionerName + ',double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# PositionerCorrectorAutoTuning :  Astrom&Hagglund based auto-tuning
	def PositionerCorrectorAutoTuning (self, socketId, PositionerName, TuningMode):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerCorrectorAutoTuning(' + PositionerName + ',' + str(TuningMode) + ',double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(3):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerAccelerationAutoScaling :  Astrom&Hagglund based auto-scaling
	def PositionerAccelerationAutoScaling (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerAccelerationAutoScaling(' + PositionerName + ',double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# MultipleAxesPVTVerification :  Multiple axes PVT trajectory verification
	def MultipleAxesPVTVerification (self, socketId, GroupName, TrajectoryFileName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'MultipleAxesPVTVerification(' + GroupName + ',' + TrajectoryFileName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# MultipleAxesPVTVerificationResultGet :  Multiple axes PVT trajectory verification result get
	def MultipleAxesPVTVerificationResultGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'MultipleAxesPVTVerificationResultGet(' + PositionerName + ',char *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# MultipleAxesPVTExecution :  Multiple axes PVT trajectory execution
	def MultipleAxesPVTExecution (self, socketId, GroupName, TrajectoryFileName, ExecutionNumber):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'MultipleAxesPVTExecution(' + GroupName + ',' + TrajectoryFileName + ',' + str(ExecutionNumber) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# MultipleAxesPVTParametersGet :  Multiple axes PVT trajectory get parameters
	def MultipleAxesPVTParametersGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'MultipleAxesPVTParametersGet(' + GroupName + ',char *,int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# MultipleAxesPVTPulseOutputSet :  Configure pulse output on trajectory
	def MultipleAxesPVTPulseOutputSet (self, socketId, GroupName, StartElement, EndElement, TimeInterval):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'MultipleAxesPVTPulseOutputSet(' + GroupName + ',' + str(StartElement) + ',' + str(EndElement) + ',' + str(TimeInterval) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# MultipleAxesPVTPulseOutputGet :  Get pulse output on trajectory configuration
	def MultipleAxesPVTPulseOutputGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'MultipleAxesPVTPulseOutputGet(' + GroupName + ',int *,int *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(3):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# MultipleAxesPVTLoadToMemory :  Multiple Axes Load PVT trajectory through function
	def MultipleAxesPVTLoadToMemory (self, socketId, GroupName, TrajectoryPart):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'MultipleAxesPVTLoadToMemory(' + GroupName + ',' + TrajectoryPart + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# MultipleAxesPVTResetInMemory :  Multiple Axes PVT trajectory reset in memory
	def MultipleAxesPVTResetInMemory (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'MultipleAxesPVTResetInMemory(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# SingleAxisSlaveModeEnable :  Enable the slave mode
	def SingleAxisSlaveModeEnable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'SingleAxisSlaveModeEnable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# SingleAxisSlaveModeDisable :  Disable the slave mode
	def SingleAxisSlaveModeDisable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'SingleAxisSlaveModeDisable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# SingleAxisSlaveParametersSet :  Set slave parameters
	def SingleAxisSlaveParametersSet (self, socketId, GroupName, PositionerName, Ratio):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'SingleAxisSlaveParametersSet(' + GroupName + ',' + PositionerName + ',' + str(Ratio) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# SingleAxisSlaveParametersGet :  Get slave parameters
	def SingleAxisSlaveParametersGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'SingleAxisSlaveParametersGet(' + GroupName + ',char *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# SingleAxisThetaClampDisable :  Set clamping disable on selected group
	def SingleAxisThetaClampDisable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'SingleAxisThetaClampDisable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# SingleAxisThetaClampEnable :  Set clamping enable on selected group
	def SingleAxisThetaClampEnable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'SingleAxisThetaClampEnable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# SingleAxisThetaSlaveModeEnable :  Enable the slave mode
	def SingleAxisThetaSlaveModeEnable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'SingleAxisThetaSlaveModeEnable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# SingleAxisThetaSlaveModeDisable :  Disable the slave mode
	def SingleAxisThetaSlaveModeDisable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'SingleAxisThetaSlaveModeDisable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# SingleAxisThetaSlaveParametersSet :  Set slave parameters
	def SingleAxisThetaSlaveParametersSet (self, socketId, GroupName, PositionerName, Ratio):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'SingleAxisThetaSlaveParametersSet(' + GroupName + ',' + PositionerName + ',' + str(Ratio) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# SingleAxisThetaSlaveParametersGet :  Get slave parameters
	def SingleAxisThetaSlaveParametersGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'SingleAxisThetaSlaveParametersGet(' + GroupName + ',char *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# SpindleSlaveModeEnable :  Enable the slave mode
	def SpindleSlaveModeEnable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'SpindleSlaveModeEnable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# SpindleSlaveModeDisable :  Disable the slave mode
	def SpindleSlaveModeDisable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'SpindleSlaveModeDisable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# SpindleSlaveParametersSet :  Set slave parameters
	def SpindleSlaveParametersSet (self, socketId, GroupName, PositionerName, Ratio):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'SpindleSlaveParametersSet(' + GroupName + ',' + PositionerName + ',' + str(Ratio) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# SpindleSlaveParametersGet :  Get slave parameters
	def SpindleSlaveParametersGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'SpindleSlaveParametersGet(' + GroupName + ',char *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# GroupSpinParametersSet :  Modify Spin parameters on selected group and activate the continuous move
	def GroupSpinParametersSet (self, socketId, GroupName, Velocity, Acceleration):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupSpinParametersSet(' + GroupName + ',' + str(Velocity) + ',' + str(Acceleration) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# GroupSpinParametersGet :  Get Spin parameters on selected group
	def GroupSpinParametersGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupSpinParametersGet(' + GroupName + ',double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GroupSpinCurrentGet :  Get Spin current on selected group
	def GroupSpinCurrentGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupSpinCurrentGet(' + GroupName + ',double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# GroupSpinModeStop :  Stop Spin mode on selected group with specified acceleration
	def GroupSpinModeStop (self, socketId, GroupName, Acceleration):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'GroupSpinModeStop(' + GroupName + ',' + str(Acceleration) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# XYLineArcVerification :  XY trajectory verification
	def XYLineArcVerification (self, socketId, GroupName, TrajectoryFileName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYLineArcVerification(' + GroupName + ',' + TrajectoryFileName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# XYLineArcVerificationResultGet :  XY trajectory verification result get
	def XYLineArcVerificationResultGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYLineArcVerificationResultGet(' + PositionerName + ',char *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# XYLineArcExecution :  XY trajectory execution
	def XYLineArcExecution (self, socketId, GroupName, TrajectoryFileName, Velocity, Acceleration, ExecutionNumber):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYLineArcExecution(' + GroupName + ',' + TrajectoryFileName + ',' + str(Velocity) + ',' + str(Acceleration) + ',' + str(ExecutionNumber) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# XYLineArcParametersGet :  XY trajectory get parameters
	def XYLineArcParametersGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYLineArcParametersGet(' + GroupName + ',char *,double *,double *,int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(3):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# XYLineArcPulseOutputSet :  Configure pulse output on trajectory
	def XYLineArcPulseOutputSet (self, socketId, GroupName, StartLength, EndLength, PathLengthInterval):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYLineArcPulseOutputSet(' + GroupName + ',' + str(StartLength) + ',' + str(EndLength) + ',' + str(PathLengthInterval) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# XYLineArcPulseOutputGet :  Get pulse output on trajectory configuration
	def XYLineArcPulseOutputGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYLineArcPulseOutputGet(' + GroupName + ',double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(3):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# XYPVTVerification :  XY PVT trajectory verification
	def XYPVTVerification (self, socketId, GroupName, TrajectoryFileName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYPVTVerification(' + GroupName + ',' + TrajectoryFileName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# XYPVTVerificationResultGet :  XY PVT trajectory verification result get
	def XYPVTVerificationResultGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYPVTVerificationResultGet(' + PositionerName + ',char *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# XYPVTExecution :  XY PVT trajectory execution
	def XYPVTExecution (self, socketId, GroupName, TrajectoryFileName, ExecutionNumber):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYPVTExecution(' + GroupName + ',' + TrajectoryFileName + ',' + str(ExecutionNumber) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# XYPVTParametersGet :  XY PVT trajectory get parameters
	def XYPVTParametersGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYPVTParametersGet(' + GroupName + ',char *,int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# XYPVTPulseOutputSet :  Configure pulse output on trajectory
	def XYPVTPulseOutputSet (self, socketId, GroupName, StartElement, EndElement, TimeInterval):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYPVTPulseOutputSet(' + GroupName + ',' + str(StartElement) + ',' + str(EndElement) + ',' + str(TimeInterval) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# XYPVTPulseOutputGet :  Get pulse output on trajectory configuration
	def XYPVTPulseOutputGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYPVTPulseOutputGet(' + GroupName + ',int *,int *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(3):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# XYPVTLoadToMemory :  XY Load PVT trajectory through function
	def XYPVTLoadToMemory (self, socketId, GroupName, TrajectoryPart):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYPVTLoadToMemory(' + GroupName + ',' + TrajectoryPart + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# XYPVTResetInMemory :  XY PVT trajectory reset in memory
	def XYPVTResetInMemory (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYPVTResetInMemory(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# XYZGroupPositionCorrectedProfilerGet :  Return corrected profiler positions
	def XYZGroupPositionCorrectedProfilerGet (self, socketId, GroupName, PositionX, PositionY, PositionZ):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYZGroupPositionCorrectedProfilerGet(' + GroupName + ',' + str(PositionX) + ',' + str(PositionY) + ',' + str(PositionZ) + ',double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(3):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# XYZGroupPositionPCORawEncoderGet :  Return PCO raw encoder positions
	def XYZGroupPositionPCORawEncoderGet (self, socketId, GroupName, PositionX, PositionY, PositionZ):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYZGroupPositionPCORawEncoderGet(' + GroupName + ',' + str(PositionX) + ',' + str(PositionY) + ',' + str(PositionZ) + ',double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(3):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# XYZSplineVerification :  XYZ trajectory verifivation
	def XYZSplineVerification (self, socketId, GroupName, TrajectoryFileName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYZSplineVerification(' + GroupName + ',' + TrajectoryFileName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# XYZSplineVerificationResultGet :  XYZ trajectory verification result get
	def XYZSplineVerificationResultGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYZSplineVerificationResultGet(' + PositionerName + ',char *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# XYZSplineExecution :  XYZ trajectory execution
	def XYZSplineExecution (self, socketId, GroupName, TrajectoryFileName, Velocity, Acceleration):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYZSplineExecution(' + GroupName + ',' + TrajectoryFileName + ',' + str(Velocity) + ',' + str(Acceleration) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# XYZSplineParametersGet :  XYZ trajectory get parameters
	def XYZSplineParametersGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'XYZSplineParametersGet(' + GroupName + ',char *,double *,double *,int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(3):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# TZPVTVerification :  TZ PVT trajectory verification
	def TZPVTVerification (self, socketId, GroupName, TrajectoryFileName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TZPVTVerification(' + GroupName + ',' + TrajectoryFileName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# TZPVTVerificationResultGet :  TZ PVT trajectory verification result get
	def TZPVTVerificationResultGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TZPVTVerificationResultGet(' + PositionerName + ',char *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# TZPVTExecution :  TZ PVT trajectory execution
	def TZPVTExecution (self, socketId, GroupName, TrajectoryFileName, ExecutionNumber):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TZPVTExecution(' + GroupName + ',' + TrajectoryFileName + ',' + str(ExecutionNumber) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# TZPVTParametersGet :  TZ PVT trajectory get parameters
	def TZPVTParametersGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TZPVTParametersGet(' + GroupName + ',char *,int *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# TZPVTPulseOutputSet :  Configure pulse output on trajectory
	def TZPVTPulseOutputSet (self, socketId, GroupName, StartElement, EndElement, TimeInterval):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TZPVTPulseOutputSet(' + GroupName + ',' + str(StartElement) + ',' + str(EndElement) + ',' + str(TimeInterval) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# TZPVTPulseOutputGet :  Get pulse output on trajectory configuration
	def TZPVTPulseOutputGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TZPVTPulseOutputGet(' + GroupName + ',int *,int *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(3):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# TZPVTLoadToMemory :  TZ Load PVT trajectory through function
	def TZPVTLoadToMemory (self, socketId, GroupName, TrajectoryPart):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TZPVTLoadToMemory(' + GroupName + ',' + TrajectoryPart + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# TZPVTResetInMemory :  TZ PVT trajectory reset in memory
	def TZPVTResetInMemory (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TZPVTResetInMemory(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# TZFocusModeEnable :  Enable the focus mode
	def TZFocusModeEnable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TZFocusModeEnable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# TZFocusModeDisable :  Disable the focus mode
	def TZFocusModeDisable (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TZFocusModeDisable(' + GroupName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# TZTrackingUserMaximumZZZTargetDifferenceGet :  Get user maximum ZZZ target difference for tracking control
	def TZTrackingUserMaximumZZZTargetDifferenceGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TZTrackingUserMaximumZZZTargetDifferenceGet(' + GroupName + ',double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
			j += 1
		retList.append(eval(returnedString[i:i+j]))

		return retList


	# TZTrackingUserMaximumZZZTargetDifferenceSet :  Set user maximum ZZZ target difference for tracking control
	def TZTrackingUserMaximumZZZTargetDifferenceSet (self, socketId, GroupName, UserMaximumZZZTargetDifference):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TZTrackingUserMaximumZZZTargetDifferenceSet(' + GroupName + ',' + str(UserMaximumZZZTargetDifference) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# FocusProcessSocketReserve :  Set user maximum ZZZ target difference for tracking control
	def FocusProcessSocketReserve (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'FocusProcessSocketReserve()'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# FocusProcessSocketFree :  Set user maximum ZZZ target difference for tracking control
	def FocusProcessSocketFree (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'FocusProcessSocketFree()'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# PositionerMotorOutputOffsetGet :  Get soft (user defined) motor output DAC offsets
	def PositionerMotorOutputOffsetGet (self, socketId, PositionerName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerMotorOutputOffsetGet(' + PositionerName + ',double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(4):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# PositionerMotorOutputOffsetSet :  Set soft (user defined) motor output DAC offsets
	def PositionerMotorOutputOffsetSet (self, socketId, PositionerName, PrimaryDAC1, PrimaryDAC2, SecondaryDAC1, SecondaryDAC2):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'PositionerMotorOutputOffsetSet(' + PositionerName + ',' + str(PrimaryDAC1) + ',' + str(PrimaryDAC2) + ',' + str(SecondaryDAC1) + ',' + str(SecondaryDAC2) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# SingleAxisThetaPositionRawGet :  Get raw encoder positions for single axis theta encoder
	def SingleAxisThetaPositionRawGet (self, socketId, GroupName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'SingleAxisThetaPositionRawGet(' + GroupName + ',double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(3):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# EEPROMCIESet :  Get raw encoder positions for single axis theta encoder
	def EEPROMCIESet (self, socketId, CardNumber, ReferenceString):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'EEPROMCIESet(' + str(CardNumber) + ',' + ReferenceString + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# EEPROMDACOffsetCIESet :  Get raw encoder positions for single axis theta encoder
	def EEPROMDACOffsetCIESet (self, socketId, PlugNumber, DAC1Offset, DAC2Offset):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'EEPROMDACOffsetCIESet(' + str(PlugNumber) + ',' + str(DAC1Offset) + ',' + str(DAC2Offset) + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# EEPROMDriverSet :  Get raw encoder positions for single axis theta encoder
	def EEPROMDriverSet (self, socketId, PlugNumber, ReferenceString):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'EEPROMDriverSet(' + str(PlugNumber) + ',' + ReferenceString + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# EEPROMINTSet :  Get raw encoder positions for single axis theta encoder
	def EEPROMINTSet (self, socketId, CardNumber, ReferenceString):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'EEPROMINTSet(' + str(CardNumber) + ',' + ReferenceString + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# CPUCoreAndBoardSupplyVoltagesGet :  Get raw encoder positions for single axis theta encoder
	def CPUCoreAndBoardSupplyVoltagesGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'CPUCoreAndBoardSupplyVoltagesGet(double *,double *,double *,double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(8):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# CPUTemperatureAndFanSpeedGet :  Get raw encoder positions for single axis theta encoder
	def CPUTemperatureAndFanSpeedGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'CPUTemperatureAndFanSpeedGet(double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(2):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# ActionListGet :  Action list
	def ActionListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ActionListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# ActionExtendedListGet :  Action extended list
	def ActionExtendedListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ActionExtendedListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# APIExtendedListGet :  API method list
	def APIExtendedListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'APIExtendedListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# APIListGet :  API method list without extended API
	def APIListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'APIListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# ControllerStatusListGet :  Controller status list
	def ControllerStatusListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ControllerStatusListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# ErrorListGet :  Error list
	def ErrorListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ErrorListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# EventListGet :  General event list
	def EventListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'EventListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# GatheringListGet :  Gathering type list
	def GatheringListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'GatheringListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# GatheringExtendedListGet :  Gathering type extended list
	def GatheringExtendedListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'GatheringExtendedListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# GatheringExternalListGet :  External Gathering type list
	def GatheringExternalListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'GatheringExternalListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# GroupStatusListGet :  Group status list
	def GroupStatusListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'GroupStatusListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# HardwareInternalListGet :  Internal hardware list
	def HardwareInternalListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'HardwareInternalListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# HardwareDriverAndStageGet :  Smart hardware
	def HardwareDriverAndStageGet (self, socketId, PlugNumber):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'HardwareDriverAndStageGet(' + str(PlugNumber) + ',char *,char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# ObjectsListGet :  Group name and positioner name
	def ObjectsListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ObjectsListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# PositionerErrorListGet :  Positioner error list
	def PositionerErrorListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'PositionerErrorListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# PositionerHardwareStatusListGet :  Positioner hardware status list
	def PositionerHardwareStatusListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'PositionerHardwareStatusListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# PositionerDriverStatusListGet :  Positioner driver status list
	def PositionerDriverStatusListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'PositionerDriverStatusListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# ReferencingActionListGet :  Get referencing action list
	def ReferencingActionListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ReferencingActionListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# ReferencingSensorListGet :  Get referencing sensor list
	def ReferencingSensorListGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ReferencingSensorListGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# GatheringUserDatasGet :  Return UserDatas values
	def GatheringUserDatasGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'GatheringUserDatasGet(double *,double *,double *,double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(8):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# ControllerMotionKernelPeriodMinMaxGet :  Get controller motion kernel min/max periods
	def ControllerMotionKernelPeriodMinMaxGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ControllerMotionKernelPeriodMinMaxGet(double *,double *,double *,double *,double *,double *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		if (error != 0):
			return [error, returnedString]

		i, j, retList = 0, 0, [error]
		for paramNb in range(6):
			while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
				j += 1
			retList.append(eval(returnedString[i:i+j]))
			i, j = i+j+1, 0

		return retList


	# ControllerMotionKernelPeriodMinMaxReset :  Reset controller motion kernel min/max periods
	def ControllerMotionKernelPeriodMinMaxReset (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'ControllerMotionKernelPeriodMinMaxReset()'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# SocketsStatusGet :  Get sockets current status
	def SocketsStatusGet (self, socketId):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = b'SocketsStatusGet(char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command)
		return [error, returnedString]


	# TestTCP :  Test TCP/IP transfert
	def TestTCP (self, socketId, InputString):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'TestTCP(' + InputString + ',char *)'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# OptionalModuleExecute :  Execute an optional module
	def OptionalModuleExecute (self, socketId, ModuleFileName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'OptionalModuleExecute(' + ModuleFileName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]


	# OptionalModuleKill :  Kill an optional module
	def OptionalModuleKill (self, socketId, TaskName):
		if (XPS.__usedSockets[socketId] == 0):
			return

		command = 'OptionalModuleKill(' + TaskName + ')'
		[error, returnedString] = self.__sendAndReceive(socketId, command.encode())
		return [error, returnedString]
