import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        print("API fetch successful. Products fetched:", len(products))

        simplified_products = []

        for product in products:
            simplified_products.append({
                "id": product.get("id"),
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "price": product.get("price"),
                "rating": product.get("rating")
            })

        return simplified_products

    except Exception as e:
        print("API fetch failed:", e)
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Returns: dictionary mapping product IDs to info
    """

    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")

        product_mapping[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_mapping
