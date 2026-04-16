from db import get_connection

def get_student_by_email_password(email, password):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM etudiant WHERE email=%s AND password=%s",
        (email, password)
    )

    student = cursor.fetchone()
    db.close()
    return student
