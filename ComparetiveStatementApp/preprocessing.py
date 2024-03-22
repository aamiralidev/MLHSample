import pandas as pd 


class DataProcessor:
    """
    A class responsible for processing and aggregating data from multiple DataFrames.
    """

    def process_data(self, df_dict):
        """
        Process and aggregate data from multiple DataFrames.

        Args:
            df_dict (dict): A dictionary of DataFrames.

        Returns:
            pd.DataFrame: The processed and aggregated DataFrame.
        """

        ### concatinating all the data frames so we have rows from all of them
        output = pd.concat(df_dict.values(), ignore_index=True)

        ### removing last 2 columns since those were NaN and kind of noise
        output = output.drop(columns=output.columns[-2:])

        ### renaming columns as these are required in the expected output 
        output = output.rename(columns={'PART NO': 'CAT PART NO', 'A/U': 'UOM', 'PRODUCTION STATUS': 'PROD STATUS'})

        ### we divide supplier class into multiple columns and under the supplier we put the value provided by that supplier
        df_encoded = pd.get_dummies(output['Supplier'], prefix='', prefix_sep='').apply(lambda x: x * output['RATE'])

        ### replacing Supplier column with all the encoded columns
        output = pd.concat([output.drop(columns='Supplier'), df_encoded], axis=1)

        ### droping RATE as it is available now under supplier name columns, also droping serial number 
        output = output.drop(columns=['RATE', 'SER'])

        ### for rate column, we are aggregating at sum considering that a supplier has provided a single rate 
        ### for particular part in a particular region and a particular brand so in whole group, we only have 
        ### value in a single row for a particular supplier
        columns_to_sum = {column: 'sum' for column in df_dict.keys()}

        ### for the columns that have not been used in groupby must be aggregated, we assume they have same value in all columns hence using first
        columns_to_sum.update({'NOMEN': 'first', 'PROD STATUS': 'first', 'Spare Type': 'first', 'UOM': 'first'})

        output = output.groupby(['CAT PART NO', 'COO', 'BRAND']).agg(columns_to_sum).reset_index()

        ### keys consist of columns in dataframe that represents suppliers while others represent part attributes
        keys = [column for column in df_dict.keys()]
        cols = ['CAT PART NO', 'NOMEN', 'UOM', 'PROD STATUS', 'Supplier', 'Spare Type', 'COO', 'BRAND'] + keys + ['RATE']

        def get_supplier_name(x, cols=keys):
            for col in cols:
                if x[col] == x['RATE']:
                    return col
            return pd.NA

        ### in each row, for all suppliers, put min rate in RATE column
        output['RATE'] = output.apply(lambda x: min(filter(lambda x: x != 0, x[keys].values), default=0), axis=1)

        ### put supplier with min rate in Supplier column
        output['Supplier'] = output.apply(get_supplier_name, axis=1)

        ### 0 shows as it is in excel and other formats while pd.NA is shown as white space
        ### dropping rows that have null rate as supplier has not provided a rate for that part
        output = output[cols].replace(0, pd.NA).dropna(subset=['RATE']).reset_index()

        ### reset index adds an extra index column in df other then index itself so droping that
        output = output.drop(columns=['index'])

        return output

