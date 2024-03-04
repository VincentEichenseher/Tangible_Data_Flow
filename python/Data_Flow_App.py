#Based on the pyqtgraph Flowchart example that can be accessed with the command "pythom -m pyqtgraph.examples"
import pandas as pd
import pyqtgraph as pg
import json
import argparse
import threading
import sys

from lib.pythonosc import dispatcher
from lib.pythonosc import osc_server

from parsers.MessageParser import MessageParser
from parsers.MessageTypes import MessageTypes
import signal

from pyqtgraph.flowchart.NodeLibrary import NodeLibrary
from pyqtgraph.flowchart import Flowchart
from pyqtgraph.Qt import QtWidgets
from pyqtgraph.Qt.QtCore import QTimer

from CustomNodes import SelectColumnNode, JoinDataNode, ThresholdDataNode, GroupByNode, MathOperationNode, MissingDataNode, LinePlotWidgetNode, HistogramWidgetNode
from sklearn import datasets

# important params:
# modify as needed
update_interval = 300 # update interval in ms

# temp storeage variables
json_data = None #json data cache 
elements_added = {} # dict to cache references to currently active elements (so these can be removed and to avoid duplication of elements on update)

# create Qt app
signal.signal(signal.SIGINT, signal.SIG_DFL) # SIGINT = Ctrl + C; this line lets us kill the Qt app and timer with te rest of this script
app = QtWidgets.QApplication(sys.argv)

## Create main window and layout
win = QtWidgets.QMainWindow()
win.setWindowTitle('pyqtgraph: Data-Flow graph')
cw = QtWidgets.QWidget()
win.setCentralWidget(cw)
layout = QtWidgets.QGridLayout()
cw.setLayout(layout)

## Create flowchart object, set input/output Nodes (these are the input and output of the entire data-flow process)
fc = Flowchart(terminals={
    'dataIn': {'io': 'in'},
    'dataOut': {'io': 'out'}    
})
w = fc.widget()
w.chartWidget._viewBox.setMouseEnabled(False,False)
## Add flowchart pannel
layout.addWidget(w.chartWidget.viewDock, 0, 0, 2, 1)

## init two plot widgets (areas for displaying plots) to main screen
pw1 = pg.PlotWidget()
pw2 = pg.PlotWidget()
layout.addWidget(pw1, 0, 1, 1, 1)
layout.addWidget(pw2, 1, 1, 1, 1)

layout.setColumnStretch(0, 27)
layout.setColumnStretch(1, 15)

win.showMaximized()

# load data
df = pd.read_csv("./drug-overdose-death-rates.csv")
data = df.to_dict()

## set Input Node data
fc.setInput(dataIn=data)
                        
# add custom Nodes

nodeLibrary = NodeLibrary()
nodeLibrary.addNodeType(SelectColumnNode, [('Filter',)])
nodeLibrary.addNodeType(JoinDataNode, [('Filter',)])
nodeLibrary.addNodeType(ThresholdDataNode, [('Filter',)])
nodeLibrary.addNodeType(GroupByNode, [('Filter',)])
nodeLibrary.addNodeType(MathOperationNode, [('Operations',)])
nodeLibrary.addNodeType(MissingDataNode, [('Operations',)])
nodeLibrary.addNodeType(LinePlotWidgetNode, [('Display',)])
nodeLibrary.addNodeType(HistogramWidgetNode, [('Display',)])
fc.setLibrary(nodeLibrary)

# set PlotWidget Nodes (Nodes for showing plots in the plotwidgets we created earlier)

pw1Node = fc.createNode('LinePlotWidget', pos=(300, -100))
pw1Node.setPlot(pw1)

pw2Node = fc.createNode('HistogramWidget', pos=(300, -50))
pw2Node.setPlot(pw2)

# load json for the first time
#if json_data is None:
#    with open("../node_data.json","r") as fh:
#        json_data = json.load(fh)

# define functions
        
def main():
    sys.setrecursionlimit(10000)
    mp = MessageParser()

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=3333, help="The port to listen on")
    args = parser.parse_args()

    dispatch = dispatcher.Dispatcher()
    dispatch.map(MessageTypes.POINTER.value, mp.parse)
    dispatch.map(MessageTypes.TOKEN.value, mp.parse)
    dispatch.map(MessageTypes.BOUNDS.value, mp.parse)
    dispatch.map(MessageTypes.FRAME.value, mp.parse)
    dispatch.map(MessageTypes.ALIVE.value, mp.parse)
    dispatch.map(MessageTypes.SYMBOL.value, mp.parse)
    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatch)

    print("Serving on {}".format(server.server_address))

    server_ = threading.Thread(target=server.serve_forever)

    #dw = QDrawWidget.QDrawWidget(app, mp)
    #dw.on_close.connect(lambda: server.shutdown())

    timer = QTimer()
    timer.timeout.connect(create_nodes_from_json)

    server_.start()

    timer.start(update_interval)

    app.aboutToQuit.connect(lambda: server.shutdown())
    app.aboutToQuit.connect(lambda: timer.stop())

    sys.exit(app.exec_())

# create nodes based on changes to json
def create_nodes_from_json():
    global json_data
    #listen for markers here
    stack_data = None
    with open("./node_data.json","r") as fh:
      json_data = json.load(fh)
    with open("./stack_data.json","r") as fh:
      stack_data = json.load(fh)
    for element in json_data["nodes"]:
        el_id = element["aruco_id"]
        id_as_string = str(el_id)
        if element["is_active"] is True and id_as_string not in list(elements_added):
            nodename = element["node_type"]
            nodecoords = element["coord"]
            node = fc.createNode(nodename, pos=[nodecoords[0], nodecoords[1]])
            elements_added.update({id_as_string:node})
        elif element["is_active"] is True and id_as_string in list(elements_added):
            # change crtl-widget values
            ui = elements_added[id_as_string].ctrls
            graphics_item = elements_added[id_as_string].graphicsItem()
            new_values = stack_data["nodes"][el_id]["values"]
            new_coords = json_data["nodes"][el_id]["coord"]
            graphics_item.setPos(new_coords[0],new_coords[1])
            for key in new_values.keys():
                if key in [1,4,5,6,7]:
                    ui[key].addItem(new_values[key])
                elif key in [0,2,3]:
                    ui[key].setValue(new_values[key])
        elif element["is_active"] is False and id_as_string in list(elements_added):
            fc.removeNode(elements_added[id_as_string])
            elements_added.pop(id_as_string)
    fc.outputChanged()

# main
if __name__ == '__main__':
    main() # execute main qt event loop

