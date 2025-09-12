def test_create_order(client, customer_token, admin_token):
    # First create a product as admin
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    product_response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "price": 29.99,
            "stock_quantity": 100
        },
        headers=admin_headers
    )
    product_id = product_response.json()["id"]
    
    # Create order as customer
    customer_headers = {"Authorization": f"Bearer {customer_token}"}
    response = client.post(
        "/orders/",
        json={
            "shipping_address": "123 Test St",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2
                }
            ]
        },
        headers=customer_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["shipping_address"] == "123 Test St"
    assert len(data["order_items"]) == 1


def test_get_my_orders(client, customer_token):
    headers = {"Authorization": f"Bearer {customer_token}"}
    response = client.get("/orders/my-orders", headers=headers)
    assert response.status_code == 200