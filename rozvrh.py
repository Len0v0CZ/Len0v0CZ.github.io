import os
import datetime
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

rozvrh = []
ucebny = []
ucitele = []


def nacti_rozvrh(nazev_rozvrhu):
    """
    TXTak
    ucitele[]
    ucebny[]
    rozvrh[]
    """
    rozvrh = []
    ucebny = []
    ucitele = []

    file_path = os.path.join(os.path.dirname(__file__), "rozvrhy", nazev_rozvrhu)
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

            # načítání hodin
            for line in lines[:5]: 
                den = line.split()
                rozvrh.append(den)

            # načítání učeben
            for line in lines[5:10]:
                den = line.split()
                ucebny.append(den)
                
            # načítání učitelů
            for line in lines[10:]:
                den = line.split()
                ucitele.append(den)
    except FileNotFoundError:
        print(f"Soubor {file_path} nebyl nalezen. Používám prázdný rozvrh.")
    
    return rozvrh, ucebny, ucitele

def vytvor_rozvrh_objekt(rozvrh, ucebny, ucitele):
    """
    Crhovy oblíbené slovníky
    """
    casy = [
        "8:00-8:45", "8:55-9:40", "10:00-10:45", "10:55-11:40",
        "11:50-12:35", "12:45-13:30", "13:40-14:25", "14:35-15:20"
    ]
    
    # Slovník pro dny v týdnu (1=pondělí, 5=pátek)
    rozvrh_obj = {}
    
    for den_index in range(len(rozvrh)):
        den_cislo = den_index + 1  # 0->1 (pondělí), 1->2 (úterý), atd.
        lessons = []
        
        for hodina_index in range(len(rozvrh[den_index])):
            subject = rozvrh[den_index][hodina_index]
            room = ucebny[den_index][hodina_index] if den_index < len(ucebny) and hodina_index < len(ucebny[den_index]) else "-"
            teacher = ucitele[den_index][hodina_index] if den_index < len(ucitele) and hodina_index < len(ucitele[den_index]) else "-"
            
            # Přeskočit prázdné hodiny
            if subject != "-" and subject.strip():
                lessons.append({
                    "number": hodina_index + 1,
                    "subject": subject,
                    "room": room,
                    "teacher": teacher,
                    "time": casy[hodina_index] if hodina_index < len(casy) else "N/A"
                })
        
        rozvrh_obj[den_cislo] = lessons
    
    return rozvrh_obj


# Načtení rozvrhu při startu
rozvrh, ucebny, ucitele = nacti_rozvrh("rozvrh.txt")


@app.route('/')
def index():
    """HTML"""
    try:
        html_path = os.path.join(os.path.dirname(__file__), 'index.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return """
        <h1>Chyba. ztratils soubor retarde</h1>
        """.format(os.path.dirname(__file__))


@app.route('/api/rozvrh')
def get_rozvrh():
    rozvrh_obj = vytvor_rozvrh_objekt(rozvrh, ucebny, ucitele)
    return jsonify(rozvrh_obj)


if __name__ == '__main__':
    print("\n" + "!"*50)
    print("Rozvrh http://localhost:5000")
    print("!"*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)