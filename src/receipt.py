import re
class Receipt:
    def __init__(
        self, 
        receipt_content=None, 
        merchant_name=None, merchant_name_confidence=None,
        transaction_date=None, transaction_date_confidence=None,
        tax=None, tax_confidence=None,
        total=None, total_confidence=None,
        items=None,
        CONFIDENCE_THRESHOLD=0.8,
    ):
        self.receipt_content = receipt_content
        self.CONFIDENCE_THRESHOLD = CONFIDENCE_THRESHOLD

        self.merchant_name = merchant_name
        self.merchant_name_confidence = merchant_name_confidence

        self.transaction_date = transaction_date
        self.transaction_date_confidence = transaction_date_confidence

        self.tax = tax
        self.tax_confidence = tax_confidence

        self.total = total
        self.total_confidence = total_confidence

        self.items = items

    def display_receipt(self):
        print(f"Merchant Name: {self.merchant_name}")
        print(f"Transaction Date: {self.transaction_date}")
        print(f"Tax: ${self.tax}")
        print(f"Total: ${self.total}")
        print("\nItems:")
        for i, item in enumerate(self.items):
            print(f'Item {i+1}: {item["item_description"]}')
            print(f'     Item confidence: {item["item_description_confidence"]}')
            print(f'     Total Price: {item["item_total_price"]}')
            print(f'     Total Price Confidence: {item["item_total_price_confidence"]}')



class BerkeleyBowlReceipt(Receipt):
    def __init__(self, receipt_content, merchant_name, merchant_name_confidence,
                 transaction_date, transaction_date_confidence, tax, tax_confidence,
                 total, total_confidence, items, CONFIDENCE_THRESHOLD=0.8):
        super().__init__(
            receipt_content, merchant_name, merchant_name_confidence,
            transaction_date, transaction_date_confidence, tax, tax_confidence,
            total, total_confidence, items, CONFIDENCE_THRESHOLD
        )
        self.__preprocess_receipt__()

    
    def __preprocess_receipt__(self):
        receipt_lines = self.receipt_content.split('\n')

        # for item in self.items:
        #     print(receipt_lines.index(item['item_description']))
        


    
