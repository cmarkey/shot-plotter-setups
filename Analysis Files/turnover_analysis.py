import numpy as np
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
from matplotlib import rc
import matplotlib

plt.rcParams["font.family"] = "Consolas"
cougars = sb.diverging_palette(150, 275, s=60, l=55,n=2)
cougars
MY_DPI = 96
IMG_WIDTH = 1524
IMG_HEIGHT = 440

data_views = ["*.csv",
            "*Utica.csv",
            "*Wilkes.csv"] #list of csv's to cycle through

fig, ax = plt.subplots(1, len(data_views),figsize=(IMG_WIDTH / MY_DPI, IMG_HEIGHT / MY_DPI), dpi=MY_DPI,sharey=True)
for i in range(len(data_views)):
    print(data_views[i])
    turnovers = pd.concat(map(pd.read_csv, glob.glob(os.path.join('C:/Users/carli/Documents/Hockey Research/Chatham/Turnover data', data_views[i])))).reset_index()
    turnovers = turnovers.drop(columns=['index']).sort_values(by=['Takeaway', 'Takeaway Type'])
    turnovers.loc[(turnovers['Takeaway'] == 'Attempted'),'Takeaway'] = 'Failed'
    print(turnovers)
    physical_success = len(turnovers[(turnovers['Takeaway'] == 'Sucessful') & (turnovers['Takeaway Type'] == 'Physical Contact')])
    physical_Failed = len(turnovers[(turnovers['Takeaway'] == 'Failed') & (turnovers['Takeaway Type'] == 'Physical Contact')])
    stick_success = len(turnovers[(turnovers['Takeaway'] == 'Sucessful') & (turnovers['Takeaway Type'] == 'Stick Only')])
    stick_Failed = len(turnovers[(turnovers['Takeaway'] == 'Failed') & (turnovers['Takeaway Type'] == 'Stick Only')])

    pc_percent = physical_success/(physical_Failed+physical_success)*100
    s_percent = stick_success/(stick_Failed+stick_success)*100
    print(pc_percent,s_percent)

    tot_pc = physical_Failed+physical_success
    tot_s = stick_success+stick_Failed
    print(tot_pc,tot_s)
    sb.histplot(data=turnovers, x='Takeaway Type', hue='Takeaway', multiple='stack',ax=ax[i], palette=cougars)

ax[0].title.set_text('Total (4 Games)')
ax[1].title.set_text('Utica (2 Games)')
ax[2].title.set_text('Wilkes (2 Games)')
plt.savefig('Chatham/takeaway_summary.png', facecolor='white')
