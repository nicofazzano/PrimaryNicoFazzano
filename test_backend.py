import pip._vendor.requests as request
import json

class TestBackEndPrimary():

    # Metodos de retorno de busqueda de productos por API en json
    def get_busqueda_producto_as_json(self, producto):
        url = "https://api.mercadolibre.com/sites/MLA/search?q=" + producto
        response = request.get(url=url)

        assert response.status_code == 200
        return response.json()

    def get_busqueda_detalle_producto_by_id(self, id):
        url = "https://api.mercadolibre.com/items/" + id
        response = request.get(url=url)

        assert response.status_code == 200
        return response.json()


    # Busqueda de total de productos encontrados, devueltos y limite de paginado
    def test_total_productos_encontrados(self):
        response = self.get_busqueda_producto_as_json("epiphone")

        if (response != {}):
            print("El total de productos encontrados es de:", response['paging']['total'])
        else:
            assert False, "El response esta vacio"

    def test_productos_devueltos_y_limite_de_paginado(self):
        response = self.get_busqueda_producto_as_json("epiphone")

        if (response != {}):
            print("La cantidad de productos devueltos es de:", response['paging']['primary_results'])
            if (response['paging']['limit'] == 50):
                assert True
            else:
                assert False, "El limite de paginado no es de 50, es de " + response['paging']['limit']
        else:
            assert False, "El response esta vacio"


    # Busqueda de producto por las 2 API y verificacion de match
    def test_match_producto_en_2_apis(self):
        responseProducto = self.get_busqueda_producto_as_json("epiphone")
        responseProducto = responseProducto['results'][0]

        idDelProducto = str(responseProducto['id'])
        responsePorId = self.get_busqueda_detalle_producto_by_id(idDelProducto)

        assert responseProducto['title'] == responsePorId['title'], "Los titulos no coinciden"
        assert responseProducto['price'] == responsePorId['price'], "Los precios no coinciden"
        assert responseProducto['accepts_mercadopago'] == responsePorId['accepts_mercadopago'], "La aceptacion de MercadoPago no coincide"
        assert responseProducto['currency_id'] == responsePorId['currency_id'], "Los formatos de moneda no coinciden"
        assert responseProducto['shipping']['free_shipping'] == responsePorId['shipping']['free_shipping'], "El metodo de envio gratis no coincide"
    
