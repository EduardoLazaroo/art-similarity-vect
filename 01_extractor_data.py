import csv
import os
import requests
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time
from selenium.webdriver.chrome.options import Options
from config import DB_CONFIG

def extrair_urls_do_csv(caminho_csv):
    urls = set()
    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        leitor = csv.reader(csvfile)
        for linha in leitor:
            for item in linha:
                item = item.strip()
                if item.startswith("http://") or item.startswith("https://"):
                    urls.add(item)
    return list(urls)

def baixar_imagem(url_img, nome_imagem):
    pasta_imgs = "imgs"
    if not os.path.exists(pasta_imgs):
        os.makedirs(pasta_imgs)
    
    caminho_arquivo = os.path.join(pasta_imgs, nome_imagem)

    try:
        response = requests.get(url_img, timeout=10)
        if response.status_code == 200:
            with open(caminho_arquivo, 'wb') as f:
                f.write(response.content)
            return True
    except:
        pass
    return False

def url_ja_foi_processada(conn, url):
    cur = conn.cursor()
    cur.execute("SELECT id FROM urls WHERE url = %s", (url,))
    resultado = cur.fetchone()
    cur.close()
    return resultado[0] if resultado else None

def salvar_url_e_pegar_id(conn, url, nome_imagem):
    cur = conn.cursor()
    cur.execute("INSERT INTO urls (url, nome_imagem) VALUES (%s, %s)", (url, nome_imagem))
    conn.commit()
    id_novo = cur.lastrowid
    cur.close()
    return id_novo

def salvar_info(conn, registro_id, chave, valor):
    cur = conn.cursor()
    cur.execute(""" 
        INSERT INTO informacoes_extraidas (registro_id, chave, valor) 
        VALUES (%s, %s, %s) 
    """, (registro_id, chave, valor))
    conn.commit()
    cur.close()

def extrair_info_da_url(driver, conn, url, contador):
    print(f"\n🌐 Acessando: {url}")
    
    registro_id = url_ja_foi_processada(conn, url)
    if registro_id:
        print("⚠️ URL já processada. Pulando.")
        return

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 5)

        nome_imagem = f"{contador:02d}.png"
        try:
            img_element = wait.until(
                EC.presence_of_element_located((By.XPATH, "/html/body/section[2]/div/div/div[2]/div[1]/figure/div[1]/img"))
            )
            img_url = img_element.get_attribute("src")
            if not baixar_imagem(img_url, nome_imagem):
                print("⚠️ Imagem não baixada. Pulando.")
                return
            print(f"📸 Imagem salva: {nome_imagem}")
        except:
            print("⚠️ Imagem não encontrada. Pulando.")
            return

        registro_id = salvar_url_e_pegar_id(conn, url, nome_imagem)

        info_div = driver.find_element(By.XPATH, "/html/body/section[3]/div/div/section[1]/div")
        paragrafos = info_div.find_elements(By.TAG_NAME, "p")

        for p in paragrafos:
            spans = p.find_elements(By.TAG_NAME, "span")
            if len(spans) >= 2:
                chave = spans[0].text.strip()
                valor = spans[1].text.strip()
                salvar_info(conn, registro_id, chave, valor)
                print(f"🔹 {chave} -> {valor}")

        print("✅ URL processada com sucesso.")

    except Exception as e:
        print(f"❌ Erro ao processar {url}: {e}")

def processar_urls(lista_de_urls, conn, driver):
    contador = 1
    for url in lista_de_urls:
        extrair_info_da_url(driver, conn, url, contador)
        contador += 1

if __name__ == "__main__":
    arquivo_csv = "data.csv"
    print("📁 Lendo arquivo CSV...")

    lista_de_urls = extrair_urls_do_csv(arquivo_csv)
    print(f"🔍 {len(lista_de_urls)} URL(s) únicas encontradas.")

    conn = mysql.connector.connect(**DB_CONFIG)

    chrome_options = Options()
    chrome_options.add_argument("--headless")  #Ativar
    chrome_options.add_argument("--no-sandbox")  # Necessário em alguns ambientes (como contêineres)
    chrome_options.add_argument("--disable-dev-shm-usage")  # Para rodar sem usar muita memória

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    thread = threading.Thread(target=processar_urls, args=(lista_de_urls, conn, driver))
    thread.start()

    while thread.is_alive():
        time.sleep(1)

    driver.quit()
    conn.close()
    print("✅ Finalizado.")
