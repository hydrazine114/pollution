The code contains several chapters.
Description for all:

# Collect
This code snippet represents a script for loading and processing meteorological measurement data from several locations in Mexico. The data is in CSV format, and each location has a separate directory with data files.

The script uses the Pandas library to load data and create DataFrame objects. It loads each CSV file for each location, creates a separate DataFrame object for each file, adds a region column for each DataFrame indicating the location, and concatenates all DataFrames into one large DataFrame.

The script then removes rows with invalid TIMESTAMP values, converts the types of columns in the DataFrame, and saves the resulting DataFrame in Apache Parquet format.

To use the script, the user must first load the meteorological measurement data into directories for each location they want to process. Additionally, the user must have the Pandas and os libraries installed. After running the script, the created collected_data.parquet file can be used for further data analysis.

# Check data
First of all we chack time delta holes and destributions of columns in different regions.

Based on theese we decided to use Z - value and quantille to cleaning the data in each region.

# Clean data
This piece of code filters the data according to certain criteria, using the quantile function to calculate the quantiles of the array.

The code first loads the data from the data/collected_data.parquet file into a DataFrame Pandas object. It then groups the data by region column and applies several aggregation functions to multiple columns, including WSpeed_Avg, WSpeed_Max, Press_Avg, and Temp_Avg. The results are then saved to a new DataFrame dft.

Next, the code executes an SQL query using filter functions to create a new DataFrame df.

This code uses different filtering criteria to cleanse each column of data from outliers and/or errors.

For the Temp_Avg column, a z-value filter for temperature is used: values between -3 and 3 standard deviations from the mean value are left in the column, the rest are replaced by NULL.

A simple filter is used for the WSpeed_AVG and WSpeed_Max columns: values from 0 to the 99th quantile are left in the column, the rest are replaced by NULL.

The WDir_SD column also uses a simple filter: values between 0.001 and 359.999 are left in the column, the rest are replaced by NULL.

A simple filter is also used for the Rain_Tot column: values greater than or equal to 0 are left in the column, the rest are replaced by NULL.

For the Press_Avg column a filter of z-values for pressure is used: values within -3 to 3 standard deviations from the average value are left in the column, the rest are replaced by NULL.

A simple filter is used for the Rad_Avg column: values greater than 0.001 are left in the column, the rest are replaced by NULL.

For Visibility_Avg and Visibility columns a simple filter is used: the values between 500 and 19000 are left in the column, the rest are replaced by NULL.

For column RH_Avg a simple filter is used: values from 1 to 99 are left in the column, the rest are replaced by NULL.

The WDir_AVG column also uses a simple filter: values from 0.001 to 359.999 are left in the column, the rest are replaced by NULL.

# Data analyse 

## Time series

This code performs the following tasks:

Reads cleaned data from a Parquet file 'cleaned.parquet'.
Aggregates hourly weather data by taking the average of temperature, relative humidity, wind speed, wind direction, rain, pressure, radiation, and visibility for each region.
Adds additional time-based columns such as week number, hour number, and month number to the aggregated data.
Plots temperature data over time using seaborn lineplot for Morelia region. Then, plots temperature data over weeks for Morelia region and three regions (Morelia, Mexico, and Puerto Morelos) using three subplots.
Sets y-axis labels, y-axis limits, x-axis labels for each subplot, and the position of each subplot using box parameter. Then it sets the legend for the third subplot.

## Distribution of different variables

This code creates a violin plot using Seaborn library to visualize the distribution of temperature for several regions. The regions included in the plot are 'Morelia', 'Puerto Morelos', 'Sisal', 'Mexico', and 'Los Tuxtlas', and they are plotted on the y-axis. The temperature values are plotted on the x-axis.

A violin plot is a graphical representation of the density distribution of the data. The shape of the violin indicates the density of the data at different values of the temperature. A wider section of the violin indicates a higher density of data at that temperature value. The white dot inside the violin represents the median temperature value.

The x-axis label indicates the unit of temperature, which is Celsius. The y-axis label is left blank because the region names are already displayed on the y-axis.

## Wind Rose

This code defines a function get_wr that creates a windrose plot using the WindroseAxes module from the windrose library. The plot shows the distribution of wind direction and speed for a given region.

The get_wr function takes a single argument, region, which specifies the region for which the windrose plot is to be created. It uses Pandas DataFrame (df) that contains weather data to extract the wdir_avg (average wind direction) and wspeed_avg (average wind speed) columns for the specified region.

The WindroseAxes object is then created and the bar method is used to plot the wind rose. The normed=True argument specifies that the frequencies should be normalized. The opening=0.8 argument sets the gap between the bars of the windrose plot. The legend is placed below the plot using the bbox_to_anchor argument, and the title is set to the specified region.

## Seasonality 

This code performs time series analysis on weather data.

Next, the cleaned data is processed and aggregated by hour, month, and region, with the following variables being calculated: temp, rh, wspeed_avg, wdir_avg, wdir_sd, rain_tot, press, rad, and visibility_avg.

Then, the show_day_month_seasonality() function is defined, which takes a parameter y_axis (which can be temp, rh, wspeed_avg, wdir_avg, wdir_sd, rain_tot, press, rad, or visibility_avg) and generates a plot of the monthly and daily seasonality of that variable for the regions Morelia, Mexico, and Puerto Morelos. The plot shows a line graph of the variable values over time, with the x-axis labeled with the months of the year and the y-axis labeled with the variable name. The plot also includes vertical dashed lines to indicate the start of each month. The function allows for easy visualization of patterns in the data and can be used to identify trends and seasonal patterns in the weather data.

