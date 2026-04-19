from db import get_connection

def get_livrables(Id_Encadrant):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT 
            l.Id_fichier,
            l.nom_fichier,
            g.nom_group,
            e.Nom_etape,
            p.Nom_projet
        FROM livrable l
        JOIN etape e ON l.Id_etape = e.Id_etape
        JOIN projet p ON e.Id_projet = p.Id_projet
        JOIN groupe g ON p.Id_group = g.Id_group
        WHERE g.Id_Encadrant = %s
        ORDER BY l.Id_fichier DESC
    """, (Id_Encadrant,))

    livrables = cursor.fetchall()
    db.close()
    return livrables