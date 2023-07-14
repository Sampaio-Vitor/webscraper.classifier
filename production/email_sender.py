import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

def send_email(subject, message, sender_email, sender_password, receiver_email):
    # Configurar o servidor SMTP do Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Criar uma conexão segura com o servidor SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Criar a mensagem do e-mail
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Adicionar o corpo do e-mail
    body = MIMEText(message, 'html')
    msg.attach(body)

    # Enviar o e-mail
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

# Dados de autenticação do Gmail
sender_email = 'XXXXXXX'
sender_password = 'senha'

# Dados para construir o e-mail
receiver_email = 'XXXXXXX'  # O mesmo endereço usado como remetente
subject = 'Vagas encontradas na madrugada'

# Ler o arquivo "data_predicted.csv"
data_predicted = pd.read_csv('data_predicted.csv')

# Ordenar as vagas pela probabilidade em ordem decrescente
data_predicted_sorted = data_predicted.sort_values(by='0', ascending=False)

# Selecionar as 5 vagas com maior probabilidade
top_vagas = data_predicted_sorted.head(5)

# Construir a mensagem do e-mail com as vagas
message = '''<html><body>
<p>Bom dia, Usuario! ☀️</p>

<p>As vagas mais relevantes encontradas nesta madrugada foram:</p>

<ol>
'''
added_titles = set()  # Conjunto para armazenar títulos já adicionados

for i, row in top_vagas.iterrows():
    if row['TITULO'] not in added_titles:
        vaga = f"<li><a href=\"{row['LINK']}\">{row['TITULO']}</a> - {row['EMPRESA']} - {row['LOCAL']} (esta vaga possui {row['0']*100:.1f}% de compatibilidade)</li>"
        message += vaga + '\n'
        added_titles.add(row['TITULO'])

message += '</ol>'

message += '<p>Também foram encontradas as vagas a seguir:</p>'

message += '<ul>'
for i, row in data_predicted_sorted[5:].iterrows():
    if row['TITULO'] not in added_titles:
        vaga = f"<li><a href=\"{row['LINK']}\">{row['TITULO']}</a> - {row['EMPRESA']} - {row['LOCAL']} (esta vaga possui {row['0']*100:.1f}% de compatibilidade)</li>"
        message += vaga + '\n'
        added_titles.add(row['TITULO'])
message += '</ul>'

message += '''

<p>Tenha um bom dia!</p>
</body></html>'''

# Enviar o e-mail
send_email(subject, message, sender_email, sender_password, receiver_email)