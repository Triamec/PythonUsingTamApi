import clr
from os import environ, path
from System import Exception, Enum, Func, TimeSpan
from System.Linq import Enumerable

TAM_SOFTWARE_PATH = path.join(environ['ProgramFiles'], 'Triamec', 'Tam', '7.24.1', 'SDK')

clr.AddReference(path.join(TAM_SOFTWARE_PATH, 'Triamec.Common.dll'))
clr.AddReference(path.join(TAM_SOFTWARE_PATH, 'Tam.dll'))

from Triamec.Tam import TamEnumerable, TamAxis, TamTopology
from Triamec import CommonExtensions
from Triamec.TriaLink import DeviceState
from Triamec.TriaLink.Adapter import DataLinkLayers
from Triamec.Tam.Acquisitions import TamAcquisitionExtensions

topo = TamTopology(None)
try:
    topo.AddLocalTamSystem(None)
except Exception as e:
    CommonExtensions.FullMessage(e)

tamSystem = topo.Systems[0]
try:
    tamSystem.Identify()
except Exception as e:
    CommonExtensions.FullMessage(e)

axis_name = 'Axis 0'

# This code looks weird since we need to specify all extension methods and generic arguments explicitly.
# In C#, we could express this as
# var axis = topology.AsDepthFirstLeaves<TamAxis>().FirstOrDefault(a => a.Name == name);
axis = Enumerable.FirstOrDefault[TamAxis](TamEnumerable.AsDepthFirstLeaves[TamAxis](topo), Func[TamAxis, bool](lambda a : a.Name == axis_name))

# read arbitrary registers
state = axis.Register.Signals.General.AxisState.Read()
print(axis_name + ': ' + state.ToString())

# given axis, a TamAxis object
posReg = axis.Register.Signals.General.PowerStageTemperature
posVar = TamAcquisitionExtensions.CreateVariable(posReg)
duration = TimeSpan.FromSeconds(2)
TamAcquisitionExtensions.Acquire(posVar,duration)
result = list(posVar)
print('acquired ' + str(len(result)) + ' samples')

# Release resources
topo.Dispose()
