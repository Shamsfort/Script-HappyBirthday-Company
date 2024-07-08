import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from colorama import Fore, Style, init

# Inizializza colorama
init(autoreset=True)

def send_email(to_email, subject, body):
    smtp_server = 'X'
    smtp_port = 2525
    from_email = 'example@noreply.com'  # Email fittizia per il test
    from_password = 'X'  # Password fornita da Mailtrap
    username = 'X'  # Username fornito da Mailtrap

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.login(username, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print(f"Email inviata a {to_email}")
    except Exception as e:
        print(f"Errore nell'invio dell'email a {to_email}: {str(e)}")

def get_birthday_message(name, message_type, language):
    messages = {
        "it": {
            "default": f"""\
Ciao {name},

Tantissimi auguri di buon compleanno!

In questo giorno speciale, desideriamo augurarti tutto il meglio. Speriamo che tu possa trascorrere una giornata meravigliosa, piena di gioia, risate e affetto.

Grazie per essere una parte preziosa della nostra comunità. Ci auguriamo di poter festeggiare molti altri compleanni insieme.

Con affetto,
Il Team
""",
            "special": f"""\
Ciao {name},

Tantissimi auguri di buon compleanno!

In questo giorno speciale, vogliamo ringraziarti per tutto il tuo contributo e la tua dedizione. Speriamo che tu possa trascorrere una giornata meravigliosa, piena di gioia, risate e affetto.

Con i migliori auguri,
Il Team Speciale
"""
        },
        "es": {
            "default": f"""\
Hola {name},

¡Feliz cumpleaños!

En este día especial, deseamos todo lo mejor para ti. Esperamos que pases un día maravilloso, lleno de alegría, risas y cariño.

Gracias por ser una parte valiosa de nuestra comunidad. Esperamos poder celebrar muchos más cumpleaños contigo.

Con cariño,
El Equipo
""",
            "special": f"""\
Hola {name},

¡Feliz cumpleaños!

En este día especial, queremos agradecerte por todo tu aporte y dedicación. Esperamos que pases un día maravilloso, lleno de alegría, risas y cariño.

Con nuestros mejores deseos,
El Equipo Especial
"""
        }
    }

    return messages.get(language, {}).get(message_type, f"Hello {name}, happy birthday!")

def check_birthdays():
    print("Controllo compleanni...")
    df = pd.read_csv('users.csv')  # Legge il file CSV
    today = datetime.datetime.now().strftime("%m-%d")  # Ottiene la data odierna nel formato MM-DD
    print(f"Oggi è {today}")

    birthday_people = []  # Lista per memorizzare i nomi dei festeggiati

    for index, row in df.iterrows():
        # Rimuove eventuali spazi indesiderati nei campi
        row = row.apply(str.strip)
        # Estrae la data di nascita nel formato MM-DD
        birthday = datetime.datetime.strptime(row['birthdate'], "%Y-%m-%d").strftime("%m-%d")
        if today == birthday:  # Controlla se oggi è il compleanno
            birthday_people.append(row['name'])  # Aggiunge il nome del festeggiato alla lista
            
            # Determina il messaggio da inviare
            body = get_birthday_message(row['name'], row['message_type'], row['language'])
            subject = "Buon Compleanno!" if row['language'] == 'it' else "¡Feliz Cumpleaños!"
            print(f"Inviando email a {row['email']}")
            send_email(row['email'], subject, body)
        else:
            print(f"Oggi non è il compleanno di {row['name']}")

    if birthday_people:
        print(f"Oggi è anche il compleanno di: {', '.join(birthday_people)}")
    else:
        print(Fore.GREEN + "Buona giornata e buon lavoro! :)")

# Test manuale per eseguire la funzione una volta
if __name__ == "__main__":
    print("Eseguendo controllo manuale dei compleanni...")
    check_birthdays()
    print("Esecuzione completata.")