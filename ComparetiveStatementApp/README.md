### Comparative Statement App

The Comparative Statement App is a specialized business tool designed to streamline the tender evaluation process. It efficiently reads multiple Excel files submitted by different bidders, performs sophisticated data processing, and aggregates this data to produce a comprehensive final report. This process involves concatenating data from various files into a single DataFrame, manipulating columns (such as dropping and renaming), and applying one-hot encoding to supplier information for easier analysis. The app uniquely structures the data to present parts or objects in rows with corresponding suppliers and their bids in columns, alongside a dedicated column for the minimum bid and the supplier offering it. This organization facilitates a clear, unified view of all bids, highlighting the most competitive offers for each item. The final report, which emphasizes the lowest bids with red text and double underlining for immediate visibility, can be exported in either Excel or PDF format. Tailored for a specific business use case, this application stands as a prime example of custom development to meet precise tender analysis needs, now shared on GitHub as a code sample for an internship application with Major League Hacking.

#### How to Use

1. Launch the application and click on the "Open Files" button to select the Excel files containing bid data you wish to analyze.
2. The app automatically initiates data processing upon file selection, consolidating information into a single, manageable format.
3. After processing, choose your preferred report format (Excel or PDF) and click the "Save" button that appears. This will generate your comprehensive report, clearly highlighting the most competitive bids for easy comparison and decision-making.

#### Requirements

- Python 3.8 or higher is required to ensure smooth operation.
- The following Python libraries must be installed:
  - `pandas` for data manipulation and analysis.
  - `reportlab` for generating PDF reports.
  - `Pillow` (PILLOW) for image processing capabilities, enhancing report presentation.

This README now provides a more thorough understanding of the app's purpose, functionality, and usage, making it clearer for potential users or reviewers, especially in the context of demonstrating your coding capabilities for the internship application.
