import string
import pandas as pd

from exporters import Exporter


class ExcelExporter(Exporter):
    """
    A class for exporting data to an Excel file.
    """

    def export(self, data):
        """
        Export data to an Excel file.

        Args:
            data (pd.DataFrame): The data to export.
        """
        data.index += 1
        writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
        data.to_excel(writer, sheet_name='Sheet1', index_label='SER', header=True)

        workbook = writer.book
        cell_format = workbook.add_format()
        cell_format.set_font_color('red')
        cell_format.set_underline(2)
        worksheet = writer.sheets['Sheet1']

        for index, row in data.iterrows():
            worksheet.write(self.get_cell_name(data, row['Supplier'], index), row[row['Supplier']], cell_format)
        writer.close()

    def get_cell_name(self, df, col_name, row_index):
        """
        We are supposed to modify few cells and this function returns the name of the cell based on the row & column of the data frame

        Args:
            data (pd.DataFrame): The data to export.
            col_name (str): The name of the column to get col index from df 
            row_index (int): The index of the row
        """
        d = dict(zip(range(25), list(string.ascii_uppercase)[1:]))
        excel_header = str(d[df.columns.get_loc(col_name)])
        return f'{excel_header}{row_index+1}'

    def export_with_single_underscore(self, data):
        """
        Export data to an Excel file. If we don't need double underscore, we can simple export the data.

        Args:
            data (pd.DataFrame): The data to export.
        """
        data.index += 1
        data = data.style.apply(self.cell_format, axis=1)
        data.to_excel('output.xlsx', index_label='SER', engine='xlsxwriter')

    def cell_format(self, row):
        """
        Apply cell formatting to a DataFrame row.

        Args:
            row (pd.Series): A row of the DataFrame.

        Returns:
            list: A list of cell formatting settings for each cell in the row.
        """
        return ['color:red; text-decoration: red double underline;' if key == row['Supplier'] else '' for key, value in row.items()]
