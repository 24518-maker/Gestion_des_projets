from db import get_connection

def get_etapes(encadrant_id):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT e.*, p.Nom_projet
        FROM etape e
        JOIN projet p ON e.Id_projet = p.Id_projet
        JOIN groupe g ON p.Id_group= g.Id_group
        WHERE g.Id_Encadrant= %s
    """,(encadrant_id,))

    etapes = cursor.fetchall()
    db.close()
    return etapes

def get_etapes_by_projet(Id_projet):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT * FROM etape
        WHERE Id_projet = %s
    """, (Id_projet,))

    etapes = cursor.fetchall()
    db.close()
    return etapes

def add_etape(Nom_etape, Id_projet):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO etape (Nom_etape, Id_projet)
        VALUES (%s, %s)
    """, (Nom_etape, Id_projet))

    db.commit()
    db.close()

def update_etape(Id_etape, Nom_etape):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE etape
        SET Nom_etape=%s
        WHERE Id_etape=%s
    """, (Nom_etape ,Id_etape))

    db.commit()
    db.close()

def delete_etape(Id_etape):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("DELETE FROM etape WHERE Id_etape=%s", (Id_etape,))

    db.commit()
    db.close()