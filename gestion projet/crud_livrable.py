from db import get_connection

def get_livrables(Id_Encadrant):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "SELECT l.Id_fichier, l.nom_fichier, g.nom_group, e.Nom_etape "
        "FROM livrable l "
        "JOIN groupe g ON l.Id_group = g.Id_group "
        "JOIN projet p ON p.Id_group = g.Id_group "
        "JOIN etape e ON l.Id_etape = e.Id_etape "
        "WHERE g.Id_Encadrant=%s",
        (Id_Encadrant,)
    )
    livrables = cursor.fetchall()
    db.close()
    return livrables
