from db import get_connection
def get_groupes(encadrant_id):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT * FROM groupe
        WHERE Id_Encadrant = %s
    """, (encadrant_id,))

    groupes = cursor.fetchall()

    for g in groupes:
        id_group = g["Id_group"]

        # الطلاب
        cursor.execute("""
            SELECT * FROM etudiant
            WHERE Id_group = %s
        """, (id_group,))
        g["etudiants"] = cursor.fetchall()

        cursor.execute("""
            SELECT * FROM projet
            WHERE Id_group = %s
        """, (id_group,))
        g["projets"] = cursor.fetchall()

    db.close()
    return groupes