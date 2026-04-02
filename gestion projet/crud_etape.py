from db import get_connection
def get_etapes():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM etape")
    etapes = cursor.fetchall()
    db.close()
    return etapes

def add_etape(Nom_etape):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO etape (Nom_etape) VALUES (%s)",
        (Nom_etape,)
    )
    db.commit()
    db.close()

def update_etape(Id_etape, Nom_etape):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE etape SET Nom_etape=%s WHERE Id_etape=%s",
        (Nom_etape, Id_etape)
    )
    db.commit()
    db.close()

def delete_etape(Id_etape):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM etape WHERE Id_etape=%s", (Id_etape,))
    db.commit()
    db.close()
