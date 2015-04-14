from models import *


def gettingNotes():
    notes = Notes.Query.all()

    return notes

def notesImages(objectID):
    notes = Notes.Query.get(objectId=objectID)

    return notes