from PyANC350v4 import Positioner
import time

ax = {'x':0,'y':1,'z':2}
#define a dict of axes to make things simpler

anc = Positioner()

print('-------obtaining all possible gettable values for x---------')
#get every possible gettable value
print('getActuatorName',anc.getActuatorName(ax['x']))
print('getActuatorType',anc.getActuatorType(ax['x']))
print('getAmplitude',anc.getAmplitude(ax['x']))
print('getAxisStatus',anc.getAxisStatus(ax['x']))
print('getDeviceConfig',anc.getDeviceConfig())
print('getDeviceInfo',anc.getDeviceInfo())
print('getFirmwareVersion',anc.getFirmwareVersion())
print('getFrequency',anc.getFrequency(ax['x']))
print('getPosition',anc.getPosition(ax['x']))
print('-------------------------------------------------------------')
