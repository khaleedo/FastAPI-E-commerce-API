def test_create_product(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "A test product",
            "price": 29.99,
            "stock_quantity": 100,
            "category": "Electronics"
        },
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == "29.99"


def test_get_products(client, admin_token):
    # Create a product first
    headers = {"Authorization": f"Bearer {admin_token}"}
    client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "A test product",
            "price": 29.99,
            "stock_quantity": 100
        },
        headers=headers
    )
    
    # Get products
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_create_product_unauthorized(client, customer_token):
    headers = {"Authorization": f"Bearer {customer_token}"}
    response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "price": 29.99,
            "stock_quantity": 100
        },
        headers=headers
    )
    assert response.status_code == 403