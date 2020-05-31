import sys

import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    '''
    ** Load the raw data
    >> Args
        messages_filepath - path for the file that contains the disasters messages
        categories_fileath - path for the file that contains the categories of messages
    << return
        df - dataframe merged
    '''
    df_messages = pd.read_csv('disaster_messages.csv')
    df_categories = pd.read_csv('disaster_categories.csv')
    df = df_messages.merge(df_categories, on = 'id', how = 'left')
    
    return df

def clean_data(df):
    '''
    ** Cleaning of data from input dataframe
    >> Arg:
        df - dataframe not cleaned
    << return
        df - datafrem cleaned
    '''
    #Treatment of df_categories
    # split categories into separate columns
    df_categories = df.categories.str.split(pat = ';', expand = True) 
    
    # select the first row of the categories dataframe
    row = df_categories.iloc[1]                                       
    
     # transform column names by deleting numerical postfix
    category_colnames = row.apply(lambda x: x[:x.find('-')])         
    df_categories.columns = category_colnames  
    
    # transform categories values into 0's and 1's
    for column in category_colnames :                                                   
        df_categories[column] = df_categories[column].str.split(pat = '-').str[1]
        df_categories[column] = df_categories[column].astype(int)  
    
    #Drop old categories columns from df to receive new categories columns from df_categories
    df.drop(columns = ['categories'], axis = 1, inplace = True)
    df = pd.concat([df, df_categories], axis = 1)

    # fix 2 values to 1
    df['related'] = df.related.apply(lambda x: 1 if x == 2 else x)
    
    df.drop_duplicates(inplace = True)
   
    return df
    
def save_data(df, database_filename):  
    '''
    ** Save dataframe cleaned previously
    >> Args:
        df - dataframe cleaned
        database_filenae - the name given to the file
    '''
    engine = create_engine(f'sqlite:///{database_filename}')
    df.to_sql('messages_cleaned', engine, index=False)

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')

if __name__ == '__main__':
    main()