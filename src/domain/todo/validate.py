from typing import Any

def is_valid_title(title: str) -> bool:
    # trim() の代わりに strip() を使用
    trimmed = title.strip()
    
    if len(trimmed) == 0:
        return False
        
    if len(trimmed) > 100:
        return False
        
    return True

def validate_title(raw_title: Any) -> str:
    # typeof rawTitle !== "string" に相当
    if not isinstance(raw_title, str):
        raise ValueError("タイトルは必須です")
        
    trimmed = raw_title.strip()
    
    if len(trimmed) == 0:
        # throw new Error に相当
        raise ValueError("タイトルは必須です")
        
    if len(trimmed) > 100:
        raise ValueError("タイトルは100文字以内にしてください")
        
    return trimmed