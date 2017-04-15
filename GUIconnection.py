
class GUIconnection:

    def displayName(self):
        #Use this to give the required name to the listbox
        raise NotImplementedError('displayName must be implemented by subclass')
        
    def displayParameterName(self):
        #Use this to update the label next to the entry box
        raise NotImplementedError('displayParameterName must be implemented by subclass')

    def thinPoints(self,pts,param):
        #Process Button should call this
        raise NotImplementedError('thinPoints must be implemented by subclass')

