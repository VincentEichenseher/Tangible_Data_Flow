import numpy as np
import pandas as pd

from pyqtgraph import BarGraphItem, PlotDataItem, ScatterPlotItem
from pyqtgraph.flowchart.library.common import CtrlNode
from pyqtgraph.Qt import QtCore

class SelectColumnNode(CtrlNode):
    "returns column data by name"
    nodeName = 'GetColumnData'
    uiTemplate = [
        ('column',  'intSpin', {'value': 0, 'step': 1, 'bounds': [0, None]}),]
    
    def __init__(self, name):
        terminals={'data': {'io':'in'},'output':{'io':'out'}}
        CtrlNode.__init__(self, name, terminals=terminals)
        
        
    def process(self, **kwds):
        index = self.ctrls['column'].value()
        df = pd.DataFrame.from_dict(kwds['data'])
        column = list(df.keys())[index]
        data = df[column]
        result = data.to_dict()
        self.rename(str(column)+" Data")
        self.graphicsItem().setPen()
        self.graphicsItem().nameItem.setPlainText(self._name)
        return {'output': result}
    
class JoinDataNode(CtrlNode):
    "preforms join on dataframes or columns"
    nodeName = 'JoinData'
    uiTemplate = [
        ('join_type',  'combo', {'values': ["Full","Inner","Right","Left"], 'index': 0}),]
    
    def __init__(self, name):
        terminals={'A': {'io':'in'},'B':{'io':'in'},'output':{'io':'out'}}
        CtrlNode.__init__(self, name, terminals=terminals)
        
        
    def process(self, **kwds):
        joinType = str(self.ctrls['join_type'].currentText())
        self.rename(joinType +" Join")
        self.graphicsItem().setPen()
        self.graphicsItem().nameItem.setPlainText(self._name)
        try:
            dfA = pd.DataFrame.from_dict(kwds['A'], orient='columns')
            dfB = pd.DataFrame.from_dict(kwds['B'], orient='columns')
        except:
            dfA = pd.DataFrame.from_dict(kwds['A'], orient='index')
            dfB = pd.DataFrame.from_dict(kwds['B'], orient='index')
        if joinType == "Full":
            data = dfA.join(dfB, how="outer", lsuffix="_A", rsuffix="_B")
        elif joinType == "Inner":
            data = dfA.join(dfB, how="inner", lsuffix="_A", rsuffix="_B")
        elif joinType == "Left":
            data = dfA.join(dfB, how="left", lsuffix="_A", rsuffix="_B")
        elif joinType == "Right":
            data = dfA.join(dfB, how="right", lsuffix="_A", rsuffix="_B")
        result = data.to_dict()
        return {'output': result}
    
class ThresholdDataNode(CtrlNode):
    "preforms clip on dataframes or columns (applies threshold)"
    nodeName = 'ThresholdData'
    uiTemplate = [
        ('lower_threshold', 'spin', {'value': 0.0, 'step': 1, 'bounds': [0.0, None]}),
        ('upper_threshold', 'spin', {'value': None, 'step': 1, 'bounds': [0.0, None]})]
    
    def __init__(self, name):
        terminals={'data':{'io':'in'},'output':{'io':'out'}}
        CtrlNode.__init__(self, name, terminals=terminals)
        
        
    def process(self, **kwds):
        thresLower = self.ctrls["lower_threshold"].value()
        thresUpper = self.ctrls["upper_threshold"].value()
        self.rename(str(thresLower) + " ≤ Data ≤ " + str(thresUpper))
        self.graphicsItem().setPen()
        self.graphicsItem().nameItem.setPlainText(self._name)
        try:
            df = pd.DataFrame.from_dict(kwds['data'])
        except:
            df = pd.DataFrame.from_dict(kwds['data'],orient='index')
        data = df.clip(thresLower,thresUpper)
        result = data.to_dict()
        return {'output': result}
    

class GroupByNode(CtrlNode):
    "groups a variable by another variable and calculates statistics"
    nodeName = 'CalculateStats'
    uiTemplate = [
        ('column',  'intSpin', {'value': 0, 'step': 1, 'bounds': [0, None]}),
        ('group_by',  'intSpin', {'value': 0, 'step': 1, 'bounds': [0, None]}),]
    
    def __init__(self, name):
        terminals = {'data': {'io':'in'},
                     'min':{'io':'out'},
                     'max':{'io':'out'},
                     'mean':{'io':'out'},
                     'median':{'io':'out'},
                     'var':{'io':'out'},
                     'std':{'io':'out'},
                     'group':{'io':'out'}}
        CtrlNode.__init__(self, name, terminals=terminals)
        
    def process(self, **kwds):
        df = pd.DataFrame.from_dict(kwds['data'])
        index = list(df.keys())[self.ctrls['column'].value()]
        group_var = None
        if self.ctrls['group_by'].value != None:
            group_var = list(df.keys())[self.ctrls['group_by'].value()]
            stats = df.groupby(group_var).agg(['min','max','mean','median','std','var'])
        else:
            stats = df.agg(['min','max','mean','median','std','var'])
            stats = stats.unstack(level=-1).to_frame(0).T
        stats = stats.set_axis(stats.columns.map('_'.join), axis=1, inplace=False)
        result = stats.to_dict()
        self.rename(str(index)+" by " + str(group_var))
        self.graphicsItem().setPen()
        self.graphicsItem().nameItem.setPlainText(self._name)
        if self.ctrls['column'].value() != self.ctrls['group_by'].value():
            return {'max': result[str(index) + '_' + 'max'],
                    'min': result[str(index)+ '_' + 'min'],
                    'mean': result[str(index)+ '_' + 'mean'],
                    'var': result[str(index)+ '_' + 'var'],
                    'std': result[str(index)+ '_' + 'std'],
                    'group': stats.index}
        else:
            return {'group': stats.index}
        
class MathOperationNode(CtrlNode):
    "preforms a mathemetical operation (+, -, *, /) on dataframes or columns"
    nodeName = 'MathOperation'
    uiTemplate = [
        ('operation_type',  'combo', {'values': ["Addition","Subtraction","Multiplication","Division"], 'index': 0}),]
    
    def __init__(self, name):
        terminals={'A': {'io':'in'},'B':{'io':'in'},'output':{'io':'out'}}
        CtrlNode.__init__(self, name, terminals=terminals)
        
        
    def process(self, **kwds):
        operationType = str(self.ctrls['operation_type'].currentText())
        self.rename(operationType)
        self.graphicsItem().setPen()
        self.graphicsItem().nameItem.setPlainText(self._name)
        try:
            dfA = pd.DataFrame.from_dict(kwds['A'], orient='columns')
            dfB = pd.DataFrame.from_dict(kwds['B'], orient='columns')
        except:
            dfA = pd.DataFrame.from_dict(kwds['A'], orient='index')
            dfB = pd.DataFrame.from_dict(kwds['B'], orient='index')
        if operationType == "Addition":
            data = dfA + dfB
        elif operationType == "Subtraction":
            data = dfA - dfB
        elif operationType == "Multiplication":
            data = dfA * dfB
        elif operationType == "Division":
            data = dfA / dfB
        result = data.to_dict()
        return {'output': result}
    
class MissingDataNode(CtrlNode):
    "imputates or drops missing values"
    nodeName = 'MissingDataNode'
    uiTemplate = [
        ('handle_NAs',  'combo', {'values': ["imputate","drop"], 'index': 0}),
        ('imputation_method',  'combo', {'values': ["mean","median","null"], 'index': 0})]
    
    def __init__(self, name):
        terminals={'data':{'io':'in'},'output':{'io':'out'}}
        CtrlNode.__init__(self, name, terminals=terminals)
           
    def process(self, **kwds):
        approach = str(self.ctrls['handle_NAs'].currentText())
        self.rename(approach + " missing values")
        self.graphicsItem().setPen()
        self.graphicsItem().nameItem.setPlainText(self._name)
        try:
            df = pd.DataFrame.from_dict(kwds['data'])
        except:
            df = pd.DataFrame.from_dict(kwds['data'],orient='index')
        if  approach == "imputate":
            imputate_meth = str(self.ctrls['imputation_method'].currentText())
            if imputate_meth == "mean":
                data = df.fillna(df.mean())
            elif imputate_meth == "median":
                data = df.fillna(df.median())
            elif imputate_meth == "null":
                data = df.fillna(0)
        elif  approach == "drop":
            data = df.dropna()
        result = data.to_dict()
        return {'output': result}
    
class LinePlotWidgetNode(CtrlNode):
    "custom dual input PlotWidet"
    nodeName = 'LinePlotWidget'
    sigPlotChanged = QtCore.Signal(object)
    uiTemplate = [
        ('plot_type',  'combo', {'values': ["Lineplot","Barchart","Scatterplot"], 'index': 0}),]

    def __init__(self, name):
        terminals = {'X': {'io':'in'},'Y':{'io':'in'}}
        CtrlNode.__init__(self, name, terminals=terminals)
        self.plot = None

    def setPlot(self, plot):
        if plot == self.plot:
            return
        if self.plot is not None:
             self.plot.clear()

        self.plot = plot
        self.update()
        self.sigPlotChanged.emit(self)
        
    def process(self, X, Y, display=True):
        plot_type = str(self.ctrls['plot_type'].currentText())
        self.rename(plot_type + " Widget")
        self.graphicsItem().setPen()
        self.graphicsItem().nameItem.setPlainText(self._name)

        if X and Y and display and self.plot is not None:
            df1 = pd.DataFrame.from_dict(X,orient='index')
            df2 = pd.DataFrame.from_dict(Y,orient='index')
            if df1.empty == False and df2.empty == False:
                xData = np.concatenate(df1.to_numpy(),axis=0).tolist()
                yData = np.concatenate(df1.to_numpy(),axis=0).tolist()
                self.plot.clear()
                if plot_type == "Lineplot":
                    plot = PlotDataItem(x=xData,y=yData)
                elif plot_type == "Barchart":
                    plot = BarGraphItem(x=xData, width=10/len(xData), height=yData)
                elif plot_type == "Scatterplot":
                    plot = ScatterPlotItem(xData, yData)
                self.plot.addItem(plot)

class HistogramWidgetNode(CtrlNode):
    "custom single input PlotWidget"
    nodeName = 'HistogramWidget'
    sigPlotChanged = QtCore.Signal(object)
    uiTemplate = [
        ('plot_type',  'combo', {'values': ["Histogram","SimpleLineplot"], 'index': 0}),]

    def __init__(self, name):
        terminals = {'X':{'io':'in'}}
        CtrlNode.__init__(self, name, terminals=terminals)
        self.plot = None

    def setPlot(self, plot):
        if plot == self.plot:
            return
        if self.plot is not None:
             self.plot.clear()

        self.plot = plot
        self.update()
        self.sigPlotChanged.emit(self)
        
    def process(self, X, display=True):
        plot_type = str(self.ctrls['plot_type'].currentText())
        self.rename(plot_type + " Widget")
        self.graphicsItem().setPen()
        self.graphicsItem().nameItem.setPlainText(self._name)

        if X and display and self.plot is not None:
            df = pd.DataFrame.from_dict(X,orient='index')
            if df.empty == False:
                inputData = np.concatenate(df.to_numpy(),axis=0).tolist()
                x_data = [x for x in inputData]
                y_data = [inputData.count(x) for x in inputData]

                self.plot.clear()
                if plot_type == "SimpleLineplot":
                    plot = PlotDataItem(inputData)
                elif plot_type == "Histogram":
                    plot = BarGraphItem(x=x_data, width=10/len(x_data), height=y_data)
                self.plot.addItem(plot)