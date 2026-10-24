def is_valid_title(title: str) -> bool:
    """
    TODO のタイトルが有効かどうかを判定する
    - 空文字はダメ
    - 空白だけもダメ
    - 100文字を超えるのもダメ
    """
    trimmed = title.strip()
    if len(trimmed) == 0:
        return False
    if len(trimmed) > 100:
        return False
    return True