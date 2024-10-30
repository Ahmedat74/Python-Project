#Python module for Sales Project
"""
This module contains functions to analyze sales data from a JSON string.
"""
__version__ = '1.0.0'

#importing the required libraries

import json # => reading the data, since data is in JSON format

from datetime import datetime # => to convert date string to datetime object

import pandas as pd # => for data manipulation and analysis

#function to download data from JSON string
def DownloadData(json_str):
        try:
                data = json.loads(json_str)
                
                data_frame = pd.DataFrame(data)
                
                return data_frame
        except:
                raise ValueError(F"{json_str} must be a valid JSON string format")
        
#if you want to Take a part of data and anaylsis it you can uncomment below lines
#def get_part_of_data(data_frame, number_of_rows):
#       new_data_frame = data_frame.head(number_of_rows)
#        return new_data_frame

#function to convert string date to datetime object        
def ConvertIntoDatetime(data_frame, date_column):
        try:
                data_frame[date_column] = pd.to_datetime(data_frame[date_column])
                
                return data_frame
        except:
                raise ValueError(F"{date_column} must be a valid column name in the data frame")
        
#function to get sales for a single item in a given date range                
def GetSalesForItem(json_str,date_column,id_column_name, product_id,start_date, end_date):
        
        data_frame = DownloadData(json_str)
        
        ConvertIntoDatetime(data_frame, date_column)
        
        filterd_data = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date)]  
        
        single_sales = filterd_data[filterd_data[id_column_name] == product_id]
        
        json_sales = single_sales.to_json()
        
        return  json_sales

        
#function to get sales for multiple items in a given date range
            
def GetSalesForListItems(json_str,date_column,id_colunm_name, product_ids, start_date, end_date, target_colunm):
        
        data_frame = DownloadData(json_str)
        
        ConvertIntoDatetime(data_frame, date_column)
        
        filterd_data = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date)]
        
        multiple_sales = filterd_data[filterd_data[id_colunm_name].isin(product_ids)]
        
        json_sales = multiple_sales.to_json()
        
        return json_sales

#function  to get sales for a single branch in given date range                                           
def GetSalesForBranchId(json_str,date_column,branch_column_name,branch_id,start_date,end_date,target_colunm):
        
        data_frame = DownloadData(json_str)
        
        ConvertIntoDatetime(data_frame, date_column)
        
        filterd_data = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date)]
        
        branch_sales = filterd_data[filterd_data[branch_column_name] == branch_id]
        
        json_sales = branch_sales.to_json()

        return json_sales

#function to get total sales for a single item and a given branch in a given date range                                         
def GetTotalSales(json_str,date_column,target_column,id_column_name,product_id,start_date,end_date,branch_column_name):
        
        data_frame = DownloadData(json_str)

        ConvertIntoDatetime(data_frame, date_column)

        #filter data based on date range and product id
        filtered_df = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date) & (data_frame[id_column_name] == product_id)]

        merge_date_branch = filtered_df.groupby([date_column, branch_column_name])

        total_sales = merge_date_branch[target_column].sum().reset_index()
        
        sum_of_sales = total_sales[target_column].sum()

        json_sales = total_sales.to_json()

        return json_sales , sum_of_sales
 
#function for checking sales movement for a single item in a given date range                                     
def checkSalesMovement(sum_of_sales):
        
        if(sum_of_sales > 0):
                
                return "There Were Sales Movement for this item"
        
        elif(sum_of_sales < 0):
                
                return "There Were Return Movements for this item"
        
        else:
                
              return  """
                There are two possibities: either there were no sales or returns for this item
                or the sales and returns were equal for this item
                """       
#function  to check for no movements per day for a single item in a given date range                                             
def checkForNoMovementsperDay(json_str,date_column,product_id_column, product_id,date_day,target_column):
        
        data_frame = DownloadData(json_str)
        
        ConvertIntoDatetime(data_frame, date_column)
        
        filtered_df = data_frame[(data_frame[date_column] == date_day) & (data_frame[product_id_column] == product_id)]
        
        if(filtered_df[target_column].sum() == 0):
                
                return "There were no sales or returns for this item on this day"
        else:
                
                return "There were sales or returns for this item on this day"
        
def checkForMovementsperRange(json_str, date_column, product_id_column, product_id, start_date, end_date, target_column):

        data_frame = DownloadData(json_str)

        ConvertIntoDatetime(data_frame, date_column)

        filtered_df = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date) & (data_frame[product_id_column] == product_id)]

        no_movement_days = filtered_df[target_column].sum() == 0

        if no_movement_days:
                
                return "No sales or returns for this item on any of the days in the given date range"
        else:

                return "Sales or returns for this item on some of the days in the given date range"

#function to calculate outlier sales using Z-score                                            
                
def GetOutlierZscore(json_str,product__id_column,product_id,date_column,target_column,start_date, end_date,num):
        
        data_frame = DownloadData(json_str)
        
        ConvertIntoDatetime(data_frame, date_column)
        
        filtered_df = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date) & (data_frame[product__id_column] == product_id)]
        
        mean_sales = filtered_df[target_column].mean()
        
        std_sales = filtered_df[target_column].std()
        
        filtered_df['Z-score'] = (filtered_df[target_column] - mean_sales) / std_sales
        
        filtered_df['Outlier'] = filtered_df['Z-score'].abs() > num
        
        json_Zscore = filtered_df.to_json()
        
        return json_Zscore
#function to calculate outlier sales using IQR method(Interquartile Range)                                                                                        
def GetOutlierIQR(json_str, product__id_column, product_id, date_column, target_column, start_date, end_date):
        
        data_frame = DownloadData(json_str)
        
        ConvertIntoDatetime(data_frame, date_column)
        
        filtered_df = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date) & (data_frame[product__id_column] == product_id)]
        
        Q1 = filtered_df[target_column].quantile(0.25)
        
        Q3 = filtered_df[target_column].quantile(0.75)
        
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        
        
        upper_bound = Q3 + 1.5 * IQR
        
        filtered_df['Outlier'] = (filtered_df[target_column] > upper_bound)
        
        json_Iqr = filtered_df.to_json()
    

        return json_Iqr , IQR

                
#this for Example usage
if __name__ == "__main__":
        json_str = """

"""
df = DownloadData(json_str)

newdf = ConvertIntoDatetime(df, 'date')

startdate = datetime(2022, 1, 1)

enddate = datetime(2022, 12, 31)

getsalesbyproductid = GetSalesForItem(newdf, 'date', 'product_id', 1, startdate, enddate, 'sales')

getsalesbyproductid_list = GetSalesForListItems(newdf, 'date', 'product_id', [1, 2, 3], startdate, enddate, 'sales')

getsalesbybranch_id = GetSalesForBranchId(newdf, 'date', 'branch_id', 1, startdate, enddate, 'sales')

totalsales , sum_of_sales = GetTotalSales(newdf, 'date', 'sales', 'product_id', 1, startdate, enddate, 'branch_id')

checksales = checkSalesMovement(sum_of_sales)

checknosalesmovement = checkForNoMovementsperDay(newdf, 'date', 'product_id', 1, datetime(2022, 1, 1), 'sales')

checkmovementrange = checkForMovementsperRange(newdf, 'date', 'product_id', 1, datetime(2022, 1, 1), datetime(2022, 12, 31), 'sales')

outlierzscore = GetOutlierZscore(newdf, 'product_id', 1, 'date', 'sales', startdate, enddate)

outlieriqr, iqr = GetOutlierIQR(newdf, 'product_id', 1, 'date', 'sales', startdate, enddate)