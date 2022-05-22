'''
An action consist of a trigger character, that is associated to a given function. So when in the game a user use a letter, the correct function can be called.
'''
import os

class Action():
    '''
    Create a new Action with a given triggering character and handler, description can be ommitted but is recommended
    '''

    def __init__(self, trigger, handler, description=""):
        self.trigger = trigger
        self.description = description
        self.handler = handler


'''
A list of Action
'''
def read_history(his):
    output = {}
    filepath = os.path.abspath('.')
    rootdir = os.path.join(filepath, his)
    lines = open(rootdir, 'r').readlines()
    for l in lines:
        l = l.strip()
        fields  = l.split(":")
        output[fields[0]] = fields[1]
    return output


class Actions():
    def __init__(self):
        self.actions = []

    '''
    Check if the given trigger exist ine the list
    '''

    def isPresent(self, trigger):
        for a in self.actions:
            if a.trigger == trigger:
                return True
        return False

    '''
    Add the provided action to the list if the trigger is not already used
    '''

    def addAction(self, action):
        if self.isPresent(action.trigger):
            return False

        self.actions.append(action)

    '''
    Return the handler associated with the provided trigger
    '''

    def getHandler(self, trigger):
        for a in self.actions:
            if trigger == a.trigger:
                return a.handler
        return None