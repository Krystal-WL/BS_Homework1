# Pandas and Visualization
import pandas as pd
import os

os.getcwd()

# load the data to a single DataFrame
occupancy = pd.read_csv('LIN_KRYSTAL_python_assignment2_orig.csv')

# profile the dataFrame
occupancy.columns
occupancy.dtypes

# count the number of NaNs in each column
occupancy.isna().sum()
occupancy.shape

# summarize only numeric columns
occupancy.describe()

# find the most common values in each text columns
occupancy.select_dtypes(include=['object']).describe()

# find the frequency of each values in a specific text column 
occupancy['SECTOR'].value_counts()

occupancy.head()

# rename '_id' column to 'ID'
occupancy.rename(columns={'_id':'ID'}, inplace=True)
occupancy.head(3)

# find unique values in a single column
occupancy['PROGRAM_MODEL'].unique()

# find the counts of its values in a single text/categorical column and 
occupancy['OVERNIGHT_SERVICE_TYPE'].value_counts()
occupancy['SECTOR'].value_counts()

occupancy.dtypes

# 'OCCUPANCY_DATE' column: convert from a 'object' to a 'datetime' datatype
occupancy['OCCUPANCY_DATE'] = pd.to_datetime(occupancy['OCCUPANCY_DATE'])

# # 'LOCATION_ID' column: convert datatype from 'float64' to 'int64'
occupancy['LOCATION_ID'] = occupancy['LOCATION_ID'].astype('Int64')

# capacity and occupancy columns (CAPACITY_ACTUAL_BED, CAPACITY_FUNDING_BED, OCCUPIED_BEDS, UNOCCUPIED_BEDS, UNAVAILABLE_BEDS,'CAPACITY_ACTUAL_ROOM', 'CAPACITY_FUNDING_ROOM','OCCUPIED_ROOMS', 'UNOCCUPIED_ROOMS', 'UNAVAILABLE_ROOMS')
# represents counts, so they should be coverted from 'float64' to ''int64
columns_to_convert = ['CAPACITY_ACTUAL_BED', 
                      'CAPACITY_FUNDING_BED', 
                      'OCCUPIED_BEDS', 
                      'UNOCCUPIED_BEDS', 
                      'UNAVAILABLE_BEDS', 
                      'CAPACITY_ACTUAL_ROOM', 
                      'CAPACITY_FUNDING_ROOM', 
                      'OCCUPIED_ROOMS', 
                      'UNOCCUPIED_ROOMS', 
                      'UNAVAILABLE_ROOMS']

for column in columns_to_convert:
    occupancy[column] = occupancy[column].astype('Int64')
occupancy.dtypes


# save as a .xlsx file
occupancy.to_excel('LIN_KRYSTAL_python_assignment2_proc.xlsx', index=False)

# extract a month part 'OCCUPANCY_MONTH' from 'OCCUPANCY_DATE'
occupancy['OCCUPANCY_MONTH'] = occupancy['OCCUPANCY_DATE'].dt.month

occupancy['LOCATION_ADDRESS'].unique()

# use str.replace() to replace "Road" with "Rd" in the 'LOCATION_ADDRESS' column
occupancy['LOCATION_ADDRESS'] = occupancy['LOCATION_ADDRESS'].str.replace('Road', 'Rd')

occupancy['LOCATION_PROVINCE'].unique()

# remove the column 'LOCATION_PROVINCE'
occupancy_dropped = occupancy.drop(columns='LOCATION_PROVINCE')

occupancy_dropped['PROGRAM_MODEL'].unique()
occupancy_dropped['PROGRAM_MODEL'].value_counts()

# extract a subset of columns and rows to a new DataFrame --> 'occupancy_emergency'
occupancy_emergency = occupancy_dropped.loc[occupancy_dropped['PROGRAM_MODEL'] == 'Emergency', 
                                            # filter 'PROGRAM_MODEL' row is 'Emergency'
                      ['OCCUPANCY_DATE', 
                       'SECTOR', 
                       'PROGRAM_MODEL', 
                       'SERVICE_USER_COUNT', 
                       'CAPACITY_TYPE', 
                       'OCCUPANCY_RATE_BEDS', 
                       'OCCUPANCY_RATE_ROOMS']] # select columns
occupancy_dropped.describe()

# create a DataFrame containing records with NaNs in any column
occupancy_NaN = occupancy_dropped[occupancy_dropped.isna().any(axis=1)]
occupancy_NaN.describe()

# create a DataFrame containing records with NaNs in a subset of columns 'occupancy_emergency'
occupancy_emergency_NaN = occupancy_emergency[occupancy_emergency.isna().any(axis=1)]
occupancy_emergency_NaN.describe()

# create groups based on ‘OCCUPANCY_DATE’ column
occupancy_date_groups = occupancy_dropped.groupby(['OCCUPANCY_DATE'])
occupancy_date_groups.count()

# apply sum() and mean() on column 'SERVICE_USER_COUNT' and 'OCCUPANCY_RATE_BEDS'
service_user_summary =  occupancy_date_groups.agg(total_service_user = ('SERVICE_USER_COUNT', 'sum'),
                                                  average_service_user =('SERVICE_USER_COUNT', 'mean'),
                                                  average_occupancy_rate_beds=('OCCUPANCY_RATE_BEDS', 'mean'))

# use a object-oriented approach to plot a line chart
import matplotlib.pyplot as plt

# create the plot
fig, ax = plt.subplots()

# plot using the aggregated data 'service_user_summary'
ax.plot(service_user_summary.index, service_user_summary['total_service_user'], label = 'total_service_user')
# set a title, labels, a grid, and a legend
ax.set_title('Total Service User Over Time') 
ax.set_xlabel('occupancy date')
ax.set_ylabel('total service user')
ax.legend() 

# grid is in the background
ax.set_axisbelow(True) 

# set the transparency of grid
ax.grid(alpha=0.6) 

plt.savefig('total_service_user_over_time.png')