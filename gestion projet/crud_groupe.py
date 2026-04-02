from db import get_connection

def get_groupes(Id_Encadrant):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "SELECT g.* FROM groupe g "
        "JOIN projet p ON g.Id_projet = p.Id_projet "
        "WHERE p.Id_Encadrant=%s",
        (Id_Encadrant,)
    )
    groupes = cursor.fetchall()
    db.close()
    return groupes

def add_groupe(nom_group, Id_projet):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO groupe (nom_group, Id_projet) VALUES (%s,%s)",
        (nom_group, Id_projet)
    )
    db.commit()
    db.close()

def update_groupe(Id_group, nom_group):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE groupe SET nom_group=%s WHERE Id_group=%s",
        (nom_group, Id_group)
    )
    db.commit()
    db.close()

def delete_groupe(Id_group):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM groupe WHERE Id_group=%s", (Id_group,))
    db.commit()
    db.close()


