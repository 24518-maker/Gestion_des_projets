from db import get_connection

# LOGIN
def get_encadrant_by_email_password(email, password):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM encadrant WHERE email=%s AND password=%s",
        (email, password)
    )

    encadrant = cursor.fetchone()
    db.close()
    return encadrant

def get_encadrant_by_email(email):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM encadrant WHERE email=%s", (email,))
    result = cursor.fetchone()

    db.close()
    return result


# UPDATE PASSWORD
def update_password(email, new_password):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE encadrant SET password=%s WHERE email=%s",
        (new_password, email)
    )

    db.commit()
    db.close()

# def get_etudiants_by_encadrant(id_encadrant):
#     db = get_connection()
#     cursor = db.cursor()
#
#     cursor.execute("""
#         SELECT etudiant.*
#         FROM etudiant
#         JOIN groupe ON etudiant.id_groupe = groupe.id_groupe
#         JOIN projet ON groupe.id_projet = projet.id_projet
#         WHERE projet.id_encadrant = %s
#     """, (id_encadrant,))
#
#     result = cursor.fetchall()
#     db.close()
#     return result


