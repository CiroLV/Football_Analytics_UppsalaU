#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 15:38:39 2020

@author: ciro
"""

#Load in Statsbomb competition and match data
#This is a library for loading json files.
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas import json_normalize

#Load the competition file
#Got this by searching 'how do I open json in Python'
with open('Statsbomb/data/competitions.json') as f:
    competitions = json.load(f)
    
#Womens World Cup 2019 has competition ID 72
#competition_id=72
#Men's world cup
competition_id=43

#Load the list of matches for this competition
with open('Statsbomb/data/matches/'+str(competition_id)+'/3.json') as f:
    matches = json.load(f)
    
#South Korea matches
team_name_req="South Korea"

#Find ID for the match
for match in matches:
    home_team_name=match['home_team']['home_team_name']
    away_team_name=match['away_team']['away_team_name']
    if (home_team_name==team_name_req) or (away_team_name==team_name_req):
        match_id_required = match['match_id']
        print(home_team_name + ' vs ' + away_team_name + ' has id:' + str(match_id_required))

        
#Size of the pitch in yards (!!!)
pitchLengthX=120
pitchWidthY=80

#ID for England vs Sweden Womens World Cup
match_ids_required = 7567 #[7538,7553,7567]
# dfs = []
matchid = 7567
# Load in the data
# I took this from https://znstrider.github.io/2018-11-11-Getting-Started-with-StatsBomb-Data/
# for matchid in match_ids_required:    
file_name=str(matchid)+'.json'

#Load in all match events 
#import json
with open('Statsbomb/data/events/'+file_name) as data_file:
    
        #print (mypath+'events/'+file)
    data = json.load(data_file)

#get the nested structure into a dataframe 
#store the dataframe in a dictionary with the match id as key (remove '.json' from string)
#from pandas import json_normalize
df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])
# dfs.append(df)
# print(dfs[len(dfs)-1].shape)

# for df in dfs[0]:
    # df = dfs[0]
    # matchid = df['match_id'].unique()[0]
# for match in matches:
#     if match['match_id']== matchid:
#         home_team_name=match['home_team']['home_team_name']
#         away_team_name=match['away_team']['away_team_name']          
#            if (home_team_name == team_name_req):

#A dataframe of shots
shots = df.loc[df['type_name'] == 'Shot'].set_index('id')
   
#Draw the pitch
from FCPython import createPitch
(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')

#Plot the shots
for i,shot in shots.iterrows():
    x=shot['location'][0]
    y=shot['location'][1]
    
    goal=shot['shot_outcome_name']=='Goal'
    team_name=shot['team_name']
                    
    circleSize=2
  # circleSize=np.sqrt(shot['shot_statsbomb_xg']*15)

    if (team_name==team_name_req):
        if goal:
            shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="red")
            plt.text((x-10),pitchWidthY-y+1,shot['player_name']) 
        else:
            shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="red")     
            shotCircle.set_alpha(.2)
    elif (team_name!=team_name_req):
        continue
        # if goal:
        #     shotCircle=plt.Circle((pitchLengthX-x,y),circleSize,color="blue") 
        #     plt.text((pitchLengthX-x+1),y+1,shot['player_name']) 
        # else:
        #     shotCircle=plt.Circle((pitchLengthX-x,y),circleSize,color="blue")      
        #     shotCircle.set_alpha(.2)

    ax.add_patch(shotCircle)
    
            
plt.text(80,75,team_name_req + ' shots vs Germany') 

fig.set_size_inches(10, 7)
fig.savefig('Output/South_Korea_shots_vsGermany.pdf', dpi=300) 
plt.show()

#1, Create a dataframe of passes which contains all the passes in the match
passes = df.loc[df['type_name'] == 'Pass'].set_index('id')
(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')
#2, Plot the start point of every Sweden pass. Attacking left to right.
#Plot the passes
for i,thepass in passes.iterrows():
    if thepass['player_name']=='Heung-Min Son':
        x=thepass['location'][0]
        y=thepass['location'][1]
        circleSize=2
        
        passCircle = plt.Circle((pitchLengthX-x,y),2,color="blue")
    
        passCircle.set_alpha(.2)
        ax.add_patch(passCircle)
        
        dx = thepass["pass_end_location"][0]-x
        dy = thepass["pass_end_location"][1]-y
        passArrow=plt.Arrow(pitchLengthX-x,y,dx,dy,width=3,color='blue')
        ax.add_patch(passArrow)


plt.text(20,75,'Heung-Min Son passes vs Germany') 
fig.set_size_inches(10, 7)
fig.savefig('Output/Heung-Min_Son_passes_vsGermany.pdf', dpi=300) 
plt.show()   














