
"""
Created on Wed Jul 22 21:54:12 2020

@author:Supernowae
"""

# Here is a dictionary of player names that seem to be written in different ways
names_to_correct={
 'Bautista R.':'Bautista Agut R.',
 'Bogomolov Jr. A.':'Bogomolov A.',
 'Bogomolov Jr.A.':'Bogomolov A.',
 'Carreno-Busta P.': 'Carreno Busta P.',
 'Chela J.':'Chela J.I.',
 'Del Potro J.': 'Del Potro J.M.',
 'Del Potro J. M.':'Del Potro J.M.',
 'Dutra Da Silva R.': 'Dutra Silva R.',
 'Ferrero J.':'Ferrero J.C.',
 'Gambill J. M.':'Gambill J.M.',
 'Haider-Mauer A.':'Haider-Maurer A.',
 'Hantschek M.':'Hantschk M.',
 'Herbert P.H':'Herbert P.H.',
 'Lisnard J.':'Lisnard J.R.',
 'Lu H.':'Lu Y.H.',
 'Marin J.A':'Marin J.A.',
 'Munoz De La Nava D.':'Munoz-De La Nava D.',
 'Nadal-Parera R.':'Nadal R.',
 'Querry S.':'Querrey S.',
 'Ramirez Hidalgo R.': 'Ramirez-Hidalgo R.',
 'Ramos A.':'Ramos-Vinolas A.',
 'Stebe C-M.':'Stebe C.M.',
 'De Voest R.':'de Voest R.',
 'De Chaunac S.':'de Chaunac S.',
 'Di Mauro A.':'di Mauro A.',
 'Di Pasquale A.':'di Pasquale A.',
 'Van Lottum J.':'van Lottum J.'
}


# There are several Kuznetsov: Alex, Andrey and Artem


# sorted(list(data.Winner.unique()))

def namelist(data):
    '''
    This function returns the contained player names of the column 'Winner'
    to have a look on. I don't assume that there are such bugs of players that only loose.
    Check the amount of occurencies with 'name_occur' or 'name_occur2'
    '''
    return sorted(list(data.Winner.unique()))

def name_occur(data, name):
    '''
    This function just prints how often the given name occurs 
    in the 'Winner' and the 'Loser' column
    '''
    print(f'In Winner the name occurs: {data.ATP[data.Winner == name].count()} times')
    print(f'In Loser the name occurs:  {data.ATP[data.Loser == name].count()} times')

def name_occur2(data,name, name2):
    '''
    This function prints the occurencies of the given names to decide which 
    one to put in the dict for correction and in which order.
    '''
    occ1w = data.ATP[data.Winner == name].count()
    occ1l = data.ATP[data.Loser == name].count()
    occ2w = data.ATP[data.Winner == name2].count()
    occ2l = data.ATP[data.Loser == name2].count()    
    
    print(f'In Winner the first name occurs:  {occ1w} times')
    print(f'In Loser the first name occurs:   {occ1l} times')
    print(f'In Winner the second name occurs: {occ2w} times')
    print(f'In Loser the second name occurs:  {occ2l} times\n')
    print('-----------------------------------------------------------------')
    print(f'In total the first name occurs:   {occ1w + occ1l} times')
    print(f'In total the second name occurs:  {occ2w + occ2l} times')

# ToDo: A function that outputs a list of suspected Names where to look on.
# A very good function would be checked and sycronized with tennisabstract.com 
# to have an unique name and maybe also the link to the current data for scarping e.g.
# 