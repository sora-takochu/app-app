from test_validate import is_valid_title  # todo.py から関数を読み込む

def test_valid_title_normal():
    # 普通のタイトルは True
    assert is_valid_title("牛乳を買う") == True

def test_valid_title_empty():
    # 空文字は False
    assert is_valid_title("") == False

def test_valid_title_whitespace_only():
    # 空白だけは False
    assert is_valid_title("   ") == False

def test_valid_title_over_100():
    # 100文字を超えると False
    long_title = "あ" * 101
    assert is_valid_title(long_title) == False

def test_valid_title_exactly_100():
    # 100文字ちょうどは True
    max_title = "あ" * 100
    assert is_valid_title(max_title) == True