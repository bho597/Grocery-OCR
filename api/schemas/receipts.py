def receiptEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "filename": str(item["filename"]),
        "merchant_name": str(item["merchant_name"]),
        "receipt_date": str(item["receipt_date"]),
        "image_url": str(item["image_url"]),
        "transaction_date": str(item["transaction_date"]),
        "transaction_time": str(item["transaction_time"]),
        "modified_date": str(item["modified_date"]),
        "textracted": bool(item["textracted"]),
        "verified": bool(item["verified"]),
    }

def receiptEntities(entities) -> list:
    return [receiptEntity(item) for item in entities]