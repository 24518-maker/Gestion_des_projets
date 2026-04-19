from db import get_connection

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

def update_password(email, new_password):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE encadrant SET password=%s WHERE email=%s",
        (new_password, email)
    )

    db.commit()
    db.close()

