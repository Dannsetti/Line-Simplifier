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
class nthPoint(GUIconnection):


     ## Method to setup the name a the list box
     # @return name is placed
     #
     def displayName(self):
         return("nthpoint")

     ## Method to set the content of label in the line simplification class
     #
     def displayParameterName(self, widget):
          widget.labelText.set('n=')


     ## Method that operates the nthpoint line simplification method.
     # Gets two arguments and self - pts is the coordinates list, param is the user input.
     # Handles bad input in the entry box such as string.
     # Handles also empty coords lists. 
     # @return new list of coordinates is sent to be displayed in the canvas
     #
     def thinPoints(self,pts,param):
          n = param
          if pts == []: 
               return pts
          try:
               if n:
                    n = int(n)
          except ValueError:  # if input is not a number convert to 1 
               n = 1
               
          newCoordsList = []
          
          # Iterate through the pts list in stepping the lines by the user input
          # and add to the new list
          for i in pts[0::n]:   
               
               newCoordsList.append(i)
               
          return(newCoordsList)
               
