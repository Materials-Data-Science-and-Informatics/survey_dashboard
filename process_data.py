#!/usr/bin/env python3
"""
Data processing script for HMC Survey Dashboard

This script processes the raw survey data from responses_cleaned_mapped_internal_use.csv
and creates the cleaned data file hmc_survey_2021_data_cleaned.csv with proper
column mapping and data preparation for analysis and plotting.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_column_mapping():
    """Load the column mapping dictionary from the specifications"""
    # Import the column mapping dictionary
    import sys
    sys.path.append('survey_dashboard/data/display_specifications')
    from hcs_clean_dictionaries import HCS_colnamesDict
    return HCS_colnamesDict

def process_research_area_columns(df):
    """
    Process research area columns to create a single researchArea column
    based on the specific research area columns that have values
    """
    # List of research area columns to check
    research_area_cols = [
        'PERBG3ING/_', 'PERBG3GEO/_', 'PERBG3MATH/_', 'PERBG3PHYS/_',
        'PERBG3LIFE/_', 'PERBG3BIO/_', 'PERBG3MED/_', 'PERBG3AGRI/_',
        'PERBG3PSYCH/_', 'PERBG3CHEM/_'
    ]
    
    # Create a mapping from specific research area columns to general areas
    area_mapping = {
        'PERBG3ING/_': 'Engineering Science',
        'PERBG3GEO/_': 'Earth Science', 
        'PERBG3MATH/_': 'Mathematics',
        'PERBG3PHYS/_': 'Physics',
        'PERBG3LIFE/_': 'Life Science',
        'PERBG3BIO/_': 'Life Science',
        'PERBG3MED/_': 'Life Science',
        'PERBG3AGRI/_': 'Life Science',
        'PERBG3PSYCH/_': 'Psychology',
        'PERBG3CHEM/_': 'Chemistry'
    }
    
    # Initialize the researchArea column
    df['PERBG3/_'] = ''
    
    # Fill researchArea based on which specific columns have values
    for col in research_area_cols:
        if col in df.columns:
            # Find rows where this column has a value (not empty, not NaN)
            mask = df[col].notna() & (df[col] != '') & (df[col] != 'False')
            df.loc[mask, 'PERBG3/_'] = area_mapping.get(col, col)
    
    return df

def clean_boolean_columns(df):
    """Convert boolean-like columns to proper boolean values"""
    # Columns that should be treated as boolean (excluding DTPUB6/1 which is numeric)
    boolean_cols = [col for col in df.columns if any(x in col for x in ['/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9', '/10']) and col != 'DTPUB6/1']
    
    for col in boolean_cols:
        if col in df.columns:
            # Convert 'True'/'False' strings to boolean
            df[col] = df[col].map({'True': True, 'False': False, '': False})
            # Fill NaN with False
            df[col] = df[col].fillna(False)
    
    return df

def process_software_columns(df):
    """Process software-related columns to create software_1, software_2, software_3 columns"""
    # Software-related columns (these are the ones that contain software names)
    software_cols = [
        'RDMPR6/1', 'RDMPR6/2', 'RDMPR6/3', 'RDMPR6/4', 'RDMPR6/5',
        'RDMPR6/6', 'RDMPR6/7', 'RDMPR6/8', 'RDMPR6/9', 'RDMPR6/10',
        'RDMPR6/11', 'RDMPR6/12', 'RDMPR6/13', 'RDMPR6/14', 'RDMPR6/15',
        'RDMPR6/16', 'RDMPR6/17', 'RDMPR6/18', 'RDMPR6/19', 'RDMPR6/20',
        'RDMPR6/21', 'RDMPR6/22', 'RDMPR6/23', 'RDMPR6/24', 'RDMPR6/25',
        'RDMPR6/26'
    ]
    
    # Initialize software columns
    df['software_1'] = ''
    df['software_2'] = ''
    df['software_3'] = ''
    
    # For each row, collect software names from columns that are True
    for idx, row in df.iterrows():
        software_list = []
        for col in software_cols:
            if col in df.columns and row[col] == True:
                # Extract software name from column name or use a default
                software_name = col.replace('RDMPR6/', '').replace('_', '')
                software_list.append(software_name)
        
        # Assign up to 3 software names
        for i, software in enumerate(software_list[:3]):
            df.at[idx, f'software_{i+1}'] = software
    
    return df

def process_publication_repository_columns(df):
    """Process publication repository columns to create pubRepo_1, pubRepo_2, etc."""
    # Publication repository columns
    pub_repo_cols = [
        'RDMPR7/2', 'RDMPR7/3', 'RDMPR7/4', 'RDMPR7/5', 'RDMPR7/6',
        'RDMPR7/7', 'RDMPR7/8', 'RDMPR7/9'
    ]
    
    # Initialize publication repository columns
    df['pubRepo_1'] = ''
    df['pubRepo_2'] = ''
    df['pubRepo_3'] = ''
    df['pubRepo_4'] = ''
    df['pubRepo_5'] = ''
    
    # For each row, collect repository names from columns that are True
    for idx, row in df.iterrows():
        repo_list = []
        for col in pub_repo_cols:
            if col in df.columns and row[col] == True:
                # Map column names to repository names
                repo_mapping = {
                    'RDMPR7/2': 'Zenodo',
                    'RDMPR7/3': 'RODARE',
                    'RDMPR7/4': 'Gitlab / GitHub',
                    'RDMPR7/5': 'Institutional Repository',
                    'RDMPR7/6': 'OSF',
                    'RDMPR7/7': 'FZJ Datapub',
                    'RDMPR7/8': 'HZB ICAT',
                    'RDMPR7/9': 'Other'
                }
                repo_name = repo_mapping.get(col, col)
                repo_list.append(repo_name)
        
        # Assign up to 5 repository names
        for i, repo in enumerate(repo_list[:5]):
            df.at[idx, f'pubRepo_{i+1}'] = repo
    
    return df

def process_data_generation_method_columns(df):
    """Process data generation method columns"""
    # Data generation method columns
    method_cols = [
        'RSDP2/1', 'RSDP2/2', 'RSDP2/3', 'RSDP2/4', 'RSDP2/5', 'RSDP2/6'
    ]
    
    # Initialize data generation method columns
    df['dataGenMethod_1'] = ''
    df['dataGenMethod_2'] = ''
    df['dataGenMethod_3'] = ''
    df['dataGenMethod_4'] = ''
    df['dataGenMethod_5'] = ''
    df['dataGenMethod_6'] = ''
    
    # For each row, collect method names from columns that are True
    for idx, row in df.iterrows():
        method_list = []
        for col in method_cols:
            if col in df.columns and row[col] == True:
                # Map column names to method names
                method_mapping = {
                    'RSDP2/1': 'Experimental',
                    'RSDP2/2': 'Simulation',
                    'RSDP2/3': 'Literature Review',
                    'RSDP2/4': 'Survey',
                    'RSDP2/5': 'Other',
                    'RSDP2/6': 'Not specified'
                }
                method_name = method_mapping.get(col, col)
                method_list.append(method_name)
        
        # Assign up to 6 method names
        for i, method in enumerate(method_list[:6]):
            df.at[idx, f'dataGenMethod_{i+1}'] = method
    
    return df

def process_data_format_columns(df):
    """Process data format columns"""
    # Data format columns
    format_cols = [
        'RSDP3/1', 'RSDP3/2', 'RSDP3/3', 'RSDP3/4', 'RSDP3/5', 'RSDP3/6',
        'RSDP3/7', 'RSDP3/8', 'RSDP3/9', 'RSDP3/10', 'RSDP3/11', 'RSDP3/12',
        'RSDP3/13', 'RSDP3/14', 'RSDP3/15'
    ]
    
    # Initialize data format columns
    df['dataFormats_1'] = ''
    df['dataFormats_2'] = ''
    df['dataFormats_3'] = ''
    df['dataFormats_4'] = ''
    df['dataFormats_5'] = ''
    
    # For each row, collect format names from columns that are True
    for idx, row in df.iterrows():
        format_list = []
        for col in format_cols:
            if col in df.columns and row[col] == True:
                # Map column names to format names
                format_mapping = {
                    'RSDP3/1': 'CSV',
                    'RSDP3/2': 'Excel',
                    'RSDP3/3': 'JSON',
                    'RSDP3/4': 'XML',
                    'RSDP3/5': 'HDF5',
                    'RSDP3/6': 'NetCDF',
                    'RSDP3/7': 'Binary',
                    'RSDP3/8': 'Text',
                    'RSDP3/9': 'Image',
                    'RSDP3/10': 'Video',
                    'RSDP3/11': 'Audio',
                    'RSDP3/12': 'Database',
                    'RSDP3/13': 'Archive',
                    'RSDP3/14': 'Other',
                    'RSDP3/15': 'Not specified'
                }
                format_name = format_mapping.get(col, col)
                format_list.append(format_name)
        
        # Assign up to 5 format names
        for i, format_name in enumerate(format_list[:5]):
            df.at[idx, f'dataFormats_{i+1}'] = format_name
    
    return df

def process_service_columns(df):
    """Process service-related columns"""
    # Service columns
    service_cols = [
        'SERVC1/1', 'SERVC1/2', 'SERVC1/3', 'SERVC1/4', 'SERVC1/5',
        'SERVC1/6', 'SERVC1/7', 'SERVC1/8', 'SERVC1/9'
    ]
    
    # Initialize service columns
    df['services_1'] = ''
    df['services_2'] = ''
    df['services_3'] = ''
    df['services_4'] = ''
    df['services_5'] = ''
    
    # For each row, collect service names from columns that are True
    for idx, row in df.iterrows():
        service_list = []
        for col in service_cols:
            if col in df.columns and row[col] == True:
                # Map column names to service names
                service_mapping = {
                    'SERVC1/1': 'Data Storage',
                    'SERVC1/2': 'Data Processing',
                    'SERVC1/3': 'Data Analysis',
                    'SERVC1/4': 'Data Visualization',
                    'SERVC1/5': 'Data Sharing',
                    'SERVC1/6': 'Data Archiving',
                    'SERVC1/7': 'Data Backup',
                    'SERVC1/8': 'Data Security',
                    'SERVC1/9': 'Other'
                }
                service_name = service_mapping.get(col, col)
                service_list.append(service_name)
        
        # Assign up to 5 service names
        for i, service in enumerate(service_list[:5]):
            df.at[idx, f'services_{i+1}'] = service
    
    return df

def clean_numeric_columns(df):
    """Clean numeric columns by converting to appropriate data types"""
    # Columns that should be numeric (excluding RDMPR4/_ which maps to docStructured)
    numeric_cols = [
        col for col in df.columns 
        if any(x in col for x in ['/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9', '/10'])
        and col != 'RDMPR4/_'  # This maps to docStructured (categorical)
    ]
    
    for col in numeric_cols:
        if col in df.columns:
            # Convert to numeric, coercing errors to NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Fill NaN with 0 for numeric columns
            df[col] = df[col].fillna(0)
    
    # Handle DTPUB6/1 (pubAmount) as numeric
    if 'DTPUB6/1' in df.columns:
        df['DTPUB6/1'] = pd.to_numeric(df['DTPUB6/1'], errors='coerce')
        df['DTPUB6/1'] = df['DTPUB6/1'].fillna(0)
    
    return df

def process_data():
    """Main function to process the survey data"""
    print("Loading raw survey data...")
    
    # Load the raw data
    raw_data_path = Path("survey_dashboard/data/responses_cleaned_mapped_internal_use.csv")
    df = pd.read_csv(raw_data_path)
    
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    
    # Load column mapping
    col_mapping = load_column_mapping()
    
    print("Processing research area columns...")
    df = process_research_area_columns(df)
    
    print("Cleaning boolean columns...")
    df = clean_boolean_columns(df)
    
    print("Processing software columns...")
    df = process_software_columns(df)
    
    print("Processing publication repository columns...")
    df = process_publication_repository_columns(df)
    
    print("Processing data generation method columns...")
    df = process_data_generation_method_columns(df)
    
    print("Processing data format columns...")
    df = process_data_format_columns(df)
    
    print("Processing service columns...")
    df = process_service_columns(df)
    
    print("Cleaning numeric columns...")
    df = clean_numeric_columns(df)
    
    print("Applying column mapping...")
    # Apply column mapping
    df.rename(columns=col_mapping, inplace=True)
    
    # Ensure pubAmount column is properly handled as numeric
    if 'pubAmount' in df.columns:
        # Convert pubAmount to numeric, coercing errors to NaN
        df['pubAmount'] = pd.to_numeric(df['pubAmount'], errors='coerce')
        # Fill NaN with 0
        df['pubAmount'] = df['pubAmount'].fillna(0)
    
    print("Cleaning up data...")
    # Clean up the data
    # Replace empty strings with NaN
    df = df.replace('', np.nan)
    
    # Fill NaN values appropriately
    # For categorical columns, fill with empty string
    categorical_cols = ['researchArea', 'careerLevel', 'centerAffiliation', 'yearsInResearch', 'docStructured']
    for col in categorical_cols:
        if col in df.columns:
            if col == 'docStructured':
                df[col] = df[col].fillna('Not specified')
            else:
                df[col] = df[col].fillna('')
    
    # For numeric columns, fill with 0
    numeric_cols = ['dataAmount_lsf', 'pubAmount']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    
    # For boolean columns, fill with False
    boolean_cols = [col for col in df.columns if any(x in col for x in ['software_', 'pubRepo_', 'dataGenMethod_', 'dataFormats_', 'services_'])]
    for col in boolean_cols:
        if col in df.columns:
            df[col] = df[col].fillna('')
    
    print("Saving processed data...")
    # Save the processed data
    output_path = Path("survey_dashboard/data/hmc_survey_2021_data_cleaned.csv")
    df.to_csv(output_path, index=False)
    
    print(f"Processed data saved to {output_path}")
    print(f"Final dataset: {len(df)} rows and {len(df.columns)} columns")
    
    # Print some statistics
    print("\nData Statistics:")
    print(f"Research areas: {df['researchArea'].value_counts().to_dict()}")
    print(f"Career levels: {df['careerLevel'].value_counts().to_dict()}")
    print(f"Years in research: {df['yearsInResearch'].value_counts().to_dict()}")
    
    return df

if __name__ == "__main__":
    processed_df = process_data()
    print("\nData processing completed successfully!") 