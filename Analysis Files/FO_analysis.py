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

#rc('text',usetex=True)
MY_DPI = 96*1.40
#IMG_WIDTH = 490*1.40
#IMG_HEIGHT = 440*1.40
cougars = sb.diverging_palette(150, 275, n=10, s=60, l=55)
cougars[0][0]
#latex_pream = matplotlib.rcParams['text.latex.preamble']
#latex_pream.append(r'\usepackage{color}')
#latex_pream.append(r"\definecolor{g1}{rgb}{0.9,0.9,0.9}")
plt.rcParams["font.family"] = "Consolas"


wFOs = pd.read_csv('C:/Users/carli/Documents/Hockey Research/Chatham/Faceoff Data/wFOs.csv') #csv of won faceoffs
roster = pd.read_csv('C:/Users/carli/Documents/Hockey Research/Chatham/Chatham Roster 2021-22.csv') #csv of the roster
wFOs['Player'] = wFOs['Player'].astype(int)
wFOs['Picked Up By'] = wFOs[~(wFOs['Picked Up By'].isna())]['Picked Up By'].astype(int)
wFOs['FO Player'] = wFOs['Player']
wFOs.loc[wFOs['5 Sec Result '] == 'LOP','5 Sec Result '] = 'Loss of Possession'
wFOs.loc[wFOs['5 Sec Result '] == 'Skated around zone','5 Sec Result '] = 'Passing sequence'
wFOs['Chatham 5 Sec Result'] = wFOs['5 Sec Result ']
wFOs['Chatham 5 Sec Result'] = wFOs['5 Sec Result ']
print(roster.columns)

dFOs = wFOs[wFOs['Zone'] == 'Defensive'].reset_index()
oFOs = wFOs[wFOs['Zone'] == 'Offensive'].reset_index()
dFOs[['X', 'X2']] = np.abs(dFOs[['X', 'X2']])
oFOs[['X', 'X2']] = np.abs(oFOs[['X', 'X2']])
dx_coords = np.abs(np.array(dFOs[['X', 'X2']]).T)
dy_coords = np.abs(np.array(dFOs[['Y', 'Y2']]).T)
ox_coords = np.abs(np.array(oFOs[['X', 'X2']]).T)
oy_coords = np.abs(np.array(oFOs[['Y', 'Y2']]).T)

#dzone FO charts
for player in np.unique(dFOs['FO Player']):
    fo_data = dFOs[dFOs['FO Player'] == player].reset_index()
    if len(fo_data) > 5:
        fig, ax = plt.subplots(1, 1, sharey=True, dpi=MY_DPI)
        rink = NHLRink(x_shift=100, y_shift=42.5)
        ax = rink.draw(display_range="ozone")
        sb.scatterplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Dumped Out'], x="X2", y="Y2", color=cougars[0],s=100,zorder=101)
        sb.scatterplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Skated Out'], x="X2", y="Y2", color=cougars[3],s=100,zorder=101)
        sb.scatterplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Kept In'], x="X2", y="Y2", color=cougars[5],s=100,zorder=101)
        sb.scatterplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Loss of Possession'], x="X2", y="Y2", color=cougars[8],s=100,zorder=101)
        ax.invert_yaxis()
        for i in range(len(fo_data)):
            if fo_data['Picked Up By'].isna()[i] != True:
                ax.text(fo_data['X2'].iloc[i]+.4,fo_data['Y2'].iloc[i]-.4,str(int(fo_data['Picked Up By'].iloc[i])),size=8,zorder=102,c='black', weight='bold', va='center', ha='center',rotation=90)
        #sb.kdeplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Skated Out'], x="X2", y="Y2", bw_adjust=.5, cmap='Purples', shade=True, shade_lowest=False, alpha=0.7)
        #sb.kdeplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Dumped Out'], x="X2", y="Y2", bw_adjust=.5, cmap='Purples', shade=True, shade_lowest=False, alpha=0.7)
        watermark = "Created by Carleen Markey (@quarkyhockey) for Chatham Women's Hockey"
        plt.text(25,-45,watermark,size=5)
        notes = "Dots show puck pick up location after the FO.\nPlayer # shown in dot if Chatham player picked up puck."
        plt.text(118,0,notes,size=8,va='center',ha='center',rotation=90,zorder=105,color='dimgrey')
        player_name=roster.loc[(roster['Number']==player),'First Name'].to_string(index=False)+' '+roster.loc[(roster['Number']==player),'Last Name'].to_string(index=False)
        player_pos=roster.loc[(roster['Number']==player),'Position'].to_string(index=False)
        player_hand=roster.loc[(roster['Number']==player),'Handedness'].to_string(index=False)
        title = 'Results of D Zone FO won by\n'+str(player)+' '+str(player_name)+' ('+str(player_hand)+')' #add position and name
        print(title)
        plt.text(15,0, title, size=15, va='center',ha='center',weight='bold',rotation=90,zorder=105)
        im = plt.imread('C:/Users/carli/Documents/Hockey Research/Chatham/dFO_2col_legend.PNG')
        newax = fig.add_axes([.72,.22,.1,.55], anchor='C', zorder=101)
        rotated_img = ndimage.rotate(im, 90)
        newax.imshow(rotated_img)
        newax.axis('off')
        #fake_legend = 'Shot Attempt   Passing Sequence\nLoss of Possession'
        #plt.text(20,0, fake_legend, size=10, va='center',ha='center',rotation=270,zorder=105)
        #plt.legend().set_zorder(120)
        #plt.legend(bbox_to_anchor=(1.25,0),ncol=2)
        #plt.show()
        plt.savefig('C:/Users/carli/Documents/Hockey Research/Chatham/FO charts/dzone_center_'+player_name+'.png', facecolor='white',bbox_inches=matplotlib.transforms.Bbox([[1, .1], [5.2, 3.9]]))
        plt.clf()

for player in np.unique(dFOs['Picked Up By']):
    fo_data = dFOs[dFOs['Picked Up By'] == player].reset_index()
    if len(fo_data) > 5:
        fig, ax = plt.subplots(1, 1, sharey=True, dpi=MY_DPI)
        rink = NHLRink(x_shift=100, y_shift=42.5)
        ax = rink.draw(display_range="ozone")
        sb.scatterplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Dumped Out'], x="X2", y="Y2", color=cougars[0],s=100,zorder=101)
        sb.scatterplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Skated Out'], x="X2", y="Y2", color=cougars[3],s=100,zorder=101)
        sb.scatterplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Kept In'], x="X2", y="Y2", color=cougars[5],s=100,zorder=101)
        sb.scatterplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Loss of Possession'], x="X2", y="Y2", color=cougars[8],s=100,zorder=101)
        ax.invert_yaxis()
        for i in range(len(fo_data)):
            if fo_data['FO Player'].isna()[i] != True:
                ax.text(fo_data['X2'].iloc[i],fo_data['Y2'].iloc[i],str(int(fo_data['FO Player'].iloc[i])),size=8,zorder=102,c='black', weight='bold', va='center', ha='center',rotation=90)
        #sb.kdeplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Skated Out'], x="X2", y="Y2", bw_adjust=.5, cmap='Purples', shade=True, shade_lowest=False, alpha=0.7)
        #sb.kdeplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Dumped Out'], x="X2", y="Y2", bw_adjust=.5, cmap='Purples', shade=True, shade_lowest=False, alpha=0.7)
        watermark = "Created by Carleen Markey (@quarkyhockey) for Chatham Women's Hockey"
        plt.text(25,-45,watermark,size=5)
        notes = "Dots show puck pick up location after the FO.\nFO Player # shown in dot."
        plt.text(118,0,notes,size=8,va='center',ha='center',rotation=90,zorder=105,color='dimgrey')
        player_name=roster.loc[(roster['Number']==player),'First Name'].to_string(index=False)+' '+roster.loc[(roster['Number']==player),'Last Name'].to_string(index=False)
        player_pos=roster.loc[(roster['Number']==player),'Position'].to_string(index=False)
        player_hand=roster.loc[(roster['Number']==player),'Handedness'].to_string(index=False)
        title = 'Results of D Zone FO picked up\nby '+str(int(player))+' '+str(player_name)+' ('+str(player_hand)+')' #add position and name
        print(title)
        plt.text(15,0, title, size=15, va='center',ha='center',weight='bold',rotation=90,zorder=105)
        im = plt.imread('C:/Users/carli/Documents/Hockey Research/Chatham/dFO_2col_legend.PNG')
        newax = fig.add_axes([.72,.22,.1,.55], anchor='C', zorder=101)
        rotated_img = ndimage.rotate(im, 90)
        newax.imshow(rotated_img)
        newax.axis('off')
        #fake_legend = 'Shot Attempt   Passing Sequence\nLoss of Possession'
        #plt.text(20,0, fake_legend, size=10, va='center',ha='center',rotation=270,zorder=105)
        #plt.legend().set_zorder(120)
        #plt.legend(bbox_to_anchor=(1.25,0),ncol=2)
        #plt.show()
        plt.savefig('C:/Users/carli/Documents/Hockey Research/Chatham/FO charts/dzone_pu_'+player_name+'.png', facecolor='white',bbox_inches=matplotlib.transforms.Bbox([[1, .1], [5.2, 3.9]]))
        plt.clf()



#ozone FO charts
for player in np.unique(oFOs['FO Player']):
    fo_data = oFOs[oFOs['FO Player'] == player].reset_index()
    if len(fo_data) > 5:
        fig, ax = plt.subplots(1, 1, sharey=True, dpi=MY_DPI)
        rink = NHLRink(x_shift=100, y_shift=42.5)
        ax = rink.draw(display_range="ozone")
        sb.scatterplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Shot Attempt'], x="X2", y="Y2", color=cougars[0],s=100,zorder=101)
        sb.scatterplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Passing sequence'], x="X2", y="Y2", color=cougars[3],s=100,zorder=101)
        sb.scatterplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Loss of Possession'], x="X2", y="Y2", color=cougars[8],s=100,zorder=101)
        ax.invert_yaxis()
        for i in range(len(fo_data)):
            if fo_data['Picked Up By'].isna()[i] != True:
                ax.text(fo_data['X2'].iloc[i],fo_data['Y2'].iloc[i],str(int(fo_data['Picked Up By'].iloc[i])),size=8,zorder=102,c='black', weight='bold', va='center', ha='center',rotation=270)
        #sb.kdeplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Skated Out'], x="X2", y="Y2", bw_adjust=.5, cmap='Purples', shade=True, shade_lowest=False, alpha=0.7)
        #sb.kdeplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Dumped Out'], x="X2", y="Y2", bw_adjust=.5, cmap='Purples', shade=True, shade_lowest=False, alpha=0.7)
        watermark = "Created by Carleen Markey (@quarkyhockey) for Chatham Women's Hockey"
        plt.text(25,-45,watermark,size=5)
        notes = "Dots show puck pick up location after the FO.\nPlayer # shown in dot if Chatham player picked up puck."
        plt.text(8,0,notes,size=8,va='center',ha='center',rotation=270,zorder=105,color='dimgrey')
        player_name=roster.loc[(roster['Number']==player),'First Name'].to_string(index=False)+' '+roster.loc[(roster['Number']==player),'Last Name'].to_string(index=False)
        player_pos=roster.loc[(roster['Number']==player),'Position'].to_string(index=False)
        player_hand=roster.loc[(roster['Number']==player),'Handedness'].to_string(index=False)
        title = 'Results of O Zone FO won by\n'+str(player)+' '+str(player_name)+' ('+str(player_hand)+')' #add position and name
        print(title)
        plt.text(111,0, title, size=15, va='center',ha='center',weight='bold',rotation=270,zorder=105)
        im = plt.imread('C:/Users/carli/Documents/Hockey Research/Chatham/oFO_2col_legend.PNG')
        newax = fig.add_axes([.205,.18,.1,.65], anchor='C', zorder=107)
        rotated_img = ndimage.rotate(im, 270)
        newax.imshow(rotated_img)
        newax.axis('off')
        #fake_legend = 'Shot Attempt   Passing Sequence\nLoss of Possession'
        #plt.text(20,0, fake_legend, size=10, va='center',ha='center',rotation=270,zorder=105)
        #plt.legend().set_zorder(120)
        #plt.legend(bbox_to_anchor=(1.25,0),ncol=2)
        #plt.show()
        plt.savefig('C:/Users/carli/Documents/Hockey Research/Chatham/FO charts/ozone_center_'+player_name+'.png', facecolor='white',bbox_inches=matplotlib.transforms.Bbox([[.9, .1], [5.1, 3.9]]))
        plt.clf()

for player in np.unique(oFOs['Picked Up By']):
    fo_data = oFOs[oFOs['Picked Up By'] == player].reset_index()
    if len(fo_data) > 5:
        fig, ax = plt.subplots(1, 1, sharey=True, dpi=MY_DPI)
        rink = NHLRink(x_shift=100, y_shift=42.5)
        ax = rink.draw(display_range="ozone")
        sb.scatterplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Shot Attempt'], x="X2", y="Y2", color=cougars[0],s=100,zorder=101)
        sb.scatterplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Passing sequence'], x="X2", y="Y2", color=cougars[3],s=100,zorder=101)
        sb.scatterplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Loss of Possession'], x="X2", y="Y2", color=cougars[8],s=100,zorder=101)
        ax.invert_yaxis()
        for i in range(len(fo_data)):
            if fo_data['FO Player'].isna()[i] != True:
                ax.text(fo_data['X2'].iloc[i],fo_data['Y2'].iloc[i],str(int(fo_data['FO Player'].iloc[i])),size=8,zorder=102,c='black', weight='bold', va='center', ha='center',rotation=270)
        #sb.kdeplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Skated Out'], x="X2", y="Y2", bw_adjust=.5, cmap='Purples', shade=True, shade_lowest=False, alpha=0.7)
        #sb.kdeplot(data = fo_data[fo_data['Chatham 5 Sec Result'] == 'Dumped Out'], x="X2", y="Y2", bw_adjust=.5, cmap='Purples', shade=True, shade_lowest=False, alpha=0.7)
        watermark = "Created by Carleen Markey (@quarkyhockey) for Chatham Women's Hockey"
        plt.text(25,-45,watermark,size=5)
        notes = "Dots show puck pick up location after the FO.\nFO Player # shown in dot."
        plt.text(8,0,notes,size=8,va='center',ha='center',rotation=270,zorder=105,color='dimgrey')
        player_name=roster.loc[(roster['Number']==player),'First Name'].to_string(index=False)+' '+roster.loc[(roster['Number']==player),'Last Name'].to_string(index=False)
        player_pos=roster.loc[(roster['Number']==player),'Position'].to_string(index=False)
        player_hand=roster.loc[(roster['Number']==player),'Handedness'].to_string(index=False)
        title = 'Results of O Zone FO picked up\nby '+str(int(player))+' '+str(player_name)+' ('+str(player_hand)+')' #add position and name
        print(title)
        plt.text(111,0, title, size=15, va='center',ha='center',weight='bold',rotation=270,zorder=105,color='black')
        im = plt.imread('C:/Users/carli/Documents/Hockey Research/Chatham/oFO_2col_legend.PNG')
        newax = fig.add_axes([.205,.18,.1,.65], anchor='C', zorder=107)
        rotated_img = ndimage.rotate(im, 270)
        newax.imshow(rotated_img)
        newax.axis('off')
        #fake_legend = 'Shot Attempt   Passing Sequence\nLoss of Possession'
        #plt.text(20,0, fake_legend, size=10, va='center',ha='center',rotation=270,zorder=105)
        #plt.legend().set_zorder(120)
        #plt.legend(bbox_to_anchor=(1.25,0),ncol=2)
        #plt.show()
        plt.savefig('C:/Users/carli/Documents/Hockey Research/Chatham/FO charts/ozone_pu_'+player_name+'.png', facecolor='white',bbox_inches=matplotlib.transforms.Bbox([[.9, .1], [5.1, 3.9]]))
        plt.clf()

#ozone % breakdown
ofo_center_breakdown = pd.DataFrame(columns=['FO Player', '# of FOs', 'Shot Attempt %','Passing Sequence %', 'LOP %'])
i=0
for player in np.unique(oFOs['FO Player']):
    fo_data = oFOs[oFOs['FO Player'] == player].reset_index()
    if len(fo_data) > 5:
        player_name=roster.loc[(roster['Number']==player),'First Name'].to_string(index=False)+' '+roster.loc[(roster['Number']==player),'Last Name'].to_string(index=False)
        player_pos=roster.loc[(roster['Number']==player),'Position'].to_string(index=False)
        player_hand=roster.loc[(roster['Number']==player),'Handedness'].to_string(index=False)
        tot_fo = len(fo_data)
        sa_pct = len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Shot Attempt'])/tot_fo*100
        #print(len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Passing sequence']))
        lop_pct = len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Loss of Possession'])/tot_fo*100
        pa_pct = len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Passing sequence'])/tot_fo*100
        ofo_center_breakdown.loc[i] = pd.Series({'FO Player':player,'# of FOs':tot_fo, 'Shot Attempt %':sa_pct,'Passing Sequence %':pa_pct, 'LOP %':lop_pct})
        i += 1
ofo_center_breakdown.to_csv('C:/Users/carli/Documents/Hockey Research/Chatham/FO charts/ozone_center_breakdown.csv')

ofo_pu_breakdown = pd.DataFrame(columns=['Picked Up By', '# of FOs', 'Shot Attempt %','Passing Sequence %', 'LOP %'])
i=0
for player in np.unique(oFOs['Picked Up By']):
    fo_data = oFOs[oFOs['Picked Up By'] == player].reset_index()
    if len(fo_data) > 5:
        player_name=roster.loc[(roster['Number']==player),'First Name'].to_string(index=False)+' '+roster.loc[(roster['Number']==player),'Last Name'].to_string(index=False)
        player_pos=roster.loc[(roster['Number']==player),'Position'].to_string(index=False)
        player_hand=roster.loc[(roster['Number']==player),'Handedness'].to_string(index=False)
        tot_fo = len(fo_data)
        sa_pct = len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Shot Attempt'])/tot_fo*100
        #print(len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Passing sequence']))
        lop_pct = len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Loss of Possession'])/tot_fo*100
        pa_pct = len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Passing sequence'])/tot_fo*100
        ofo_pu_breakdown.loc[i] = pd.Series({'Picked Up By':player,'# of FOs':tot_fo, 'Shot Attempt %':sa_pct,'Passing Sequence %':pa_pct, 'LOP %':lop_pct})
        i += 1
ofo_pu_breakdown.to_csv('C:/Users/carli/Documents/Hockey Research/Chatham/FO charts/ozone_pu_breakdown.csv')

#dzone % breakdown
dfo_center_breakdown = pd.DataFrame(columns=['FO Player','# of FOs', 'Dump Out %','Skated Out %','Kept In %', 'LOP %'])
i=0
for player in np.unique(dFOs['FO Player']):
    fo_data = dFOs[dFOs['FO Player'] == player].reset_index()
    if len(fo_data) > 5:
        player_name=roster.loc[(roster['Number']==player),'First Name'].to_string(index=False)+' '+roster.loc[(roster['Number']==player),'Last Name'].to_string(index=False)
        player_pos=roster.loc[(roster['Number']==player),'Position'].to_string(index=False)
        player_hand=roster.loc[(roster['Number']==player),'Handedness'].to_string(index=False)
        tot_fo = len(fo_data)
        do_pct = len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Dumped Out'])/tot_fo*100
        lop_pct = len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Loss of Possession'])/tot_fo*100
        so_pct = len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Skated Out'])/tot_fo*100
        ki_pct = len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Kept In'])/tot_fo*100
        dfo_center_breakdown.loc[i] = pd.Series({'FO Player':player, '# of FOs':tot_fo,'Dump Out %':do_pct,'Skated Out %':so_pct,'Kept In %':ki_pct, 'LOP %':lop_pct})
        i += 1
dfo_center_breakdown.to_csv('C:/Users/carli/Documents/Hockey Research/Chatham/FO charts/dzone_center_breakdown.csv')

dfo_pu_breakdown = pd.DataFrame(columns=['Picked Up By', '# of FOs','Dump Out %','Skated Out %','Kept In %', 'LOP %'])
i=0
for player in np.unique(dFOs['Picked Up By']):
    fo_data = dFOs[dFOs['Picked Up By'] == player].reset_index()
    if len(fo_data) > 5:
        player_name=roster.loc[(roster['Number']==player),'First Name'].to_string(index=False)+' '+roster.loc[(roster['Number']==player),'Last Name'].to_string(index=False)
        player_pos=roster.loc[(roster['Number']==player),'Position'].to_string(index=False)
        player_hand=roster.loc[(roster['Number']==player),'Handedness'].to_string(index=False)
        tot_fo = len(fo_data)
        do_pct = len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Dumped Out'])/tot_fo*100
        lop_pct = len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Loss of Possession'])/tot_fo*100
        so_pct = len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Skated Out'])/tot_fo*100
        ki_pct = len(fo_data[fo_data['Chatham 5 Sec Result'] == 'Kept In'])/tot_fo*100
        dfo_pu_breakdown.loc[i] = pd.Series({'Picked Up By':player,'# of FOs':tot_fo, 'Dump Out %':do_pct,'Skated Out %':so_pct,'Kept In %':ki_pct, 'LOP %':lop_pct})
        i += 1
dfo_pu_breakdown.to_csv('C:/Users/carli/Documents/Hockey Research/Chatham/FO charts/dzone_pu_breakdown.csv')
