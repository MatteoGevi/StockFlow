from typing import Dict, List, Optional
import os
from frappeclient import FrappeClient
from dotenv import load_dotenv

load_dotenv(override=True)

class ERPNextClient:
    def __init__(self):
        """Initialize ERPNext client with configuration from environment variables."""
        self.url = os.getenv('ERPNEXT_URL')
        self.username = os.getenv('ERPNEXT_USERNAME')
        self.password = os.getenv('ERPNEXT_PASSWORD')
        self.client = FrappeClient(
            url=self.url,
            username=self.username,
            password=self.password
        )

    def get_inventory(self, warehouse: Optional[str] = None) -> List[Dict]:
        """
        Retrieve inventory data from ERPNext.
        
        Args:
            warehouse: Optional warehouse code to filter inventory
            
        Returns:
            List of dictionaries containing inventory data
        """
        try:
            filters = {"warehouse": warehouse} if warehouse else {}
            
            # Get bin (inventory) data
            bins = self.client.get_list(
                "Bin",
                filters=filters,
                fields=["item_code", "warehouse", "actual_qty", "projected_qty"]
            )
            
            # Enrich with item details
            inventory_data = []
            for bin_item in bins:
                item = self.client.get_doc("Item", bin_item["item_code"])
                inventory_data.append({
                    "item_code": bin_item["item_code"],
                    "warehouse": bin_item["warehouse"],
                    "quantity": bin_item["actual_qty"],
                    "projected_quantity": bin_item["projected_qty"],
                    "item_name": item.get("item_name"),
                    "item_group": item.get("item_group"),
                    "uom": item.get("stock_uom")
                })
            
            return inventory_data
            
        except Exception as e:
            raise Exception(f"Failed to retrieve inventory data: {str(e)}")

    def get_purchase_orders(self, status: Optional[str] = None) -> List[Dict]:
        """
        Retrieve purchase orders from ERPNext.
        
        Args:
            status: Optional status to filter purchase orders
            
        Returns:
            List of dictionaries containing purchase order data
        """
        try:
            filters = {"status": status} if status else {}
            
            purchase_orders = self.client.get_list(
                "Purchase Order",
                filters=filters,
                fields=["name", "supplier", "transaction_date", "grand_total", "status"]
            )
            
            # Enrich with items
            for po in purchase_orders:
                po_doc = self.client.get_doc("Purchase Order", po["name"])
                po["items"] = [
                    {
                        "item_code": item.get("item_code"),
                        "qty": item.get("qty"),
                        "rate": item.get("rate"),
                        "amount": item.get("amount"),
                        "expected_delivery_date": item.get("expected_delivery_date")
                    }
                    for item in po_doc.get("items", [])
                ]
            
            return purchase_orders
            
        except Exception as e:
            raise Exception(f"Failed to retrieve purchase orders: {str(e)}")

    def create_purchase_order(self, supplier: str, items: List[Dict], 
                            schedule_date: str) -> Dict:
        """
        Create a new purchase order in ERPNext.
        
        Args:
            supplier: Supplier code/name
            items: List of items with quantities and rates
            schedule_date: Expected delivery date
            
        Returns:
            Dictionary containing the created purchase order details
        """
        try:
            po_doc = {
                "doctype": "Purchase Order",
                "supplier": supplier,
                "schedule_date": schedule_date,
                "items": [
                    {
                        "item_code": item["item_code"],
                        "qty": item["quantity"],
                        "rate": item.get("rate", 0),
                        "schedule_date": schedule_date
                    }
                    for item in items
                ]
            }
            
            result = self.client.insert(po_doc)
            return result
            
        except Exception as e:
            raise Exception(f"Failed to create purchase order: {str(e)}")

    def get_stock_balance(self, item_code: str, 
                         warehouse: Optional[str] = None) -> Dict:
        """
        Get current stock balance for an item.
        
        Args:
            item_code: Item code to check
            warehouse: Optional warehouse to filter
            
        Returns:
            Dictionary containing stock balance information
        """
        try:
            filters = {
                "item_code": item_code,
                "warehouse": warehouse
            } if warehouse else {"item_code": item_code}
            
            balance = self.client.get_list(
                "Bin",
                filters=filters,
                fields=["actual_qty", "projected_qty", "reserved_qty", "ordered_qty"]
            )
            
            return balance[0] if balance else {
                "actual_qty": 0,
                "projected_qty": 0,
                "reserved_qty": 0,
                "ordered_qty": 0
            }
            
        except Exception as e:
            raise Exception(f"Failed to get stock balance: {str(e)}") 