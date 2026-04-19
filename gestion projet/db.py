import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="gestion_projet",
        cursorclass=pymysql.cursors.DictCursor
    )


def get_student_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM etudiant WHERE email = %s", (email,))
    student = cursor.fetchone()

    conn.close()
    return student


def update_student_password(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE etudiant SET password = %s WHERE email = %s",
        (password, email)
    )

    conn.commit()
    conn.close()


def update_encadrant_password(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE encadrant SET password = %s WHERE email = %s",
        (password, email)
    )

    conn.commit()
    conn.close()