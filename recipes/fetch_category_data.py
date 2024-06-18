import requests
import json

API_KEY = "1046289489798689204"
CATEGORY_LIST_API_URL = "https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426"

def fetch_category_list(api_key):
    params = {
        "applicationId": api_key
    }
    response = requests.get(CATEGORY_LIST_API_URL, params=params)
    response.encoding = 'utf-8'  # エンコーディングをUTF-8に設定
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}")

def main():
    categories = fetch_category_list(API_KEY)
    with open('categories.json', 'w', encoding='utf-8') as f:
        json.dump(categories, f, indent=4, ensure_ascii=False)
    print("Category list fetched and saved to 'categories.json'")

if __name__ == "__main__":
    main()
