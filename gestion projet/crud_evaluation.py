from db import get_connection
def get_all_etapes_groups_with_evaluation(Id_Encadrant):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT 
            et.Id_etape,
            et.Nom_etape,
            g.Id_group,
            g.nom_group,
            e.Id_Evaluation,
            e.Note,
            e.Remarque,
            e.date_evaluation
        FROM groupe g
        JOIN projet p ON p.Id_group = g.Id_group
        JOIN etape et ON et.Id_projet = p.Id_projet
        LEFT JOIN evaluation e 
            ON e.Id_etape = et.Id_etape 
           AND e.Id_group = g.Id_group
        WHERE g.Id_Encadrant = %s
        ORDER BY et.Id_etape DESC
    """, (Id_Encadrant,))

    data = cursor.fetchall()
    db.close()
    return data

def get_evaluation_by_id(Id_Evaluation):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM evaluation WHERE Id_Evaluation=%s",
        (Id_Evaluation,)
    )
    data = cursor.fetchone()
    db.close()
    return data

def add_evaluation(Note, Remarque, Id_etape, Id_group, Id_Encadrant):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO evaluation (Note, Remarque, Id_etape, Id_group, Id_Encadrant)
        VALUES (%s,%s,%s,%s,%s)
        """,
        (Note, Remarque, Id_etape, Id_group, Id_Encadrant)
    )
    db.commit()
    db.close()

def update_evaluation(Id_Evaluation, Note, Remarque):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        """
        UPDATE evaluation
        SET Note=%s, Remarque=%s
        WHERE Id_Evaluation=%s
        """,
        (Note, Remarque, Id_Evaluation)
    )
    db.commit()
    db.close()

def delete_evaluation(Id_Evaluation):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM evaluation WHERE Id_Evaluation=%s",
        (Id_Evaluation,)
    )
    db.commit()
    db.close()