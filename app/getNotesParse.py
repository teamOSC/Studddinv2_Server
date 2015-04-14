from models import *


def gettingNotes():
    return Notes.Query.all()[0].notesImages[0]['url']
    #print type(Notes.Query.all()[0].notesImages[0])