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
def GetSalesForItem(data_frame,date_column,id_column_name, product_id,start_date, end_date, target_colunm):
        
        filterd_data = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date)]  
        
        single_sales = filterd_data[filterd_data[id_column_name] == product_id]
        
        total_single_sales = single_sales[target_colunm].sum()
        
        return total_single_sales, single_sales

        
#function to get sales for multiple items in a given date range
            
def GetSalesForListItems(date_frame,date_column,id_colunm_name, product_ids, start_date, end_date, target_colunm):
        
        filterd_data = date_frame[(date_frame[date_column] >= start_date) & (date_frame[date_column] <= end_date)]
        
        multiple_sales = filterd_data[filterd_data[id_colunm_name].isin(product_ids)]
        
        return multiple_sales 

#function  to get sales for a single branch in given date range                                           
def GetSalesForBranchId(data_frame,date_column,branch_column_name,branch_id,start_date,end_date,target_colunm):
        
        filterd_data = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date)]
        
        branch_sales = filterd_data[filterd_data[branch_column_name] == branch_id]
        
        total_branch_sales = branch_sales[target_colunm].sum()

        return total_branch_sales, branch_sales 

#function to get total sales for a single item and a given branch in a given date range                                         
def GetTotalSales(data_frame,date_column,target_column,id_column_name,product_id,start_date,end_date,branch_column_name):
        
        filtered_df = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date) & (data_frame[id_column_name] == product_id)]
        
        merge_date_branch = filtered_df.groupby([date_column,branch_column_name])
                    
        total_sales = merge_date_branch[target_column].sum().reset_index()
        
        sum_of_sales = total_sales[target_column].sum()
        
        return total_sales , sum_of_sales
 
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
def checkForNoMovementsperDay(data_frame,date_column,product_id_column, product_id,date_day,target_column):
        
        filtered_df = data_frame[(data_frame[date_column] == date_day) & (data_frame[product_id_column] == product_id)]
        
        if(filtered_df[target_column].sum() == 0):
                
                return "There were no sales or returns for this item on this day"
        else:
                
                return "There were sales or returns for this item on this day"
        
def checkForMovementsperRange(data_frame, date_column, product_id_column, product_id, start_date, end_date, target_column):

        filtered_df = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date) & (data_frame[product_id_column] == product_id)]

        no_movement_days = filtered_df[target_column].sum() == 0

        if no_movement_days:
                
                return "No sales or returns for this item on any of the days in the given date range"
        else:

                return "Sales or returns for this item on some of the days in the given date range"

#function to calculate outlier sales using Z-score                                            
                
def GetOutlierZscore(data_frame,product__id_column,product_id,date_column,target_column,start_date, end_date):
        
        filtered_df = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date) & (data_frame[product__id_column] == product_id)]
        
        mean_sales = filtered_df[target_column].mean()
        
        std_sales = filtered_df[target_column].std()
        
        filtered_df['Z-score'] = (filtered_df[target_column] - mean_sales) / std_sales
        
        filtered_df['Outlier'] = filtered_df['Z-score'].abs() > 3
        
        return filtered_df
#function to calculate outlier sales using IQR method(Interquartile Range)                                                                                        
def GetOutlierIQR(data_frame, product__id_column, product_id, date_column, target_column, start_date, end_date):
        
        filtered_df = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date) & (data_frame[product__id_column] == product_id)]
        
        Q1 = filtered_df[target_column].quantile(0.25)
        
        Q3 = filtered_df[target_column].quantile(0.75)
        
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        
        
        upper_bound = Q3 + 1.5 * IQR
        
        filtered_df['Outlier'] = (filtered_df[target_column] > upper_bound)
    

        return filtered_df , IQR

                
#this for Example usage
if __name__ == "__main__":
        json_str = """

"""

