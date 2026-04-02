from db import get_connection

def get_projets(Id_Encadrant):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM projet WHERE Id_Encadrant=%s",
        (Id_Encadrant,)
    )
    projets = cursor.fetchall()
    db.close()
    return projets

def add_projet(Nom_projet, date_debut, date_fin, Id_Encadrant):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO projet (Nom_projet, date_debut, date_fin, Id_Encadrant) VALUES (%s,%s,%s,%s)",
        (Nom_projet, date_debut, date_fin, Id_Encadrant)
    )
    db.commit()
    db.close()

def update_projet(Id_projet, Nom_projet, date_debut, date_fin):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE projet SET Nom_projet=%s, date_debut=%s, date_fin=%s WHERE Id_projet=%s",
        (Nom_projet, date_debut, date_fin, Id_projet)
    )
    db.commit()
    db.close()

def delete_projet(Id_projet):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM projet WHERE Id_projet=%s", (Id_projet,))
    db.commit()
    db.close()