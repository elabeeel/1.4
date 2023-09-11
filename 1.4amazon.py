from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

def buscar_productos_en_amazon(producto, numero_de_paginas=1):
    driver = webdriver.Chrome(executable_path='C:/Users/lange/Downloads/chromedriver')

    nombres = []
    ratings = []
    precios = []
    fechas_de_entrega = []

    try:
        driver.get('https://www.amazon.com.mx/')

        for pagina in range(1, numero_de_paginas + 1):
            search_box = driver.find_element_by_id('twotabsearchtextbox')
            search_box.clear()
            search_box.send_keys(producto)
            search_box.send_keys(Keys.ENTER)

            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            resultados = soup.find_all('div', {'data-component-type': 's-search-result'})

            for resultado in resultados:
                nombre = resultado.find('span', {'class': 'a-text-normal'}).text
                nombres.append(nombre)

                rating_element = resultado.find('span', {'class': 'a-icon-alt'})
                rating = rating_element.text if rating_element else 'N/A'
                ratings.append(rating)

                precio_element = resultado.find('span', {'class': 'a-offscreen'})
                precio = precio_element.text if precio_element else 'N/A'
                precios.append(precio)

                fecha_element = resultado.find('span', {'class': 'a-text-secondary'})
                fecha_entrega = fecha_element.text if fecha_element else 'N/A'
                fechas_de_entrega.append(fecha_entrega)

            if pagina < numero_de_paginas:
                next_button = driver.find_element_by_partial_link_text('Next')
                next_button.click()
                time.sleep(2)

    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")

    finally:
        driver.quit()

    data = {
        'Nombre del Producto': nombres,
        'Rating': ratings,
        'Precio': precios,
        'Fecha de Entrega': fechas_de_entrega
    }
    df = pd.DataFrame(data)

    df.to_csv('productos_amazon.csv', index=False)

    return df

productos_df = buscar_productos_en_amazon('Perfume creed', numero_de_paginas=3)
print(productos_df)