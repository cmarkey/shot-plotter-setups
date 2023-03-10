import os
import random
import re
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
from hockey_rink import NHLRink
import glob
import os.path
import numpy as np
from cycler import cycler
import matplotlib.patches as patches
import matplotlib
from matplotlib import rc
import numpy as np
import scipy.misc
from scipy import ndimage
from sklearn.linear_model import LinearRegression

MY_DPI = 96*1.40
#IMG_WIDTH = 490*1.40
#IMG_HEIGHT = 440*1.40
cougars = sb.diverging_palette(150, 275, n=10, s=60, l=55)
cougars
plt.rcParams["font.family"] = "Consolas"

#import all files
path = r'C:/Users/carli/Documents/Hockey Research/Chatham/Passing Data' # use your path
all_files = glob.glob(path + "/*.csv")

list = []

for filename in all_files:
    print(filename)
    df = pd.read_csv(filename, index_col=None, header=0)
    list.append(df)

centering_passes = pd.concat(list, axis=0, ignore_index=True).drop(columns=['X2.1','Y2.1'])
centering_passes.loc[(centering_passes['Centering Pass'] == 'Not Attempted - Missed'), 'Centering Pass'] = 'Attempted - Missed'
centering_passes
centering_passes = centering_passes[((centering_passes['Y2'] < 25) & (centering_passes['Y2'] > -25) ) & ((centering_passes['X2'] > 55) & (centering_passes['X2'] > -55) )]
centering_passes[['X','X2']] = np.abs(centering_passes[['X','X2']])
centering_passes
lv_cp = centering_passes.loc[:(105+56)]
al_cp = centering_passes.loc[(105+57):]
lv_cp.columns
al_cp

cp_types = np.sort(np.unique(centering_passes['Centering Pass']))
cp_types
tot_percentages = np.zeros(shape=[len(cp_types)])
lv_percentages = np.zeros(shape=[len(cp_types)])
alv_percentages = np.zeros(shape=[len(cp_types)])
#percentage breakdowns
for i in range(len(cp_types)):
    lv_percentages[i] = len(lv_cp[lv_cp['Centering Pass'] == cp_types[i]])/len(lv_cp)*100
    alv_percentages[i] = len(al_cp[al_cp['Centering Pass'] == cp_types[i]])/len(al_cp)*100
    tot_percentages[i] = len(centering_passes[centering_passes['Centering Pass'] == cp_types[i]])/len(centering_passes)*100
print(cp_types)
print(lv_percentages)
print(alv_percentages)
print(tot_percentages)

#plot where missed passes are trying to be recieved
fig, ax = plt.subplots(1, 1, sharey=True, dpi=MY_DPI)
rink = NHLRink(rotation=90)
ax = rink.draw(display_range="ozone")
rotated_x, rotated_y = rink.convert_xy(centering_passes.loc[centering_passes['Centering Pass'] == 'Attempted - Missed','X'], centering_passes.loc[centering_passes['Centering Pass'] == 'Attempted - Missed','Y'])
arrows = rink.arrow(centering_passes.loc[centering_passes['Centering Pass'] == 'Attempted - Missed','X'], centering_passes.loc[centering_passes['Centering Pass'] == 'Attempted - Missed','Y'],
                    centering_passes.loc[centering_passes['Centering Pass'] == 'Attempted - Missed','X2'], centering_passes.loc[centering_passes['Centering Pass'] == 'Attempted - Missed','Y2'], color="black",alpha=.15)

sb.kdeplot(x=rotated_x, y=rotated_y, fill=True, cmap='Purples', bw=.2)
transform = rink._get_transform(ax=ax)
constraint = rink._add_boards_constraint(ax=ax, transform=transform)
for col in ax.collections:
    col.set_clip_path(constraint)

watermark = "Created by Carleen Markey (@quarkyhockey) for Chatham Women's Hockey"
plt.text(-46,27,watermark,size=5, rotation=90)
notes = "Arrows point from decision-making player\nto where player was open to recieve centering pass.\nPurple spots are stronger where more CPs could've come from"
plt.text(0,20,notes,size=8,va='center',ha='center',zorder=105,color='dimgrey')
title = 'Decision-maker Locations - \nCentering Pass Attempted + Missed'
plt.title(title,y=1.05,size=15, va='center',ha='center',weight='bold',zorder=105)

plt.savefig('C:/Users/carli/Documents/Hockey Research/Chatham/missed_cp.png')

#plot where not attempted passes are starting from
fig, ax = plt.subplots(1, 1, sharey=True, dpi=MY_DPI)
rink = NHLRink(rotation=90)
ax = rink.draw(display_range="ozone")
selection = centering_passes[(centering_passes['Centering Pass'] == 'Not Attempted - Shot Taken')]
rotated_x, rotated_y = rink.convert_xy(selection['X'], selection['Y'])
selection
sb.kdeplot(x=rotated_x, y=rotated_y, fill=True, cmap='Purples', bw=.2)
transform = rink._get_transform(ax=ax)
constraint = rink._add_boards_constraint(ax=ax, transform=transform)
arrows = rink.arrow(selection['X'], selection['Y'],
                    selection['X2'], selection['Y2'], color="black",alpha=.1)

for col in ax.collections:
    col.set_clip_path(constraint)

watermark = "Created by Carleen Markey (@quarkyhockey) for Chatham Women's Hockey"
plt.text(-46,27,watermark,size=5, rotation=90)
notes = "Arrows point from decision-making player\nto where player was open to recieve centering pass.\nPurple spots are stronger where more CPs could've come from"
plt.text(0,20,notes,size=8,va='center',ha='center',zorder=105,color='dimgrey')
title = 'Decision-maker Locations - \nShot Taken instead of CP'
plt.title(title,y=1.05,size=15, va='center',ha='center',weight='bold',zorder=105)

plt.savefig('C:/Users/carli/Documents/Hockey Research/Chatham/not_attempted_st_cp.png')


fig, ax = plt.subplots(1, 1, sharey=True, dpi=MY_DPI)
rink = NHLRink(rotation=90)
ax = rink.draw(display_range="ozone")
centering_passes[(centering_passes['X2'] < 50)]
selection = centering_passes[(centering_passes['Centering Pass'] == 'Not Attempted - Low Danger Pass')]
rotated_x, rotated_y = rink.convert_xy(selection['X'], selection['Y'])

sb.kdeplot(x=rotated_x, y=rotated_y, fill=True, cmap='Purples', bw=.2)
transform = rink._get_transform(ax=ax)
arrows = rink.arrow(selection['X'], selection['Y'],
                    selection['X2'], selection['Y2'], color="black",alpha=.1)

constraint = rink._add_boards_constraint(ax=ax, transform=transform)
for col in ax.collections:
    col.set_clip_path(constraint)

watermark = "Created by Carleen Markey (@quarkyhockey) for Chatham Women's Hockey"
plt.text(-46,27,watermark,size=5, rotation=90)
notes = "Arrows point from decision-making player\nto where player was open to recieve centering pass.\nPurple spots are stronger where more CPs could've come from"
plt.text(0,20,notes,size=8,va='center',ha='center',zorder=105,color='dimgrey')
title = 'Decision-maker Locations - \nLow Danger Pass instead of CP'
plt.title(title,y=1.05,size=15, va='center',ha='center',weight='bold',zorder=105)

plt.savefig('C:/Users/carli/Documents/Hockey Research/Chatham/not_attempted_ldp_cp.png')


#plot successful centering passes
fig, ax = plt.subplots(1, 1, sharey=True, dpi=MY_DPI)
rink = NHLRink(rotation=90)
ax = rink.draw(display_range="ozone")
selection = centering_passes[(centering_passes['Centering Pass'] == 'Successful')]
len(selection)
len(selection['X'])
len(selection['Y'])


rotated_x, rotated_y = rink.convert_xy(selection['X'], selection['Y'])
sb.kdeplot(x=rotated_x, y=rotated_y, fill=True, cmap='Purples', bw=.2)
transform = rink._get_transform(ax=ax)
arrows = rink.arrow(selection['X'], selection['Y'],
                    selection['X2'], selection['Y2'], color="black",alpha=.1)

constraint = rink._add_boards_constraint(ax=ax, transform=transform)
for col in ax.collections:
    col.set_clip_path(constraint)

arrows = rink.arrow(selection['X'], selection['Y'],
                    selection['X2'], selection['Y2'], color="black",alpha=.15)

watermark = "Created by Carleen Markey (@quarkyhockey) for Chatham Women's Hockey" # your watermark
plt.text(-46,27,watermark,size=5, rotation=90)
notes = "Arrows point from decision-making player\nto where player was open to recieve centering pass.\nPurple spots are stronger where more CPs could've come from"
plt.text(0,20,notes,size=8,va='center',ha='center',zorder=105,color='dimgrey')
title = 'Decision-maker Locations - \nSuccessful Centering Passes'
plt.title(title,y=1.05,size=15, va='center',ha='center',weight='bold',zorder=105)

plt.savefig('C:/Users/carli/Documents/Hockey Research/Chatham/sucessful_centering_pass.png') #your save file
