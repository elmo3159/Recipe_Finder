import requests
import json
import time

API_KEY = "1046289489798689204"
CATEGORY_LIST_FILE = 'categories.json'
RECIPE_API_URL = "https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426"

def fetch_recipes(category_id, api_key):
    params = {
        "applicationId": api_key,
        "categoryId": category_id
    }
    for attempt in range(5):  # 最大5回の再試行
        response = requests.get(RECIPE_API_URL, params=params)
        response.encoding = 'utf-8'  # エンコーディングをUTF-8に設定
        print(f"Request URL: {response.url}")  # リクエストURLを表示
        print(f"Status Code: {response.status_code}")  # ステータスコードを表示
        if response.status_code == 200:
            try:
                response_json = response.json()
                print(f"Response JSON for category ID {category_id}: {json.dumps(response_json, ensure_ascii=False, indent=2)}")  # レスポンスの詳細を表示
                return response_json
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON for category {category_id}: {e}")
                print(f"Response Content: {response.content[:500]}")  # エラー時のレスポンス内容を表示
                return None
        elif response.status_code == 429:
            print(f"Rate limit exceeded for category {category_id}. Retrying in 30 seconds.")
            time.sleep(30)  # レートリミットに達した場合、30秒待機して再試行
        else:
            print(f"Failed to fetch recipes for category {category_id} with status code {response.status_code}")
            print(f"Response Content: {response.content[:500]}")  # エラー時のレスポンス内容を表示
            if 'error' in response.json():
                error_message = response.json()['error']
                print(f"Error message: {error_message}")
            return None

    return None  # 最大再試行回数を超えた場合

def main():
    with open(CATEGORY_LIST_FILE, 'r', encoding='utf-8') as f:
        categories = json.load(f)
    
    print(f"Loaded categories: {len(categories['result']['large'])} large categories")

    all_recipes = []

    # Large categories
    large_categories = categories['result']['large']
    medium_categories = categories['result']['medium']
    small_categories = categories['result']['small']

    for large in large_categories:
        large_id = str(large['categoryId'])
        print(f"Processing large category: {large['categoryName']} ({large_id})")
        for medium in medium_categories:
            if medium['parentCategoryId'] == large_id:
                medium_id = str(medium['categoryId'])
                print(f"  Processing medium category: {medium['categoryName']} ({medium_id})")
                for small in small_categories:
                    if small['parentCategoryId'] == medium_id:
                        small_id = str(small['categoryId'])
                        category_id = f"{large_id}-{medium_id}-{small_id}"
                        print(f"    Fetching recipes for category ID: {category_id}")
                        recipes = fetch_recipes(category_id, API_KEY)
                        if recipes and 'result' in recipes:
                            all_recipes.extend(recipes['result'])
                            print(f"    Recipes found for category ID {category_id}: {len(recipes['result'])}")
                        else:
                            print(f"    No recipes found or 'result' not in response for category ID {category_id}")
                        time.sleep(1)  # API rate limitを考慮して1秒の遅延を入れる

    with open('recipes.json', 'w', encoding='utf-8') as f:
        json.dump(all_recipes, f, indent=4, ensure_ascii=False)
    print(f"Total recipes fetched: {len(all_recipes)}")

if __name__ == "__main__":
    main()
