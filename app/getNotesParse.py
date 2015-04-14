from models import *


def gettingNotes():
    notes = Notes.Query.all()

    return notes

    #print type(Notes.Query.all()[0].notesImages[0])