from flask import Flask, render_template, request, redirect, url_for
import os
import pymysql

app = Flask(__name__)
app.secret_key = "cle-secrete"

# مجلد حفظ الملفات
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# قاعدة البيانات
db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="gestion_des_projets",
    cursorclass=pymysql.cursors.DictCursor
)

# ---------------- Dashboard ----------------
@app.route("/")
def dashboard():
    cursor = db.cursor()

    total_etapes = 3  # عدد المراحل (يمكن تغييره لاحقًا)

    # جلب كل الملفات
    cursor.execute("SELECT * FROM livrable")
    livrables = cursor.fetchall()

    # حساب التقدم
    completed = len(livrables)
    progress = int((completed / total_etapes) * 100) if total_etapes else 0

    cursor.close()
    return render_template("dashboard.html",
                           livrables=livrables,
                           progress=progress)

# ---------------- Livrables CRUD ----------------
@app.route("/upload/<int:id_etape>", methods=["POST"])
def upload(id_etape):
    file = request.files.get('file')
    if not file or file.filename == "":
        return redirect(url_for("dashboard"))

    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO livrable (nom_fichier, Id_etape) VALUES (%s,%s)",
        (filename, id_etape)
    )
    cursor.execute(
        "INSERT INTO historique (action) VALUES (%s)",
        (f"Upload {filename}",)
    )
    db.commit()
    cursor.close()
    return redirect(url_for("dashboard"))

@app.route("/modifier/<int:id>", methods=["POST"])
def modifier(id):
    file = request.files.get('file')
    if file and file.filename != "":
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cursor = db.cursor()
        cursor.execute("UPDATE livrable SET nom_fichier=%s WHERE Id_livrable=%s",
                       (filename, id))
        cursor.execute(
            "INSERT INTO historique (action) VALUES (%s)",
            (f"Modification {filename}",)
        )
        db.commit()
        cursor.close()
    return redirect(url_for("dashboard"))

@app.route("/delete/<int:id>")
def delete(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM livrable WHERE Id_livrable=%s", (id,))
    cursor.execute(
        "INSERT INTO historique (action) VALUES (%s)",
        ("Suppression fichier",)
    )
    db.commit()
    cursor.close()
    return redirect(url_for("dashboard"))

# ---------------- Historique ----------------
@app.route("/historique")
def historique():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM historique ORDER BY id DESC")
    data = cursor.fetchall()
    cursor.close()
    return render_template("historique.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)