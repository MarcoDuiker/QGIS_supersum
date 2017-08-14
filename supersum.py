##clip_layer=optional vector
##filter_expression=optional string
##polygon=boolean True
##point=boolean True
##line=boolean True
##sum_expression=string
##selected_features_only=boolean True
##sum_total=output number
##sum_result_table=output table

from qgis._core import *
from qgis.utils import iface
from processing import *
import csv

# input validation
clip_lyr = None
if clip_layer:
    clip_lyr = getObject(clip_layer)
    if not clip_lyr.geometryType() == QGis.Polygon:
        raise GeoAlgorithmExecutionException("Clip layer must be of type Polygon")

filter_exp = False
if filter_expression:
    filter_exp = QgsExpression(filter_expression)
    if filter_exp.hasParserError():
        raise GeoAlgorithmExecutionException(filter_exp.parserErrorString()) 

sum_exp = QgsExpression(sum_expression)
if sum_exp.hasParserError():
    raise GeoAlgorithmExecutionException(sum_exp.parserErrorString())

# where filter function    
def where(layer, exp, selected_features_only):
    if selected_features_only:
        features = processing.features(layer)
    else:
        features = layer.getFeatures()    
    if exp:
        exp.prepare(layer.pendingFields())
    for feature in features:
        if exp:
            value = exp.evaluate(feature)
            if exp.hasEvalError():
                # raise GeoAlgorithmExecutionException(exp.evalErrorString())
                progress.setInfo('-->' + 'Warning: ' + exp.evalErrorString())
            if bool(value):
                yield feature
        else:
            yield feature

# main 
sum_result = {}
sum_total = 0

#loop al selected layers and sum using the sum expression skipping features with the where filter. Optionally clip first
for layer in iface.legendInterface().selectedLayers():
    if (layer.geometryType() == 2 and polygon) or (layer.geometryType() == 1 and line) or (layer.geometryType() == 1 and point):
        progress.setInfo('Processing layer: ' + layer.name() )
        sum_result[layer.name()] = 0
        if clip_lyr:
            result = processing.runalg('qgis:clip', layer, clip_lyr, None)
            layer_to_process = QgsVectorLayer(result["OUTPUT"],'layer_clipped',"ogr")
        else:
            layer_to_process = layer
        sum_exp.prepare(layer_to_process.pendingFields())
        for feat in where(layer_to_process, filter_exp, selected_features_only):
            value = sum_exp.evaluate(feat)
            if sum_exp.hasEvalError():
                #raise GeoAlgorithmExecutionException(sum_exp.evalErrorString())
                progress.setInfo('-->' + 'Warning: ' + sum_exp.evalErrorString())
            elif value:
                sum_total = sum_total + value
                sum_result[layer.name()] = sum_result[layer.name()] + value
        progress.setInfo('-->' + str(sum_result[layer.name()]) )
 
sum_result['Total'] = sum_total 

progress.setInfo('=============================+ ' )
progress.setInfo('Total sum: ' + str(sum_total) )
progress.setInfo(' ')

with open(sum_result_table, 'wt') as f:
    writer = csv.writer(f)
    writer.writerow( ('Layer', 'Sum') )
    for key, value in sum_result.items():
        writer.writerow((key,value))
