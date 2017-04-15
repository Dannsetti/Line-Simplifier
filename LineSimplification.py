'''
Daniel Sette

MSc IT

Submission date 01/04/2017

'''

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


from GUIconnection import GUIconnection
from Pt import Pt


from Distance import Distance
from nthPoint import nthPoint

from collections import OrderedDict
import csv




METHODS = {}   # Dict to store the methods triggerd by the process button

## LineSimplification is framework that prints out a draw in the canvas using
# the given coordinates list. 
# 
class LineSimplification(Frame):

    def __init__(self, master = None, **kwargs):
        
        
        ttk.Frame.__init__(self,master, **kwargs, relief=SUNKEN)
        self.master.resizable(False, False)
        self.master.title("Line Simplification")
        self.grid()

        self._coordinatesXY = []   # List of x and y coordinates used in many functions

        ## Method to open the file in the framework 
        #           
        def fileLoad(self, event = None):
            self.types = [('files', '*.csv'), ('All files', '*')]   # Only csv type is accepted
            dialog = filedialog.Open(self, filetypes = self.types)
            infile = dialog.show()
            # call check convertToDict method to get the file content
            convertToDict(self, infile)
                       
        ## Method to read the file content and convert it into a dictionary
        # 
        def convertToDict(self, infile):
            coordinatesDict = {}
            infile = open(infile, "r")
            for line in infile:
                # Adds line to dict 
                key, x, y = line.strip().split(',')
                coordinatesDict[key] = x, y
                
            # Convert dict key into int    
            intKeyDict = dict((int(k), v) for k, v, in coordinatesDict.items())
            
            infile.close()   # close

            # Check if dict is empty - handle empty csv files 
            if intKeyDict == {}:
                return None
            else:
                # Call method to sort the coordinates by its keys
                sortCoordinatesPoints(self, intKeyDict)

        ## Method to sort the dictionary.
        # Convert values into float numbers.
        # Translate the y coods and scale x and y to fit into the Canvas.
        # And check if the coords were scaled before. 
        #
        def sortCoordinatesPoints(self, intKeyDict):
            coordinatesX = []
            coordinatesY = []
        
            # Sort the dict by its key 
            sortedCoordinates = OrderedDict(sorted(intKeyDict.items()))
            
            # Empty values at key 1 was a solution that I used to distinguish
            # the program previously saved coords so that do not need to be scalled again
            if sortedCoordinates[1] == ('',''):
                
                savedBefore(self, sortedCoordinates)

            else:
                # Convert values into float
                for items in sortedCoordinates.items():
                    x, y = items[1]
                    coordinatesX.append(float(x))
                    # Iterate through y coords multiplying by -1 to print in the right position
                    coordinatesY.append(float(y) * -1) 

                # Scale X and Y separately and join them in one list
                coordinatesX = scaleToCanvas(self, coordinatesX)
                coordinatesY = scaleToCanvas(self, coordinatesY)
                
                self._coordinatesXY = zip(coordinatesX, coordinatesY)

                printDraw(self, self._coordinatesXY) # Finally call method that prints the points of the returned list
                
        ## Scale x and y coords to fit the canvas
        # Used @sortCoordinatesPoints method
        #
        def scaleToCanvas(self, coordinates):
            convertedCoords = []
            minimum = min(coordinates)
            maximum = max(coordinates)
            for coord in coordinates:
                convertedCoords.append((coord - (minimum - 0.2)) * (380 / (maximum -minimum)))
            return(convertedCoords)

        ## Method to print the given points
        # @try checks if it is not empty and print the lines
        # @except return none
        #
        def printDraw(self, coordinates):
            self.canvas.delete("all")   # Erase actual prints
            try:
                if coordinates != []:
                    self._coordinatesXY = list(coordinates)
                    self.canvas.create_polygon(self._coordinatesXY, fill='', outline='black') # test
            except Exception:
                return None
                
        ## Method that save the file by converting the list into a dict
        #  and write the content on a CSV file.
        #
        def saveFile(self, event=None):
            coordsDct = {}
            key = 1
            coordsDct[key] = None, None     # Trick used to tag that it was saved before
            key = 2
            for coords in self._coordinatesXY:
                # Get the line and add to the dict
                coordsDct[key] = coords
                key += 1

            outfile = filedialog.asksaveasfilename(defaultextension=".csv")
            # It is used for handling a cancellation
            if not outfile:
                return None
            else:
                with open(outfile, 'w') as file:
                    wFile = csv.writer(file)
                    for key, value in coordsDct.items():
                        wFile.writerow([key, value[0], value[1]])
                    
        ## Get the dict convert the values into float and join the coords in one file
        # Then prints it out
        #
        def savedBefore(self, coordsDict):
            cX = []
            cY = []
            for items in coordsDict.items():
                if items[1] != ('',''):   # used to not get the none values 
                    x, y = items[1]
                    cX.append(float(x))
                    cY.append(float(y))
            self._coordinatesXY = zip(cX, cY)

            printDraw(self, self._coordinatesXY)

            
        ## Menu bar
        #  Crete the menubar tab
        #
        def menuBar(self):
            self.option_add('*tearOff', FALSE)
            self.menubar = Menu(master)

            self.file = Menu(self.menubar, name = 'file')
            self.menubar.add_cascade(label="File", menu=self.file)
            self.file.add_command(label="Load...", accelerator = "Command-L", command = lambda: fileLoad(self))
            self.file.add_separator()
            self.file.add_command(label="Save", accelerator = "Command-S", command = lambda: saveFile(self))
            self.master['menu'] = self.menubar
            self.menubar.bind('<Command-l>', lambda: fileLoad(self))
            self.menubar.bind('<Command-s>', lambda: saveFile(self))
        
        ## Label placed on the top left corner
        #
        def fixedLabel(self):
            self.fixedLabel = ttk.Label(self, text = "Select Method:")
            self.fixedLabel.grid(row = 0, column = 0, padx = 7)

        ## List box containing the program methods
        # @item check if the selected and trigger operation
        #
        def methodsListbox(self):
            self.modeSelection = Listbox(self, selectmode=SINGLE, width=10,height=3)
            self.modeSelection.grid(row = 0, column = 1)

            lst = []
            infile = open('plugins.txt', 'r')
            for line in infile:
                line = line.split()
                if line[0] >= "A" and line[0] <= "Z" or line[0] >= "a" and line[0] <= "z":
                    lst.append(line)
            for item in lst:
                if item == ['Distance']:
                    METHODS['Distance'] = callDistanceMethod # Append to Methods dict to be triggered by the button
                    mode = Distance.displayName(self)        # Event to get the method name
                    self.modeSelection.insert(0, mode)       # Insert in the listbox
                
                if item == ['nthPoint']:
                    METHODS['nthpoint'] = callNthPointMethod # Append to Methods dict to be triggered by the button
                    mode = nthPoint.displayName(self)        # Event to get the method name
                    self.modeSelection.insert(1, mode)       # Insert in the listbox
                    
            
            infile.close()
            
            # Selection event triggers the function that sets the next label 
            mutableLabel(self, self.modeSelection)

        
        ## Instantiate the mutable label
        # @bind event triggers the method to change label content
        #
        def mutableLabel(self, modeSelection):
            self.modeSelection.labelText = StringVar()
            self.mutableLabel = ttk.Label(self, textvariable = self.modeSelection.labelText, width = 10, anchor='e') # anchor 'e' to align text on the right side
            self.mutableLabel.grid(row = 0, column = 2)
            self.modeSelection.bind('<<ListboxSelect>>', lambda event: changeLabel(event))
        
        ## Method triggered by list box selection event
        # @index calls the related function to set the mutable label
        #
        def changeLabel(self):
            widget = self.widget
            index = widget.curselection()[0]
            
            if index == 0:
                Distance.displayParameterName(self, widget)
                
            elif index == 1:
                nthPoint.displayParameterName(self, widget)

        ## Instantiate the Entry box to get the user input
        #
        def entryBox(self):
            #Entry box
            self.entryBox = ttk.Entry(self, text = "", width = 7)
            self.entryBox.grid(row = 0, column = 3)
        
        ## Instantiate Process button to execute the line simplification methods
        # @command button triggers getMethod function
        #
        def button(self): 
           
            self.processButton = ttk.Button(self, text = "Process", command= lambda: getMethod(self))
            self.processButton.grid(row = 0, column = 4, padx = 7)

        ## Method triggered by the button
        # Gets the user input.
        # Gets the mode selected in the list box and call the appropriate method passing the input as argument
        # @Exception if nothing if no method were selected pops up an warning message
        #
        def getMethod(self):
            try:
                self.value = self.entryBox.get()
                selection = self.modeSelection.get(self.modeSelection.curselection())
                method = METHODS[selection]
                method(self.value)
            except Exception:
                warningMessage(self)
            
        ## Method to trigger and pass the arguments to Distance line simplification method
        #
        def callDistanceMethod(args):
            newList = Distance.thinPoints(self, self._coordinatesXY, self.value)
            self._coordinatesXY = newList
            printDraw(self, self._coordinatesXY)

        ## Method to trigger and pass the arguments to nthpoint line simplification method
        #            
        def callNthPointMethod(args):
            newList = nthPoint.thinPoints(self, self._coordinatesXY, self.value)
            self._coordinatesXY = newList
            printDraw(self, self._coordinatesXY)

        ## Warning message pop up window
        #
        def warningMessage(self):
            messagebox.showinfo("Warning", "Must Select a Method")
        
        ## Instantiate Canvas
        #           
        def canvas(self):
            self.canvas = Canvas(self, width =400, height=400)
            self.canvas.grid(row = 1, columnspan = 5)

        ## Builds the framework when it is started
        #
        def framework(self):
            menuBar(self)
            fixedLabel(self)
            methodsListbox(self)
            entryBox(self)
            button(self)
            canvas(self)

        framework(self)

if __name__ == "__main__":
    LineSimplification().mainloop()
    
