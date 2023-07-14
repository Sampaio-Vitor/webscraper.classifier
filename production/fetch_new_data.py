import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar o WebDriver do Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar o navegador em segundo plano (modo headless)
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

# URL do site para extrair os dados
url = "https://www.linkedin.com/jobs/search?keywords=%28%22%28data%20Science%29%22%20OR%20%22cientista%20De%20Dados%29%22%20OR%20%22machine%20Learning%22%29&location=Brasil&locationId=&geoId=106057199&f_TPR=r86400&position=1&pageNum=0"
# Lista para armazenar os dados extraídos
data = []

# Acessar a página
driver.get(url)
wait = WebDriverWait(driver, 10)

# Tempo de espera para carregar mais trabalhos (ajuste conforme necessário)
wait_time = 3


# Rolar a página até o final máximo possível
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(wait_time)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    
# Verificar se há o botão "Ver mais vagas" e clicar nele até 30 vezes, se necessário
click_count = 0
max_clicks = 10
while click_count < max_clicks:
    show_more_jobs_button = driver.find_element(By.CSS_SELECTOR, ".infinite-scroller__show-more-button")
    if show_more_jobs_button.is_displayed():
        show_more_jobs_button.click()
        time.sleep(wait_time)
        click_count += 1
        print(click_count)
    else:
        break

# Extrair os elementos de trabalho da página
soup = BeautifulSoup(driver.page_source, "html.parser")
job_elements = soup.select(".base-card__full-link")

# Extrair os dados de cada trabalho
for element in job_elements:
    # Verificar se o elemento possui o atributo href
    if "href" not in element.attrs:
        continue

    # Obter o link do trabalho
    link = element["href"]

    # Clicar no elemento para abrir a vaga na página dinâmica
    driver.get(link)
    time.sleep(wait_time)

    # Extrair o título do trabalho
    title_element = driver.find_element(By.CSS_SELECTOR, ".top-card-layout__title")
    if title_element is not None:
        title = title_element.text.strip()
    else:
        title = ""

    # Extrair o nome da empresa
    company_element = driver.find_element(By.CSS_SELECTOR, ".topcard__org-name-link")
    if company_element is not None:
        company = company_element.text.strip()
    else:
        company = ""

    # Extrair a localização
    location_element = driver.find_element(By.CSS_SELECTOR, ".topcard__flavor--bullet")
    if location_element is not None:
        location = location_element.text.strip()
    else:
        location = ""

    # Clicar no botão "Exibir mais" para obter a descrição expandida
    show_more_button = driver.find_element(By.CSS_SELECTOR, ".show-more-less-html__button")
    if show_more_button is not None:
        show_more_button.click()
        time.sleep(wait_time)

        # Extrair a descrição expandida
        expanded_description_element = driver.find_element(By.CSS_SELECTOR, ".show-more-less-html__markup")
        if expanded_description_element is not None:
            expanded_description = expanded_description_element.text.strip()
        else:
            expanded_description = ""
    else:
        expanded_description = ""

    # Verificar se o trabalho já está na lista de dados
    job_id = link.split("/")[-1].split("?")[0]
    if any(job_id == item["ID"] for item in data):
        continue

    # Adicionar os dados à lista
    data.append({
        "ID": job_id,
        "DATA": pd.Timestamp.now().strftime("%Y-%m-%d"),
        "TITULO": title,
        "EMPRESA": company,
        "LOCAL": location,
        "LINK": link,
        "DESCRICAO": expanded_description
    })

    # Converter a lista de dados em um DataFrame do Pandas
    df = pd.DataFrame(data)
    
    # Exibir uma amostra do DataFrame
    print(df.sample())

    # Salvar os dados em um arquivo CSV
    df.to_csv("newly_fetched_data.csv", index=False)

# Exibir uma amostra do DataFrame
print(df.sample(5))

# Fechar o WebDriver
driver.quit()
