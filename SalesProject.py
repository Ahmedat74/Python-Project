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
        
        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        
        filterd_data = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date)]  
        
        filterd_data[date_column] = filterd_data[date_column].apply(lambda x: x.isoformat())
        
        single_sales = filterd_data[filterd_data[id_column_name] == product_id]
        
        json_sales = single_sales.to_json()
        
        return  json_sales

        
#function to get sales for multiple items in a given date range
            
def GetSalesForListItems(json_str,date_column,id_colunm_name, product_ids, start_date, end_date):
        
        data_frame = DownloadData(json_str)
        
        ConvertIntoDatetime(data_frame, date_column)
        
        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        
        filterd_data = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date)]
        filterd_data[date_column] = filterd_data[date_column].apply(lambda x: x.isoformat())
        multiple_sales = filterd_data[filterd_data[id_colunm_name].isin(product_ids)]
        
        json_sales = multiple_sales.to_json()
        
        return json_sales

#function  to get sales for a single branch in given date range                                           
def GetSalesForBranchId(json_str,date_column,branch_column_name,branch_id,start_date,end_date,target_colunm):
        
        data_frame = DownloadData(json_str)
        
        ConvertIntoDatetime(data_frame, date_column)
        
        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        
        filterd_data = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date)]
        filterd_data[date_column] = filterd_data[date_column].apply(lambda x: x.isoformat())
        branch_sales = filterd_data[filterd_data[branch_column_name] == branch_id]
        
        json_sales = branch_sales.to_json()

        return json_sales

#function to get total sales for a single item and a given branch in a given date range                                         
def GetTotalSales(json_str,date_column,target_column,id_column_name,product_id,start_date,end_date,branch_column_name):
        
        data_frame = DownloadData(json_str)

        ConvertIntoDatetime(data_frame, date_column)
        
        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

        #filter data based on date range and product id
        filtered_df = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date)& (data_frame[id_column_name] == product_id)]
        
        filtered_df[date_column] = filtered_df[date_column].apply(lambda x: x.isoformat())
        merge_date_branch = filtered_df.groupby([date_column, branch_column_name])
        

        total_sales = merge_date_branch[target_column].sum().reset_index()
        
        sum_of_sales = total_sales[target_column].sum()

        json_sales = total_sales.to_json(orient = 'records')

        return json_sales 
 
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
        
        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        
        filtered_df = data_frame[(data_frame[date_column] == date_day) & (data_frame[product_id_column] == product_id)]
        
        if(filtered_df[target_column].sum() == 0):
                
                return "There were no sales or returns for this item on this day"
        else:
                
                return "There were sales or returns for this item on this day"
        
def checkForMovementsperRange(json_str, date_column, product_id_column, product_id, start_date, end_date, target_column):

        data_frame = DownloadData(json_str)

        ConvertIntoDatetime(data_frame, date_column)
        
        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

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
        
        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        
        filtered_df = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date) & (data_frame[product__id_column] == product_id)]
        
        mean_sales = filtered_df[target_column].mean()
        
        std_sales = filtered_df[target_column].std()
        
        filtered_df['Z-score'] = (filtered_df[target_column] - mean_sales) / std_sales
        
        filtered_df['Outlier'] = filtered_df['Z-score'].abs() > num
        
        filtered_df[date_column] = filtered_df[date_column].apply(lambda x : x.isoformat())
        
        json_Zscore = filtered_df.to_json(orient = 'records')
        
        return json_Zscore
#function to calculate outlier sales using IQR method(Interquartile Range)                                                                                        
def GetOutlierIQR(json_str, product__id_column, product_id, date_column, target_column, start_date, end_date):
        
        data_frame = DownloadData(json_str)
        
        ConvertIntoDatetime(data_frame, date_column)
        
        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        
        filtered_df = data_frame[(data_frame[date_column] >= start_date) & (data_frame[date_column] <= end_date) & (data_frame[product__id_column] == product_id)]
        
        Q1 = filtered_df[target_column].quantile(0.25)
        
        Q3 = filtered_df[target_column].quantile(0.75)
        
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        
        
        upper_bound = Q3 + 1.5 * IQR
        
        filtered_df['Outlier'] = (filtered_df[target_column] > upper_bound)
        
        filtered_df[date_column] = filtered_df[date_column].apply(lambda x : x.isoformat())
        
        json_Iqr = filtered_df.to_json(orient = 'records')
    

        return json_Iqr

                
#this for Example usage
if __name__ == "__main__":
        json_str = """[{"Id":1006,"SalesDate":"2019-02-12T12:00:00","BranchId":12,"SoldQty":2.5},{"Id":1003,"SalesDate":"2017-02-21T18:20:00","BranchId":12,"SoldQty":3.5},{"Id":1007,"SalesDate":"2016-11-16T16:20:00","BranchId":32,"SoldQty":4},{"Id":1006,"SalesDate":"2017-02-21T18:20:00","BranchId":14,"SoldQty":4.5},{"Id":1011,"SalesDate":"2019-07-21T11:20:00","BranchId":6,"SoldQty":5.5},{"Id":1012,"SalesDate":"2019-03-21T15:20:00","BranchId":2,"SoldQty":1.5},{"Id":1023,"SalesDate":"2019-02-21T13:20:00","BranchId":15,"SoldQty":9.5},{"Id":1020,"SalesDate":"2020-05-30T18:20:00","BranchId":16,"SoldQty":3.5},{"Id":1010,"SalesDate":"2023-02-21T18:20:00","BranchId":17,"SoldQty":3.5},{"Id":1011,"SalesDate":"2020-02-21T18:20:00","BranchId":19,"SoldQty":12},{"Id":1028,"SalesDate":"2024-02-21T18:20:00","BranchId":20,"SoldQty":6},{"Id":1011,"SalesDate":"2021-02-21T18:20:00","BranchId":5,"SoldQty":8.5},{"Id":1012,"SalesDate":"2018-02-21T18:20:00","BranchId":15,"SoldQty":7.5},{"Id":1032,"SalesDate":"2017-02-21T18:20:00","BranchId":11,"SoldQty":2.5},{"Id":1011,"SalesDate":"2022-02-21T18:20:00","BranchId":12,"SoldQty":3.5},{"Id":1043,"SalesDate":"2023-02-21T18:20:00","BranchId":17,"SoldQty":5.5},{"Id":1002,"SalesDate":"2023-02-21T18:20:00","BranchId":13,"SoldQty":4.5}]
        """
        