import requests

# FastAPIのデフォルトポート（8000）に合わせています
API_URL = "http://127.0.0.1:8000/api/todos"

# 以降のテストで使うためにIDを保存する変数
target_id = None

def test_1_post_create_todo():
    global target_id
    # fetchの代わりに requests.post(URL, json=データ) を使います
    response = requests.post(API_URL, json={"title": "テストタスク"})
    
    # expect(A).toBe(B) は assert A == B と書きます
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == "テストタスク"
    assert data["done"] is False
    
    target_id = data["id"]

def test_2_get_todos():
    response = requests.get(API_URL)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)  # Array.isArray(data) に相当
    
    # 追加したIDを持つTODOが一覧に含まれているか
    found = next((todo for todo in data if todo["id"] == target_id), None)
    assert found is not None

def test_3_put_update_todo():
    response = requests.put(f"{API_URL}/{target_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["done"] is True

def test_4_delete_todo():
    response = requests.delete(f"{API_URL}/{target_id}")
    assert response.status_code == 200

def test_5_validation_error():
    # 空白のみの不正なデータ
    response = requests.post(API_URL, json={"title": "   "})
    
    # サーバー側のバリデーションが機能していれば 400 になる
    assert response.status_code == 400
    
    data = response.json()
    # FastAPIのHTTPExceptionは "error" ではなく "detail" というキーで返します
    assert data["detail"] == "タイトルは1〜100文字で入力してください"