from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as chains
from selenium.common.exceptions import StaleElementReferenceException


class TestFrontEndPrimary():

    # Webdriver setup y metodos de busqueda de categorias y asserts
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def buscar_categoria(self, categoria, subcategoria):
        driver = self.driver
        actions = chains(driver)
        categorias = driver.find_element_by_class_name("nav-menu-categories-link")
        actions.move_to_element(categorias).perform()
        subCat = driver.find_element_by_xpath('//a[contains(text(), "' + categoria + '")]')
        actions.move_to_element(subCat).perform()
        subCat2 = driver.find_element_by_xpath('//a[contains(text(), "' + subcategoria + '")]').click()

    def assert_categoria_y_retornar_total_resultados(self, categoria):
        driver = self.driver
        if (driver.find_element_by_class_name("quantity-results").text is not None):
            print("La cateogoria buscada contiene", driver.find_element_by_class_name("quantity-results").text)
        else:
            print("La categoria no contiene resultados")
        if (driver.find_element_by_class_name("breadcrumb__title").text == categoria):
            assert True
        else:
            assert False, "No se ingreso a la categoria buscada"
    

    # Ejericio 1 de FrontEnd
    def test_buscar_climatizacion(self):
        driver = self.driver
        driver.get("https://www.mercadolibre.com.ar")

        self.buscar_categoria("Hogar y Electrodomésticos", "Climatización")
        self.assert_categoria_y_retornar_total_resultados("Climatización")

        driver.quit()

    def test_buscar_celulares_y_smartphones(self):
        driver = self.driver
        driver.get("https://www.mercadolibre.com.ar")

        self.buscar_categoria("Tecnología", "Celulares y Smartphones")
        self.assert_categoria_y_retornar_total_resultados("Celulares y Smartphones")

        driver.quit()

    def test_buscar_industria_textil(self):
        driver = self.driver
        driver.get("https://www.mercadolibre.com.ar")

        self.buscar_categoria("Herramientas e Industrias", "Industria Textil")
        self.assert_categoria_y_retornar_total_resultados("Industria Textil")

        driver.quit()

    def test_buscar_cuarto_del_bebe(self):
        driver = self.driver
        driver.get("https://www.mercadolibre.com.ar")

        self.buscar_categoria("Juguetes y Bebés", "Cuarto del Bebé")
        self.assert_categoria_y_retornar_total_resultados("Cuarto del Bebé")

        driver.quit()


    # Ejericio 2 de FrontEnd
    def test_match_titulo_precio_en_publicacion(self):
        driver = self.driver
        driver.get("https://www.mercadolibre.com.ar")

        self.buscar_categoria("Tecnología", "Accesorios para Celulares")

        listaDeCiudades = driver.find_elements_by_css_selector("[id='id_state'] dd")
        try:
            for i in listaDeCiudades:
                if ("Capital Federal" in i.text):
                    i.click()
        except StaleElementReferenceException as e:
            pass

        tituloEnLista = driver.find_element_by_css_selector("[id='results-section'] [class='results-item highlighted article stack product ']:nth-child(1) [class='item__title list-view-item-title'] span").text
        precioEnLista = driver.find_element_by_css_selector("[id='results-section'] [class='results-item highlighted article stack product ']:nth-child(1) [class='price__fraction']").text
        
        driver.find_element_by_css_selector("[id='results-section'] [class='results-item highlighted article stack product ']:nth-child(1) [class='item__title list-view-item-title'] span").click()

        tituloEnPublicacion = driver.find_element_by_css_selector("[class='ui-pdp-container__col col-3 pb-40'] [class='ui-pdp-title']").text
        precioEnPublicacion = driver.find_element_by_css_selector("[class='ui-pdp-container__col col-3 pb-40'] [class='ui-pdp-price__second-line'] [class='price-tag-fraction']").text

        assert tituloEnLista == tituloEnPublicacion, "Los titulos de los productos no son iguales"
        assert precioEnLista == precioEnPublicacion, "Los precios de los productos no son iguales"

        driver.quit()  
