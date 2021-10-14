import fiona
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import PIL
import io


# Reading in the csv data into a pandas dataframe
data = pd.read_csv("time_series_covid19_confirmed_global.csv")

# Group the data by the country
data = data.groupby('Country/Region').sum()

# Drop Lat and Long columns
data = data.drop(columns = ['Lat','Long'])

#Create a transposition of the dataframe
data_transposed = data.T
#data_transposed.plot(y=['Australia','China','Canada','Italy'], use_index = True,figsize = (10,10))

# Read in the world map shapefile
world =gpd.read_file(r'D:\geopy\CovidDynamicMap\CovidGeospatialTimeSeries\World_Map.shp')
#world.plot()

world.replace('Viet Nam','Vietnam',inplace = True)
world.replace('Brunei Darussalam','Brunei',inplace = True)
world.replace('Cape Verde','Cabo Verde',inplace = True)
world.replace('Democratic Republic of the Congo','Congo (Kinshasa)',inplace = True)
world.replace('Congo','Congo (Brazzaville)',inplace = True)
world.replace('Czech Republic','Czechia',inplace = True)
world.replace('Swaziland','Eswatini',inplace = True)
world.replace('Iran (Islamic Republic of)','Iran',inplace = True)
world.replace('Korea, Republic of','Korea, South',inplace = True)
world.replace("Lao People's Democratic Republic",'Laos',inplace = True)
world.replace('Libyan Arab Jamahiriya','Libya',inplace = True)
world.replace('Republic of Moldova','Moldova',inplace = True)
world.replace('The former Yugoslav Republic of Macedonia','North Macedonia',inplace = True)
world.replace('Syrian Arab Republic','Syria',inplace = True)
world.replace('Taiwan','Taiwan*',inplace = True)
world.replace('United Republic of Tanzania','Tanzania',inplace = True)
world.replace('United States','US',inplace = True)
world.replace('Palestine','West Bank and Gaza',inplace = True)

# Merge the 'data' pandas dataframe with the 'world' geopandas geodataframe
merge = world.join(data,on='NAME', how = 'right')

image_list = []

#Only make plots for every interval number of days
interval = 7
interval_counter = 0

for dates in merge.columns.to_list()[2:]:

    if (interval_counter == interval):
        interval_counter = 0
        
        #Plot
        ax = merge.plot(column = dates,
                        cmap = 'OrRd',
                        figsize = (14,14),
                        legend = True,
                        scheme = 'user_defined',
                        classification_kwds = {'bins':[100,500,1000,5000,10000,500000,1000000,5000000,10000000]},
                        edgecolor = 'black',
                        linewidth = 0.4)

        # Add a title to the map
        ax.set_title('Total Confirmed Coronavirus Cases: '+dates, fontdict =
                     {'fontsize':20},pad=12.5)

        # Removing the axes
        ax.set_axis_off()

        # Move the legend
        ax.get_legend().set_bbox_to_anchor((0.18,0.6))

        img = ax.get_figure()

        f = io.BytesIO()
        img.savefig(f, format = 'png',bbox_inches = 'tight')
        f.seek(0)
        image_list.append(PIL.Image.open(f))

    else:
        interval_counter += 1       


# Create a GIF animation
image_list[0].save('DynamicCOVID-19Mapq7day.gif', format = 'GIF',
                     append_images = image_list[1:],
                     save_all = True,duration = 300,
                     loop = 3)
f.close()

#plt.show()
