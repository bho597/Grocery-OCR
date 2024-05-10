def receiptEntity(item) -> dict:
    """
    Convert MongoDB BSON format to Python dictionary

    #TODO: Complete docstring
    Args:
        item (_type_): _description_

    Returns:
        dict: A Python dictionary representing MongoDB item
    """    
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
    """
    Process list of receipt entities.

    #TODO: Complete docstring
    Args:
        entities (_type_): _description_

    Returns:
        list: list of receipt dictionaries
    """    
    return [receiptEntity(item) for item in entities]