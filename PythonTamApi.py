import clr
from os import environ, path
from System import Exception, Enum, Func, TimeSpan
from System.Linq import Enumerable

TAM_SOFTWARE_PATH = path.join(environ['ProgramFiles'], 'Triamec', 'Tam', '7.27.0', 'SDK')

clr.AddReference(path.join(TAM_SOFTWARE_PATH, 'Triamec.Common.dll'))
clr.AddReference(path.join(TAM_SOFTWARE_PATH, 'Tam.dll'))

# These references need to be added in order to circumvent binding failures
clr.AddReference(path.join(TAM_SOFTWARE_PATH, 'System.Memory'))
clr.AddReference(path.join(TAM_SOFTWARE_PATH, 'System.Runtime.CompilerServices.Unsafe.dll'))

from Triamec.Tam import TamEnumerable, TamAxis, TamTopology
from Triamec import CommonExtensions
from Triamec.TriaLink import DeviceState
from Triamec.TriaLink.Adapter import DataLinkLayers
from Triamec.Tam.Acquisitions import TamAcquisitionExtensions

# Create the root object representing the topology of the TAM hardware.
# Note that we must dispose this object at the end in order to clean up resources.
topo = TamTopology(None)
try:
    topo.AddLocalTamSystem(None)
except Exception as e:
    CommonExtensions.FullMessage(e)

# Connect the drive / get system
tamSystem = topo.Systems[0]
try:
    # Boot the Tria-Link so that it learns about connected stations.
    tamSystem.Identify()
except Exception as e:
    CommonExtensions.FullMessage(e)

# Set the axis name the example works with.
axis_name = 'Axis 0'

# This code looks weird since we need to specify all extension methods and generic arguments explicitly.
# In C#, we could express this as
# var axis = topology.AsDepthFirstLeaves<TamAxis>().FirstOrDefault(a => a.Name == name);
# Get the axis with the predefined name
axis = Enumerable.FirstOrDefault[TamAxis](TamEnumerable.AsDepthFirstLeaves[TamAxis](topo), Func[TamAxis, bool](lambda a : a.Name == axis_name))

# Read arbitrary registers (e.g. Axis state)
state = axis.Register.Signals.General.AxisState.Read()
print(axis_name + ': ' + state.ToString())

# Create acquisition variable for master position, configure and acquire data
posReg = axis.Register.Signals.PositionController.MasterPosition
posVar = TamAcquisitionExtensions.CreateVariable(posReg)
duration = TimeSpan.FromSeconds(1)
TamAcquisitionExtensions.Acquire(posVar,duration)
result = list(posVar)
print('acquired ' + str(len(result)) + ' samples')

# Clean up resources
topo.Dispose()
