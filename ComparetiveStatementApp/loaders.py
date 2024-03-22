import os
import pandas as pd 

class FileLoader:
    """
    A class responsible for loading and preprocessing input Excel files.
    """

    def convert_to_float(self, value):
        """
        Convert a value to an integer or return 0 if it's not a valid number.

        Args:
            value (str): The input value to convert.

        Returns:
            int: The converted integer value or 0 if conversion fails.
        """
        try:
            return float(value)
        except ValueError:
            return 0

    def load(self, files):
        """
        Load and process input Excel files.

        Args:
            files (list): A list of file paths to load.

        Returns:
            dict: A dictionary of DataFrames, where each key is the filename.
        """
        df_dict = {}
        for file in files:
            try:
                filename = os.path.splitext(os.path.basename(file))[0]
                df = pd.read_excel(file, sheet_name='2.2', skiprows=1, converters={'RATE': self.convert_to_float})
                df['Supplier'] = filename
                df['Spare Type'] = 'After Mkt'
                df_dict[filename] = df
            except:
                pass
        return df_dict