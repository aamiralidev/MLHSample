from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import pandas as pd

from exporters import Exporter

class PDFExporter(Exporter):
    """
    A class for exporting data to a PDF file.
    """

    def export(self, data):
        """
        Export data to a PDF file.

        Args:
            data (pd.DataFrame): The data to export.
        """
        data = data.replace(pd.NA, '')
        
        # Specify the custom PDF width and height (adjust as needed)
        custom_width, custom_height = 2000, 1000  # Width is increased to fit data

        # Create a PDF document with custom dimensions
        pdf_filename = self.filename
        pdf = SimpleDocTemplate(pdf_filename, pagesize=(custom_width, custom_height), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

        # Create a Table for your data
        table_data = []
        table_data.append(data.columns.tolist())  # Header row
        for row in data.values:
            table_data.append(row.tolist())

        # Define the style for the table
        style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header row padding
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Table body background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Gridlines
        ]

        # Get the index of the minimum value in each row
        min_value_indices = data.apply(self.get_min_cell_no, axis=1)

        # Create a list to store cell formatting for the minimum value cell
        cell_formatting = []

        # Iterate over rows to format the cell with the minimum value
        for row_index, min_col in enumerate(min_value_indices):
            cell_format = [
                ('TEXTCOLOR', (min_col, row_index + 1), (min_col, row_index + 1), colors.red),  # Red text color for min value cell
                ('FONTNAME', (min_col, row_index + 1), (min_col, row_index + 1), 'Helvetica-Bold'),
            ]

            cell_formatting.extend(cell_format)
        # Create the table and apply the style and cell formatting
        table = Table(table_data)
        table.setStyle(TableStyle(style + cell_formatting))

        # Build the PDF document
        elements = []
        elements.append(table)

        pdf.build(elements) 
    
    def get_min_cell_no(self, row):
        for index, (key, _) in enumerate(row.items()):
            if key == row['Supplier']:
                return index 
