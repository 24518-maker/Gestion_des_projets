
from db import get_connection
def get_evaluations(Id_Encadrant):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "SELECT e.*, g.nom_group, et.Nom_etape "
        "FROM evaluation e "
        "JOIN groupe g ON e.Id_group = g.Id_group "
        "JOIN etape et ON e.Id_etape = et.Id_etape "
        "WHERE e.Id_Encadrant = %s",
        (Id_Encadrant,)
    )
    evaluations = cursor.fetchall()
    db.close()
    return evaluations

# ===== ADD =====
def add_evaluation(Note, Remarque, Id_etape, Id_group, Id_Encadrant):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO evaluation (Note, Remarque, Id_etape, Id_group, Id_Encadrant) "
        "VALUES (%s,%s,%s,%s,%s)",
        (Note, Remarque, Id_etape, Id_group, Id_Encadrant)
    )
    db.commit()
    db.close()

# ===== UPDATE =====
def update_evaluation(Id_Evaluation, Note, Remarque):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE evaluation SET Note=%s, Remarque=%s WHERE Id_Evaluation=%s",
        (Note, Remarque, Id_Evaluation)
    )
    db.commit()
    db.close()

# ===== DELETE =====
def delete_evaluation(Id_Evaluation):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM evaluation WHERE Id_Evaluation=%s", (Id_Evaluation,))
    db.commit()
    db.close()