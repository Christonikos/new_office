# =============================================================================
# MODULES, ALLIASES & GLOBALS
import pandas as pd
import numpy as np
import seaborn as sns
import os
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt
join=os.path.join
make=os.makedirs
exists=os.path.exists
see=os.listdir
load=pd.read_csv
# =============================================================================
# Paths
path2figs=join(os.path.realpath('..'),'Figures')
if not exists(path2figs): make(path2figs)

# =============================================================================


# == load .csvs == #
path2data=join(os.path.realpath('..'),'Data')
files=see(path2data)
data={} # initialize dictionary to hold the data
for idx,file in enumerate(files):
    target_name=files[idx].split('_')[0] # eg: accountant
    data[target_name]=load(join(path2data, file))
# see the venues or professions of interest specified @f'data_fetching'
target_venues= list(data.keys())
print(target_venues)

# =============================================================================
# EDA - We can use the rating as a reliable factor
for target in target_venues:
    sns.distplot(data[target].user_ratings_total, hist=False, kde=True, label=target)
plt.legend()
plt.title('#ratings')
plt.ylabel('Gaussian kernel density estimate')
plt.xlabel('#counts')
plt.tight_layout()
sns.despine()
figname=join(path2figs,'kde_ratings.png')
plt.savefig(figname, dpi=150)

# EDA - We can use the rating as a reliable factor

longs=[np.mean(data[target].longitude) for target in target_venues ]
error=[np.std(data[target].longitude) for target in target_venues ]
x_pos=np.arange(0,len(target_venues))
# 2. We need to remove outliers from the lawyer and bank offices
# Build the plot
fig, ax = plt.subplots()
ax.bar(x_pos, longs, yerr=error, align='center', alpha=0.2, ecolor='black', capsize=10)
ax.set_ylabel('Longitude')
ax.set_xticks(x_pos)
ax.set_xticklabels(target_venues)
plt.title('Longitude means & STDs')
plt.tight_layout()
sns.despine()
figname=join(path2figs,'longitude_eda.png')
plt.savefig(figname, dpi=150)



remove_outliers_from=['bank', 'lawyer']
for venue in remove_outliers_from:
    target=data[venue].longitude
    sns.distplot(target, bins=10, kde=False)
    plt.axvline(np.mean(target), color='k', label='mean')
    # plt.fill_betweenx(np.max(np.histogram(target)[0]),np.mean(target), np.max(target) )
    plt.legend()
    plt.title(f'{venue.capitalize()} latitude values')
    plt.tight_layout()
    sns.despine();
    figname=join(path2figs,f'longitude_dist_{venue}.png')
    plt.savefig(figname, dpi=150)
    plt.close()
# =============================================================================



