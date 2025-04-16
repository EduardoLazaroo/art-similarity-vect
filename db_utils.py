import mysql.connector
from config import DB_CONFIG

def get_info_by_filename(nome_arquivo):
    conn = mysql.connector.connect(**DB_CONFIG)

    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT u.url, ie.chave, ie.valor
        FROM informacoes_extraidas ie
        JOIN urls u ON ie.registro_id = u.id
        WHERE u.nome_imagem = %s;
    """
    cursor.execute(query, (nome_arquivo,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        return None

    url = rows[0]['url']
    info = [{'chave': row['chave'], 'valor': row['valor']} for row in rows]

    return {
        'url': url,
        'info': info
    }
