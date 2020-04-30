
from neuromllite import Network, Cell, InputSource, Population, Synapse
from neuromllite import Projection, RandomConnectivity, Input, Simulation
import sys

################################################################################
###   Build new network

net = Network(id='FNTest')
net.notes = 'Example FN'
net.parameters = { 'N': 1}

cell = Cell(id='fnCell', 
            neuroml2_cell='fitzHughNagumo1969Cell')
cell.parameters = {}

params = {'a':0.7, 'b':0.8, 'I': 1.0, 'phi': 0.08, 'V0': 0.0, 'W0':0.0}

for p in params:
    cell.parameters[p]=p
    net.parameters[p]=params[p]
    
net.cells.append(cell)


pop = Population(id='fnPop', size='1', component=cell.id, properties={'color':'.7 0 0'})
net.populations.append(pop)
'''
net.parameters['delay'] = '100ms'
net.parameters['stim_amp'] = '1'
net.parameters['duration'] = '500ms'
input_source = InputSource(id='iclamp_0', 
                           neuroml2_input='PulseGeneratorDL', 
                           parameters={'amplitude':'stim_amp', 'delay':'delay', 'duration':'duration'})'''
#net.input_sources.append(input_source)

#net.inputs.append(Input(id='stim',
#                        input_source=input_source.id,
#                        population=pop.id,
#                        percentage=100))
                            
print(net)
print(net.to_json())
new_file = net.to_json_file('%s.json'%net.id)


################################################################################
###   Build Simulation object & save as JSON

sim = Simulation(id='Sim%s'%net.id,
                 network=new_file,
                 duration='400',
                 dt='0.01',
                 recordVariables={'V':{'all':'*'},
                                  'W':{'all':'*'}},
                 plots2D={'VW':{'x_axis':'fnPop[0]/V',
                                 'y_axis':'fnPop[0]/W'}},
                plots3D={'V-W-t':{'x_axis':'t',
                  'y_axis':'fnPop[0]/V',
                  'z_axis':'fnPop[0]/W'}})
                 
sim.to_json_file()



################################################################################
###   Run in some simulators

from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

check_to_generate_or_run(sys.argv, sim)
