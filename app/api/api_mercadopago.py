import mercadopago

sdk = mercadopago.SDK("TEST-7466495583117293-101808-8bd069ffe97cee08abf9a20a6133df24-269562008")


def link_generate(price: float, title: str, quantity: int):
    preference_data = {
        "items": [
            {
                "title": title,
                "quantity": quantity,
                "currency_id": "ARS", # Moneda (en este caso, pesos argentinos)
                "unit_price": price  # Precio del producto
            }
        ]
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    payment_link = preference["sandbox_init_point"] # Cambia a "init_point" para entorno de producción

    return payment_link
