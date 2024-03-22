class Exporter:
    """
    A base class for exporting data to different formats.
    """
    
    def __init__(self, filename) -> None:
        self.filename = filename

    def export(self, data):
        """
        Export data to a specific format.

        Args:
            data (pd.DataFrame): The data to export.
        """
        raise NotImplementedError("Export method must be implemented in derived classes.")
