from flask import Flask, request, redirect, render_template, session, url_for
from datetime import date, datetime
from crud_projet import get_projets, add_projet, update_projet, delete_projet
from crud_groupes import get_groupes
from crud_etape import get_etapes, add_etape, update_etape, delete_etape
from crud_evaluation import get_all_etapes_groups_with_evaluation,add_evaluation, update_evaluation, delete_evaluation,get_evaluation_by_id
from crud_livrable import get_livrables
from crud_encadrant import get_encadrant_by_email_password, get_encadrant_by_email, update_password
from db import get_connection
from crud_student import get_student_by_email_password

app = Flask(__name__)
app.secret_key = "secret123"

@app.context_processor
def inject_now():
    return {'now': datetime.now}

@app.route("/")
@app.route("/accueil")
def accueil():
    if "encadrant_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("accueil.html")

# ===== LOGIN =====
@app.route("/login", methods=["GET", "POST"])
def login():
    if "encadrant_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        encadrant = get_encadrant_by_email_password(email, password)

        if encadrant:
            session["encadrant_id"] = encadrant["Id_Encadrant"]
            session["encadrant_nom"] = f"{encadrant['Nom']} {encadrant['Prenom']}"
            session['photo_encadrant']=encadrant['photo']
            return redirect(url_for("dashboard"))

        student = get_student_by_email_password(email, password)
        if student:

            session.clear()

            session["role"] = "student"

            session["student_id"] = student["Id"]

            session["group_id"] = student["Id_group"]

            session["student_nom"] = student["Nom"] + " " + student["Prenom"]

            return redirect(url_for("student_dashboard"))
        return "Email ou mot de passe incorrect"

    return render_template("login.html")

@app.route("/forget_password", methods=["GET", "POST"])
def forget_password():
    if request.method == "POST":
        email = request.form["email"]
        encadrant = get_encadrant_by_email(email)

        if encadrant:
            session["reset_email"] = email
            return redirect(url_for("reset_password"))
        else:
            return "Email non trouvé"

    return render_template("forget_password.html")

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if "reset_email" not in session:
        return redirect(url_for("forget_password"))

    if request.method == "POST":
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            return "Les mots de passe ne correspondent pas"

        update_password(session["reset_email"], new_password)
        session.pop("reset_email")

        return redirect(url_for("login"))

    return render_template("reset_password.html")

@app.route("/student/livrables")
def livrables():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT l.nom_fichier, e.Nom_etape, e.Note, e.Remarque
        FROM livrable l
        LEFT JOIN etape e ON l.Id_etape = e.Id_etape
        WHERE l.Id_group = %s
        ORDER BY l.Id_fichier DESC
    """, (session["group_id"],))

    data = cursor.fetchall()
    db.close()

    return render_template("livrables.html", data=data)
@app.route("/notes")
def notes():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT 
            l.nom_fichier,
            e.Note,
            e.Remarque
        FROM livrable l
        LEFT JOIN evaluation e ON e.Id_etape = l.Id_etape
        WHERE l.Id_group = %s
    """, (session["group_id"],))

    data = cursor.fetchall()
    db.close()

    return render_template("notes.html", data=data)
@app.route("/groupe")
def groupe():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT Nom, Prenom
        FROM etudiant
        WHERE Id_group = %s
    """, (session["group_id"],))

    students = cursor.fetchall()
    db.close()

    return render_template("groupe.html", students=students)
@app.route("/encadrant/dashboard")
def dashboard():
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    encadrant_id = session["encadrant_id"]
    nom_encadrant = session.get("encadrant_nom")

    projets = get_projets(encadrant_id)

    total_projets = len(projets)
    projets_termines = 0
    projets_en_cours = 0

    db = get_connection()
    cursor = db.cursor()

    # 👨‍🎓 total étudiants
    cursor.execute("""
        SELECT COUNT(*) as total
        FROM etudiant e
        JOIN groupe g ON e.Id_group = g.Id_group
        WHERE g.Id_Encadrant = %s
    """, (encadrant_id,))
    total_etudiants = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) as total
        FROM etape e
        JOIN projet p ON e.Id_projet = p.Id_projet
       JOIN groupe g on p.Id_group=g.Id_group
        WHERE g.Id_Encadrant = %s
    """, (encadrant_id,))
    total_etapes = cursor.fetchone()["total"]
    cursor.execute("""
        SELECT COUNT(DISTINCT l.Id_etape) as done
        FROM livrable l
        JOIN etape e ON e.Id_etape = l.Id_etape
        JOIN projet p ON e.Id_projet = p.Id_projet
        JOIN groupe g ON p.Id_group=g.Id_group
        WHERE g.Id_Encadrant = %s
    """, (encadrant_id,))
    done_etapes = cursor.fetchone()["done"]

    if total_etapes > 0:
        global_progress = int((done_etapes / total_etapes) * 100)
    else:
        global_progress = 0

    for projet in projets:
        groupes = get_groupes(projet['Id_projet'])
        projet['groupes'] = groupes
        date_fin = projet['date_fin']
        if isinstance(date_fin, str):
            try:
                date_fin = datetime.strptime(date_fin, "%Y-%m-%d").date()
            except ValueError:
                date_fin = None

        is_expired = date_fin and date_fin < date.today()
        projet['progress'] = global_progress

        if is_expired and global_progress == 0:
            status = "late"
        elif global_progress == 100:
            status = "done"
        elif global_progress > 0:
            status = "in_progress"
        else:
            status = "not_started"

        projet['status'] = status
        projet['is_expired'] = is_expired

        if is_expired:
            projets_termines += 1
        else:
            projets_en_cours += 1

    return render_template(
        "dashboard.html",
        nom_encadrant=nom_encadrant,
        total_projets=total_projets,
        photo_encadrant=session.get('photo_encadrant'),
        projets_en_cours=projets_en_cours,
        projets_termines=projets_termines,
        total_etudiants=total_etudiants,
        projets=projets,
        global_progress=global_progress
    )
@app.route("/student")
def student_dashboard():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    db = get_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT *
        FROM livrable
        WHERE Id_group = %s
        ORDER BY Id_fichier DESC
        LIMIT 1
    """, (session["group_id"],))
    last_file = cursor.fetchone()

    cursor.execute("""
        SELECT p.Nom_projet
        FROM groupe g
        LEFT JOIN projet p ON p.Id_group = g.Id_group
        WHERE g.Id_group = %s
    """, (session["group_id"],))
    projets= cursor.fetchall()
    cursor.execute("""
        SELECT Nom_group
        FROM groupe
        WHERE Id_group = %s
    """, (session["group_id"],))
    groupe = cursor.fetchone()
    cursor.execute("""
        SELECT Id_etape, Nom_etape
        FROM etape
    """)
    etapes = cursor.fetchall()

    db.close()

    return render_template(
        "student.html",
        nom_etudiant=session.get("student_nom"),
        last_file=last_file,
        projets=projets,
        groupe_nom=groupe["Nom_group"] if groupe else None,
        etapes=etapes)

@app.route('/projets')
def projets_page():
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    projets = get_projets(session["encadrant_id"])
    return render_template('projets.html', projets=projets)

@app.route('/projets/add', methods=['GET', 'POST'])
def add_projet_page():
    if "encadrant_id" not in session:
        return redirect(url_for("login"))
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM groupe WHERE Id_encadrant=%s", (session["encadrant_id"],))
    groupes = cursor.fetchall()

    if request.method == 'POST':
        add_projet(
            request.form['Nom_projet'],
            request.form['date_debut'],
            request.form['date_fin'],
            request.form['id_group']
        )
        return redirect(url_for('projets_page'))

    return render_template('add_projet.html', groupes=groupes)

@app.route('/projets/update/<int:Id_projet>', methods=['GET', 'POST'])
def update_projet_page(Id_projet):
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    projets = get_projets(session["encadrant_id"])
    projet = next((p for p in projets if p['Id_projet'] == Id_projet), None)

    if request.method == 'POST':
        update_projet(
            Id_projet,
            request.form['Nom_projet'],
            request.form['date_debut'],
            request.form['date_fin']
        )
        return redirect(url_for('projets_page'))

    return render_template('update_projet.html', projet=projet)

@app.route('/projets/delete/<int:Id_projet>')
def delete_projet_page(Id_projet):
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    delete_projet(Id_projet)
    return redirect(url_for('projets_page'))
@app.route('/groupes')
def groupes_page():
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    groupes = get_groupes(session["encadrant_id"])

    return render_template("groupes.html", groupes=groupes)
@app.route('/etapes')
def etapes_page():
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    etapes = get_etapes()
    return render_template('etapes.html', etapes=etapes)

@app.route('/etapes/add', methods=['GET', 'POST'])
def add_etape_page():
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT p.*
        FROM projet p
        JOIN groupe g ON p.Id_group = g.Id_group
        WHERE g.Id_encadrant = %s
    """, (session["encadrant_id"],))

    projets = cursor.fetchall()

    if request.method == 'POST':
        add_etape(
            request.form['Nom_etape'],
            request.form['Id_projet']
        )
        return redirect(url_for('etapes_page'))

    return render_template('add_etape.html', projets=projets)

@app.route('/etapes/update/<int:Id_etape>', methods=['GET', 'POST'])
def update_etape_page(Id_etape):
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    etapes = get_etapes()
    etape = next((e for e in etapes if e['Id_etape'] == Id_etape), None)

    if request.method == 'POST':
        update_etape(
            Id_etape,
            request.form['Nom_etape'],

        )
        return redirect(url_for('etapes_page'))

    return render_template('update_etape.html', etape=etape)


@app.route('/etapes/delete/<int:Id_etape>')
def delete_etape_page(Id_etape):
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    delete_etape(Id_etape)
    return redirect(url_for('etapes_page'))

@app.route('/evaluations')
def evaluations_page():
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    evaluations=get_all_etapes_groups_with_evaluation(session["encadrant_id"])
    return render_template('evaluations.html',  evaluations=evaluations)

@app.route('/evaluations/add', methods=['GET', 'POST'])
def add_evaluation_page():
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    groupes = get_groupes(session["encadrant_id"])
    etapes = get_etapes()

    if request.method == 'POST':
        add_evaluation(
            request.form['Note'],
            request.form['Remarque'],
            request.form['Id_etape'],
            request.form['Id_group'],
            session["encadrant_id"]
        )
        return redirect(url_for('evaluations_page'))

    return render_template(
        'add_evaluation.html',
        groupes=groupes,
        etapes=etapes
    )
@app.route('/evaluations/update/<int:Id_Evaluation>', methods=['GET', 'POST'])
def update_evaluation_page(Id_Evaluation):
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        update_evaluation(
            Id_Evaluation,
            request.form['Note'],
            request.form['Remarque']
        )
        return redirect(url_for('evaluations_page'))

    evaluation = get_evaluation_by_id(Id_Evaluation)

    return render_template(
        'update_evaluation.html',
        evaluation=evaluation
    )

@app.route('/evaluations/delete/<int:Id_Evaluation>')
def delete_evaluation_page(Id_Evaluation):
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    delete_evaluation(Id_Evaluation)
    return redirect(url_for('evaluations_page'))

@app.route('/encadrant/livrables')
def livrables_encadrant():
    Id_Encadrant = session["encadrant_id"]
    livrables = get_livrables(Id_Encadrant)
    return render_template('livrable.html', livrables=livrables)




@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)