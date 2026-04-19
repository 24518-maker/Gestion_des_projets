from flask import Flask, request, redirect, render_template, session, url_for,send_from_directory
from datetime import date, datetime
from crud_projet import get_projets, add_projet, update_projet, delete_projet
from crud_groupes import get_groupes
from crud_etape import get_etapes, add_etape, update_etape, delete_etape
from crud_evaluation import get_all_etapes_groups_with_evaluation,add_evaluation, update_evaluation, delete_evaluation,get_evaluation_by_id,get_etape_by_id,get_groupe_by_id
from crud_livrable import get_livrables
from crud_encadrant import get_encadrant_by_email_password,get_encadrant_by_email
from db import get_student_by_email,update_student_password, update_encadrant_password
from db import get_connection
from crud_student import get_student_by_email_password
import os
from werkzeug.utils import secure_filename
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

app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

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
        student = get_student_by_email(email)

        if encadrant:
            session["reset_email"] = email
            session["user_type"] = "encadrant"
            return redirect(url_for("reset_password"))

        elif student:
            session["reset_email"] = email
            session["user_type"] = "student"
            return redirect(url_for("reset_password"))

        else:
            return render_template("forget_password.html", error="Email non trouvé")

    return render_template("forget_password.html")


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if "reset_email" not in session:
        return redirect(url_for("forget_password"))

    if request.method == "POST":
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            return render_template(
                "reset_password.html",
                error="Les mots de passe ne correspondent pas"
            )

        email = session["reset_email"]
        user_type = session["user_type"]

        if user_type == "encadrant":
            update_encadrant_password(email, new_password)

        elif user_type == "student":
            update_student_password(email, new_password)

        session.pop("reset_email", None)
        session.pop("user_type", None)

        return redirect(url_for("login"))

    return render_template("reset_password.html")

@app.route("/student/livrables")
def livrables():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT 
            l.Id_fichier,
            l.nom_fichier,
            l.date_upload,
            e.Nom_etape,
            ev.Note,
            ev.Remarque
        FROM livrable l
        LEFT JOIN etape e ON l.Id_etape = e.Id_etape
        LEFT JOIN evaluation ev 
            ON ev.Id_etape = l.Id_etape 
            AND ev.Id_group = l.Id_group
        WHERE l.Id_group = %s
        ORDER BY l.Id_fichier DESC
    """, (session["group_id"],))

    data = cursor.fetchall()
    db.close()

    return render_template("livrables.html", data=data)
@app.route("/livrables")
def livrables_redirect():
    return redirect(url_for("livrables"))

@app.route("/notes")
def notes():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT 
            p.Nom_projet,
            e.Nom_etape,
            ev.Note,
            ev.Remarque,
            ev.date_evaluation,
            l.nom_fichier
        FROM etape e
        JOIN projet p ON e.Id_projet = p.Id_projet

        LEFT JOIN evaluation ev 
            ON ev.Id_etape = e.Id_etape 
            AND ev.Id_group = %s

        LEFT JOIN livrable l 
            ON l.Id_etape = e.Id_etape 
            AND l.Id_group = %s

        WHERE p.Id_group = %s

        ORDER BY ev.Id_evaluation DESC
    """, (
        session["group_id"],
        session["group_id"],
        session["group_id"]
    ))

    data = cursor.fetchall()
    db.close()

    return render_template("notes.html", data=data)

@app.route("/groupe")
def groupe():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    db = get_connection()
    cursor = db.cursor()

    # 👥 students
    cursor.execute("""
        SELECT Nom, Prenom, email, Matricule
        FROM etudiant
        WHERE Id_group = %s
    """, (session["group_id"],))
    students = cursor.fetchall()

    # 📁 project + encadrant
    cursor.execute("""
        SELECT p.Nom_projet,
               CONCAT(e.Nom, ' ', e.Prenom) AS encadrant_nom
        FROM projet p
        JOIN groupe g ON p.Id_group = g.Id_group
        JOIN encadrant e ON g.Id_Encadrant = e.Id_Encadrant
        WHERE g.Id_group = %s
        LIMIT 1
    """, (session["group_id"],))

    info = cursor.fetchone()

    db.close()

    return render_template(
        "groupe.html",
        students=students,
        projet_nom=info["Nom_projet"] if info else "Aucun",
        encadrant_nom=info["encadrant_nom"] if info else "Aucun"
    )
@app.route("/delete_all_student_data", methods=["POST"])
def delete_all_student_data():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    etape_id = request.form["etape_id"]

    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM livrable
        WHERE Id_etape=%s AND Id_group=%s
    """, (etape_id, session["group_id"]))

    cursor.execute("""
        DELETE FROM evaluation
        WHERE Id_etape=%s AND Id_group=%s
    """, (etape_id, session["group_id"]))

    db.commit()
    db.close()

    return redirect(url_for("student_dashboard"))
@app.route("/encadrant/dashboard")
def dashboard():
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    from datetime import date, datetime

    encadrant_id = session["encadrant_id"]
    nom_encadrant = session.get("encadrant_nom")

    projets = get_projets(encadrant_id)

    total_projets = len(projets)
    projets_termines = 0
    projets_en_cours = 0
    projets_en_retard = 0
    projets_non_commences = 0

    db = get_connection()
    cursor = db.cursor()

    # ===== TOTAL ETUDIANTS =====
    cursor.execute("""
        SELECT COUNT(*) as total
        FROM etudiant e
        JOIN groupe g ON e.Id_group = g.Id_group
        WHERE g.Id_Encadrant = %s
    """, (encadrant_id,))
    total_etudiants = cursor.fetchone()["total"]

    today = date.today()

    # ===== LOOP PROJETS =====
    for projet in projets:

        groupes = get_groupes(projet['Id_projet'])
        projet['groupes'] = groupes

        # ---- FIX DATES ----
        date_debut = projet['date_debut']
        date_fin = projet['date_fin']

        if isinstance(date_debut, str):
            date_debut = datetime.strptime(date_debut, "%Y-%m-%d").date()

        if isinstance(date_fin, str):
            date_fin = datetime.strptime(date_fin, "%Y-%m-%d").date()

        projet['date_debut'] = date_debut
        projet['date_fin'] = date_fin

        # ===== TOTAL ETAPES =====
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM etape
            WHERE Id_projet = %s
        """, (projet['Id_projet'],))
        total_etapes = cursor.fetchone()["total"]

        # ===== DONE ETAPES (FIXED LOGIC) =====
        cursor.execute("""
            SELECT COUNT(DISTINCT et.Id_etape) as done
            FROM evaluation e
            JOIN etape et ON e.Id_etape = et.Id_etape
            WHERE et.Id_projet = %s
        """, (projet['Id_projet'],))

        done_etapes = cursor.fetchone()["done"]

        # ===== STATUS =====
        if total_etapes > 0 and done_etapes == total_etapes:
            status = "done"
            projets_termines += 1

        elif today < date_debut:
            status = "not_started"
            projets_non_commences += 1

        elif today > date_fin:
            status = "late"
            projets_en_retard += 1

        else:
            status = "in_progress"
            projets_en_cours += 1

        # ===== PROJECT PROGRESS =====
        projet['progress'] = int((done_etapes / total_etapes) * 100) if total_etapes > 0 else 0
        projet['status'] = status

    cursor.execute("""
        SELECT COUNT(*) as total
        FROM etape et
        JOIN projet p ON et.Id_projet = p.Id_projet
        JOIN groupe g ON p.Id_group = g.Id_group
        WHERE g.Id_Encadrant = %s
    """, (encadrant_id,))
    total_etapes_global = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(DISTINCT et.Id_etape) as done
        FROM evaluation e
        JOIN etape et ON e.Id_etape = et.Id_etape
        JOIN projet p ON et.Id_projet = p.Id_projet
        JOIN groupe g ON p.Id_group = g.Id_group
        WHERE g.Id_Encadrant = %s
    """, (encadrant_id,))
    done_etapes_global = cursor.fetchone()["done"]

    global_progress = int((done_etapes_global / total_etapes_global) * 100) if total_etapes_global > 0 else 0

    db.close()

    return render_template(
        "dashboard.html",
        nom_encadrant=nom_encadrant,
        photo_encadrant=session.get('photo_encadrant'),

        total_projets=total_projets,
        projets_en_cours=projets_en_cours,
        projets_termines=projets_termines,
        projets_en_retard=projets_en_retard,
        projets_non_commences=projets_non_commences,

        total_etudiants=total_etudiants,
        projets=projets,
        global_progress=global_progress
    )
@app.route("/student")
def student_dashboard():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    from datetime import date

    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT *
        FROM etudiant
        WHERE Id = %s
    """, (session["student_id"],))
    student = cursor.fetchone()

    # ===== GROUPE =====
    cursor.execute("""
        SELECT Nom_group
        FROM groupe
        WHERE Id_group = %s
    """, (session["group_id"],))
    groupe = cursor.fetchone()

    # ===== PROJETS =====
    cursor.execute("""
        SELECT *
        FROM projet
        WHERE Id_group = %s
    """, (session["group_id"],))
    projets = cursor.fetchall()

    today = date.today()

    total_etapes_global = 0
    done_etapes_global = 0

    # ===== LOOP PROJETS =====
    for p in projets:

        # ---- dates fix ----
        if isinstance(p["date_debut"], str):
            p["date_debut"] = date.fromisoformat(p["date_debut"])

        if isinstance(p["date_fin"], str):
            p["date_fin"] = date.fromisoformat(p["date_fin"])

        # ===== TOTAL ETAPES =====
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM etape
            WHERE Id_projet = %s
        """, (p["Id_projet"],))
        total = cursor.fetchone()["total"]

        # ===== DONE ETAPES =====
        cursor.execute("""
            SELECT COUNT(DISTINCT l.Id_fichier) as done
            FROM livrable l
            JOIN etape e ON e.Id_etape = l.Id_etape
            WHERE e.Id_projet = %s
            AND l.Id_group = %s
        """, (p["Id_projet"], session["group_id"]))

        done = cursor.fetchone()["done"]

        # ===== PROGRESS =====
        p["progress"] = int((done / total) * 100) if total > 0 else 0

        total_etapes_global += total
        done_etapes_global += done
        if total > 0 and done == total:
            p["status"] = "done"

        elif today < p["date_debut"]:
            p["status"] = "not_started"

        elif today > p["date_fin"]:
            p["status"] = "late"

        else:
            p["status"] = "in_progress"
    global_progress = int((done_etapes_global / total_etapes_global) * 100) if total_etapes_global > 0 else 0

    cursor.execute("""
        SELECT 
            e.Id_etape,
            e.Nom_etape,
            e.Id_projet,
            p.Nom_projet,

            (
                SELECT l.nom_fichier
                FROM livrable l
                WHERE l.Id_etape = e.Id_etape
                AND l.Id_group = %s
                ORDER BY l.Id_fichier DESC
                LIMIT 1
            ) AS nom_fichier,

            (
                SELECT ev.Note
                FROM evaluation ev
                WHERE ev.Id_etape = e.Id_etape
                AND ev.Id_group = %s
                ORDER BY ev.Id_evaluation DESC
                LIMIT 1
            ) AS Note,

            (
                SELECT ev.Remarque
                FROM evaluation ev
                WHERE ev.Id_etape = e.Id_etape
                AND ev.Id_group = %s
                ORDER BY ev.Id_evaluation DESC
                LIMIT 1
            ) AS Remarque

        FROM etape e
        JOIN projet p ON e.Id_projet = p.Id_projet
        WHERE p.Id_group = %s
    """, (
        session["group_id"],
        session["group_id"],
        session["group_id"],
        session["group_id"]
    ))

    etapes = cursor.fetchall()

    db.close()

    return (render_template(
        "student.html",
        nom_etudiant=student["Nom"] + " " + student["Prenom"],
        matricule=student["Matricule"],
        groupe_nom=groupe["Nom_group"] if groupe else "—",

        projets=projets,
        etapes=etapes,

        global_progress=global_progress
    ))

@app.route("/delete_project_full/<int:id>")
def delete_project_full(id):
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    db = get_connection()
    cursor = db.cursor()

    # 1. delete evaluations
    cursor.execute("""
        DELETE ev FROM evaluation ev
        JOIN etape e ON ev.Id_etape = e.Id_etape
        WHERE e.Id_projet = %s
    """, (id,))

    # 2. delete livrables
    cursor.execute("""
        DELETE l FROM livrable l
        JOIN etape e ON l.Id_etape = e.Id_etape
        WHERE e.Id_projet = %s
    """, (id,))

    # 3. delete etapes
    cursor.execute("""
        DELETE FROM etape
        WHERE Id_projet = %s
    """, (id,))

    # 4. delete project
    cursor.execute("""
        DELETE FROM projet
        WHERE Id_projet = %s
    """, (id,))

    db.commit()
    db.close()

    return redirect(url_for("projets_page"))

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

    etapes = get_etapes(session["encadrant_id"])
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

@app.route("/upload", methods=["POST"])
def upload():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    etape_id = request.form["etape"]
    file = request.files["file"]

    if file.filename == "":
        return redirect(url_for("student_dashboard"))

    db = get_connection()
    cursor = db.cursor()

    filename = secure_filename(file.filename)

    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    cursor.execute("""
        SELECT Id_fichier
        FROM livrable
        WHERE Id_etape=%s AND Id_group=%s
    """, (etape_id, session["group_id"]))

    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE livrable
            SET nom_fichier=%s,date_upload=N0W()
            WHERE Id_fichier=%s
        """, (filename, existing["Id_fichier"]))
    else:
        cursor.execute("""
            INSERT INTO livrable (nom_fichier, Id_group, Id_etape)
            VALUES (%s, %s, %s)
        """, (filename, session["group_id"], etape_id))

    db.commit()
    db.close()

    return redirect(url_for("student_dashboard"))

@app.route('/etapes/update/<int:Id_etape>', methods=['GET', 'POST'])
def update_etape_page(Id_etape):
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    etapes = get_etapes(session["encadrant_id"])
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

    etape_id = request.args.get("etape_id")
    group_id = request.args.get("group_id")

    if request.method == 'POST':
        add_evaluation(
            request.form['Note'],
            request.form['Remarque'],
            etape_id,
            group_id,
            session["encadrant_id"]
        )
        return redirect(url_for('evaluations_page'))

    etape = get_etape_by_id(etape_id)
    groupe = get_groupe_by_id(group_id)

    return render_template(
        'add_evaluation.html',
        etape=etape,
        groupe=groupe
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


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)