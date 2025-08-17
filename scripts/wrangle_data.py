import pandas as pd
from datetime import datetime
import joblib

# def wrangle_car_data(path):
    
#     df = pd.read_csv(path)
#     print(f" Data Wrngling Started ...")

#     # Drop duplicates
#     df.drop_duplicates(inplace=True)
    
#     # Drop rows with missing price or odometer
#     df = df[df['price'].notnull() & df['odometer'].notnull()]
    
#     # Clean price and odometer
#     df['price'] = df['price'].astype(float)
#     df['odometer'] = df['odometer'].astype(float)
    
#     # Feature: car age
#     df['car_age'] = 2025 - df['year']
    
#     # Drop irrelevant columns
#     drop_cols = ['id', 'url', 'image_url', 'description', 'posting_date']
#     df.drop(columns=[col for col in drop_cols if col in df.columns], inplace=True)

#     # Handle categorical features
#     categorical = ['condition', 'fuel', 'transmission', 'type', 'manufacturer']
#     df = pd.get_dummies(df, columns=categorical, drop_first=True)
    
#     print(f" Data Wrngled successfully ...")
#     return df


# def wrangle_car_data(filepath: str) -> pd.DataFrame:
#     # Load CSV
#     df = pd.read_csv(filepath)

#     # ====== 1. Remove obviously useless columns ======
#     drop_cols = [
#         'id', 'url', 'region_url', 'VIN', 'image_url', 'description',
#         'lat', 'long'  # often not useful unless you're modeling geography
#     ]
#     df = df.drop(columns=[col for col in drop_cols if col in df.columns], errors='ignore')

#     # ====== 2. Remove rows with no price ======
#     df = df[df['price'].notna() & (df['price'] > 0)]

#     # ====== 3. Handle numeric columns ======
#     numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
#     # Convert anything that looks numeric but is stored as object
#     for col in df.select_dtypes(include=['object']).columns:
#         try:
#             df[col] = pd.to_numeric(df[col])
#         except ValueError:
#             pass

#     # ====== 4. Encode categorical columns ======
#     categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
#     if categorical_cols:
#         df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

#     # ====== 5. Handle missing values ======
#     df = df.fillna(0)

#     return df


def wrangle_car_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)

    # ====== 1. Remove obviously useless columns ======
    drop_cols = [
        'id', 'url', 'region_url', 'VIN', 'image_url', 'description',
        'lat', 'long',  # often not useful unless you're modeling geography
        'county' # All rows are null
    ]
    df = df.drop(columns=[col for col in drop_cols if col in df.columns], errors='ignore')

    # ====== 2. Remove rows with no price ======
    df = df[df['price'].notna() & (df['price'] > 0)]    


    # ====== 3. Find categorical columns ======
    categorical_cols = df.select_dtypes(include=['category']).columns.tolist()
    categorical_cols

    threshold_ratio = 0.0002
    row_count = len(df)

    categorical_cols = [
        col for col in df.columns
        if df[col].nunique() / row_count <= threshold_ratio
    ]

    print(categorical_cols)
    print(len(categorical_cols))

    for COLUMN in categorical_cols:
        rows_count = len(df[COLUMN])
        unique_values = df[COLUMN].unique()
        no_unique = df[COLUMN].nunique()

        print("COLUMN:", COLUMN)
        print("Unique Values:", unique_values)
        print("Unique values number:", no_unique)
        print("Rows number:", rows_count)
        print("Unique values ratio:", (no_unique/rows_count) * 100)
        print("================================================")

    # Set categorical_cols to the proper category type.
    df[categorical_cols] = df[categorical_cols].astype('category')

    # Save unique values for each categorical column
    cat_values = {col: df[col].dropna().unique().tolist() for col in categorical_cols}
    # Save categorical_values to schema
    joblib.dump({
        "categorical_values": cat_values,
    }, "models/schema.pkl")


    # ====== 4. Drop string columns ======
    df = df.drop(df.select_dtypes(include=['object']).columns, axis=1)

    # ====== 5. Encode categorical columns ======
    # One Hot Encoder
    
    categorical_cols = df.select_dtypes(include=['category']).columns
    df = pd.get_dummies(df, categorical_cols, drop_first=True)

    # ====== 5. Handle null values ======

    null_threshold = 0.002
    high_null_cols = []
    for col in df.columns:
        null_ratio = (df[col].isna().sum()/len(df[col]))
        if null_ratio >= null_threshold:
            high_null_cols.append(col)

    # For the `odometer` fill with the median
    df['odometer'] = df['odometer'].fillna(df['odometer'].median())

    # For the 'year', calculate the age, then fill with the median
    current_year = datetime.now().year

    df['age'] = current_year - df['year']
    df['age'] = df['age'].fillna(df['age'].median())

    df = df.drop(columns=['year'])

    return df
