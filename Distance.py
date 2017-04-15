'''
Daniel Sette

MSc IT

Submission date 01/04/2017

'''

from GUIconnection import GUIconnection
from Pt import Pt


## Class inherited by Line Simplification.
# Executes the events of the main file.
# And the method to handle the line simplification.
#
class Distance(GUIconnection):


     ## Method to setup the name a the list box
     # @return name is placed
     #
     def displayName(self):
         return("Distance")


     ## Method to set the content of label in the line simplification class
     #
     def displayParameterName(self, widget):
          widget.labelText.set('min distance')


     ## Method that operates the distance line simplification method.
     # Gets two arguments and self - pts is the coordinates list, param is the user input.
     # Handles bad input in the entry box such as string.
     # Handles also empty coords lists. 
     # @return new list of coordinates is sent to be displayed in the canvas
     #
     def thinPoints(self, pts, param):
          minDistance = param
          try:
               if minDistance:
                    minDistance = float(minDistance)
          except Exception:        # if input is not a number convert to 0.01 
               minDistance = 0.01

          # to handle empty lists
          if pts == []:
               return pts
          else:
               # execute the distance simplification method as specified.
               
               lastPoint = pts[0]         # Last point equal first tuple
               lastPointX = lastPoint[0]  # get x
               lastPointY = lastPoint[1]  # get y

               # call Pt class passing x and y
               LastKeptPoint = Pt(lastPointX, lastPointY)

               newCoordsList = []
               newCoordsList.append(lastPoint)   # New list append the first point

               # Iterate through the given lists to get the currents points
               for i in range(1, len(pts)):
                    current = pts[i]
                    pointX = pts[i][0]
                    pointY = pts[i][1]
                    currentPoint = Pt(pointX, pointY)
                    # Calculate the distance using the Euclidean method
                    if currentPoint.EuclideanDistance(LastKeptPoint) < minDistance:
                         i += 1    # if distance between current and last kept point
                                   # is less than minDistance pass to the next point

                    else:          
                         newCoordsList.append(current) # Else add to the new list
                         LastKeptPoint = currentPoint  # and mark it as the last kept point
               return(newCoordsList)
