# backend/services/parser.py
from typing import Optional

def parse_inventory_message(message_text: str) -> Optional[dict]:
    """
    Message-ai parse seiyum function.
    Example input: 'Mi 15, Compo, 1500, Imran'
    """
    # Comma-vai vaithu pirithu, spaces-ai remove seiyum
    parts = [part.strip() for part in message_text.split(",")]
    
    # Sariyaaga 4 parts (Item, Category, Price, Customer) irukka ena check seiyum
    if len(parts) == 4:
        try:
            # Price oru number-aa ena check seiyum
            price = int(parts[2])
            return {
                "item_name": parts[0],
                "category": parts[1],
                "price": price,
                "customer_name": parts[3]
            }
        except ValueError:
            # Price number-aaga illaiyendral, ithu normal chat message
            return None
            
    # 4 parts illaiyendral, ithuvum normal chat message thaan
    return None
