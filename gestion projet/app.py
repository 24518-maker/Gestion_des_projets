from flask import Flask, request, redirect, render_template, session, url_for
from datetime import date, datetime
from crud_projet import get_projets, add_projet, update_projet, delete_projet
from crud_groupe import get_groupes, add_groupe, update_groupe, delete_groupe
from crud_etape import get_etapes, add_etape, update_etape, delete_etape
from crud_evaluation import get_evaluations, add_evaluation, update_evaluation, delete_evaluation
from crud_livrable import get_livrables
from crud_encadrant import get_encadrant_by_email_password, get_encadrant_by_email, update_password

app = Flask(__name__)
app.secret_key = "secret123"

@app.context_processor
def inject_now():
    return {'now': datetime.now}

# ===== ACCUEIL =====
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
        else:
            return "Email ou mot de passe incorrect"

    return render_template("login.html")

# ===== FORGET PASSWORD =====
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

# ===== RESET PASSWORD =====
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

# ===== DASHBOARD =====
@app.route("/dashboard")
def dashboard():
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    encadrant_id = session["encadrant_id"]
    nom_encadrant = session.get("encadrant_nom")

    projets = get_projets(encadrant_id)

    total_projets = len(projets)
    projets_termines = 0
    projets_en_cours = 0
    total_etudiants = 0

    for projet in projets:
        groupes = get_groupes(projet['Id_projet'])
        projet['groupes'] = groupes

        # Exemple simple d'avancement
        projet['avancement'] = 0


        date_fin = projet['date_fin']
        if isinstance(date_fin, str):
            try:
                date_fin = datetime.strptime(date_fin, "%Y-%m-%d").date()
                projet['date_fin'] = date_fin
            except ValueError:
                date_fin = None

        if date_fin:
            if date_fin <= date.today():
                projets_termines += 1
            else:
                projets_en_cours += 1
        else:
            projets_en_cours += 1

        total_etudiants += sum(len(groupe.get('etudiants', [])) for groupe in groupes)

    return render_template(
        "dashboard.html",
        nom_enseignant=nom_encadrant,
        total_projets=total_projets,
        photo_encadrant=session['photo_encadrant'],
        projets_en_cours=projets_en_cours,
        projets_termines=projets_termines,
        total_etudiants=total_etudiants,
        projets=projets
    )
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

    if request.method == 'POST':
        add_projet(
            request.form['nom_projet'],
            request.form['date_debut'],
            request.form['date_fin'],
            request.form['id_groupe']
        )
        return redirect(url_for('projets_page'))

    return render_template('add_projet.html')

@app.route('/projets/update/<int:Id_projet>', methods=['GET', 'POST'])
def update_projet_page(Id_projet):
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    projets = get_projets(session["encadrant_id"])
    projet = next((p for p in projets if p['Id_projet'] == Id_projet), None)

    if request.method == 'POST':
        update_projet(
            Id_projet,
            request.form['nom_projet'],
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

    groupes = []
    projets = get_projets(session["encadrant_id"])
    for projet in projets:
        groupes += get_groupes(projet['Id_projet'])

    return render_template('groupes.html', groupes=groupes)

@app.route('/groupes/add', methods=['GET', 'POST'])
def add_groupe_page():
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        add_groupe(request.form['nom_groupe'], request.form['id_projet'])
        return redirect(url_for('groupes_page'))

    projets = get_projets(session["encadrant_id"])
    return render_template('add_groupe.html', projets=projets)

@app.route('/groupes/update/<int:Id_group>', methods=['GET', 'POST'])
def update_groupe_page(Id_group):
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    groupes = []
    projets = get_projets(session["encadrant_id"])
    for projet in projets:
        groupes += get_groupes(projet['Id_projet'])

    groupe = next((g for g in groupes if g['Id_group'] == Id_group), None)

    if request.method == 'POST':
        update_groupe(Id_group, request.form['nom_groupe'])
        return redirect(url_for('groupes_page'))

    return render_template('update_groupe.html', groupe=groupe)

@app.route('/groupes/delete/<int:Id_group>')
def delete_groupe_page(Id_group):
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    delete_groupe(Id_group)
    return redirect(url_for('groupes_page'))

# ======= ETAPES =======
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

    if request.method == 'POST':
        add_etape(request.form['nom_etape'], request.form['date_debut'], request.form['date_fin'])
        return redirect(url_for('etapes_page'))

    return render_template('add_etape.html')

@app.route('/etapes/update/<int:Id_etape>', methods=['GET', 'POST'])
def update_etape_page(Id_etape):
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    etapes = get_etapes()
    etape = next((e for e in etapes if e['Id_etape'] == Id_etape), None)

    if request.method == 'POST':
        update_etape(Id_etape, request.form['nom_etape'], request.form['date_debut'], request.form['date_fin'])
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
    evaluations = get_evaluations(session["encadrant_id"])
    return render_template('evaluations.html', evaluations=evaluations)


@app.route('/evaluations/add', methods=['GET', 'POST'])
def add_evaluation_page():
    if "encadrant_id" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        add_evaluation(
            request.form['Note'],
            request.form['Remarque'],
            request.form['Id_etape'],
            request.form['Id_group'],
            session["encadrant_id"]
        )
        return redirect(url_for('evaluations_page'))

    return render_template('add_evaluation.html')


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

    evaluations = get_evaluations(session["encadrant_id"])
    evaluation = next((e for e in evaluations if e["Id_Evaluation"] == Id_Evaluation), None)
    return render_template('update_evaluation.html', evaluation=evaluation)


@app.route('/evaluations/delete/<int:Id_Evaluation>')
def delete_evaluation_page(Id_Evaluation):
    if "encadrant_id" not in session:
        return redirect(url_for("login"))
    delete_evaluation(Id_Evaluation)
    return redirect(url_for('evaluations_page'))


@app.route('/livrables')
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
