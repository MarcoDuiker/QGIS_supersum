# Algorithm description
Supersum is a QGIS processing algorithm that sums an expression over all selected layers. 

Optionally the layers will first be clipped with a clip layer. Furthermore there is an option to filter the features by an expression or the type of the layer (point, line or polygon).

Expressions are the usual QGIS expressions.
# Input parameters
## clip layer
An optional layer to clip the features of the selected layers which will be summed.

Only features within the clip layer will be summed.
## filter expression
A valid QGIS expression evaluating to True or False. Only records where the filter expression evaluates to True will be summed.

Example: "Field name" = 'an interesting value'

Tip: Use one of the selected layers and build an expression with the expression builder in the field calculator. Copy and paste the expression in the filter expression field.

## polygon
When selected polygon layers will be summed.
## point
When selected point layers will be summed.
## line
When selected line layers will be summed.
## sum expression
A valid QGIS expression evaluating to a result which can be summed using the python + operator. Usually a float or an int will do.

Example: $area

Tip: Use one of the selected layers and build an expression with the expression builder in the field calculator. Copy and paste the expression in the sum expression field.
selected features only
# Outputs
## sum total
The grand total of the sum expression over all selected layers.
## sum result table
A table with layer names and the total of the sum expression for that layer.

Also a record with the grand total is included. 
