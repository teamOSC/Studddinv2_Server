import random
import sqlite3
from scraper import DB

chanell_names = 'MIT:MIT,khanacademy:Khan Academy,nptelhrd:NPTEL HRD,1veritasium:Veritasium,vsauce:V-Sauce,CGPGrey:CGP Grey,minutephysics:Minute Physics,destinws2:destin WS,scishow:Sci Show,crashcourse:Crash Course,AsapSCIENCE:Asap Science,numberphile:Numberphile,TheBadAstronomer:The Bad Astronomer,ACDCLeadership:ACDC Leadership,arinjayjain1979:Arinjay Jain,smithsonianchannel:Smithsonian Channel,historychannel:History Channel,periodicvideos:Periodic Videos,sixtysymbols:Sixty Symbols,Computerphile:Computerphile,FavScientist:Fav Scientist,coursera:Coursera,TEDxTalks:TedxTalks,bkraz333:BkRaz333,virtualschooluk:Virtual School UK,SpaceRip:Space RIP,bozemanbiology:BozeMan Biology,MindsetLearn: Mindset Learn,Mathbyfives:Math by Fives,jayates79:JayaTes79,MathTV:MathTV'

chanell_names = chanell_names.split(",")
ls = []
for i in chanell_names:
    x = i.split(":")
    #print x[0]
    ls.append(x[0])

print ls

'''for i in range(1):
    q = random.choice(ls)
    print q
    print DB.search(q)'''
for i in range(5):
    q = random.choice(ls)
    print q
    foo = DB.search(q)
    #print foo
    bar = random.choice(foo)
    print bar[2]