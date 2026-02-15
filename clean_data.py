def clean_data(df):
    # remove duplicates
    df = df.drop_duplicates()
    # forward fill missing values ie missing value is filled with the last known value
    df = df.fillna(method='ffill')  
    # drop remaining missing values
    df = df.dropna()
    # reset the cleaned data
    return df