from db import get_connection

def get_all_etapes_groups_with_evaluation(Id_Encadrant):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT 
            et.Id_etape,
            et.Nom_etape,

            g.Id_group,
            g.Nom_group,

            p.Id_projet,
            p.Nom_projet,

            e.Id_Evaluation,
            e.Note,
            e.Remarque,
            e.date_evaluation

        FROM groupe g
        JOIN projet p 
            ON p.Id_group = g.Id_group

        JOIN etape et 
            ON et.Id_projet = p.Id_projet

        LEFT JOIN evaluation e 
            ON e.Id_etape = et.Id_etape 
           AND e.Id_group = g.Id_group
           AND e.Id_Encadrant = g.Id_Encadrant

        WHERE g.Id_Encadrant = %s

        ORDER BY et.Id_etape DESC
    """, (Id_Encadrant,))

    data = cursor.fetchall()
    db.close()
    return data


# =====================================================
# GET ONE EVALUATION
# =====================================================
def get_evaluation_by_id(Id_Evaluation):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT * 
        FROM evaluation 
        WHERE Id_Evaluation = %s
    """, (Id_Evaluation,))

    data = cursor.fetchone()
    db.close()
    return data


# =====================================================
# GET ETAPE BY ID (مهم لصفحة ADD)
# =====================================================
def get_etape_by_id(etape_id):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT * 
        FROM etape 
        WHERE Id_etape = %s
    """, (etape_id,))

    data = cursor.fetchone()
    db.close()
    return data


# =====================================================
# GET GROUPE BY ID (مهم لصفحة ADD)
# =====================================================
def get_groupe_by_id(group_id):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT * 
        FROM groupe 
        WHERE Id_group = %s
    """, (group_id,))

    data = cursor.fetchone()
    db.close()
    return data


# =====================================================
# ADD EVALUATION
# =====================================================
def add_evaluation(Note, Remarque, Id_etape, Id_group, Id_Encadrant):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO evaluation 
        (Note, Remarque, Id_etape, Id_group, Id_Encadrant)
        VALUES (%s, %s, %s, %s, %s)
    """, (Note, Remarque, Id_etape, Id_group, Id_Encadrant))

    db.commit()
    db.close()


# =====================================================
# UPDATE EVALUATION
# =====================================================
def update_evaluation(Id_Evaluation, Note, Remarque):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE evaluation
        SET Note = %s,
            Remarque = %s
        WHERE Id_Evaluation = %s
    """, (Note, Remarque, Id_Evaluation))

    db.commit()
    db.close()

def delete_evaluation(Id_Evaluation):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM evaluation 
        WHERE Id_Evaluation = %s
    """, (Id_Evaluation,))

    db.commit()
    db.close()