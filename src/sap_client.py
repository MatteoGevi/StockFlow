from typing import Dict, List, Optional
import os
from pyrfc import Connection
from dotenv import load_dotenv

load_dotenv(override=True)

SAP_SYSNR=00
SAP_CLIENT=100

class SAPClient:
    def __init__(self):
        self.conn = None
        self._connect()

    def _connect(self) -> None:
        """Establish connection to SAP system using credentials from environment variables."""
        try:
            self.conn = Connection(
                ashost=os.getenv('SAP_ASHOST'),
                sysnr=os.getenv('SAP_SYSNR'),
                client=os.getenv('SAP_CLIENT'),
                user=os.getenv('SAP_USER'),
                passwd=os.getenv('SAP_PASSWORD')
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to SAP: {str(e)}")

    def get_inventory(self, plant: Optional[str] = None) -> List[Dict]:
        """
        Retrieve inventory data from SAP.
        
        Args:
            plant: Optional plant code to filter inventory
            
        Returns:
            List of dictionaries containing inventory data
        """
        try:
            # Example RFC call to get inventory data
            # You'll need to replace this with your actual SAP function module
            result = self.conn.call('BAPI_MATERIAL_GET_INVENTORY',
                                  MATERIAL='',
                                  PLANT=plant)
            
            # Process and format the result
            inventory_data = []
            for item in result.get('INVENTORY_DATA', []):
                inventory_data.append({
                    'material_code': item.get('MATERIAL'),
                    'plant': item.get('PLANT'),
                    'storage_location': item.get('STORAGE_LOCATION'),
                    'quantity': item.get('QUANTITY'),
                    'unit': item.get('UNIT'),
                    'batch': item.get('BATCH')
                })
            
            return inventory_data
            
        except Exception as e:
            raise Exception(f"Failed to retrieve inventory data: {str(e)}")

    def close(self) -> None:
        """Close the SAP connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 