from flask import Flask, request, jsonify
from db import get_master_conn, get_replica_conn

app = Flask(__name__)

# ---------------- GET (REPLICA) ----------------
@app.route("/employees", methods=["GET"])
def get_employees():

    conn = get_replica_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()
    conn.close()

    return jsonify({"source": "replica", "data": data})

# ---------------- POST (MASTER) ----------------
@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.json

    conn = get_master_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employees (name, role) VALUES (%s, %s)",
        (data["name"], data["role"])
    )
    conn.commit()
    conn.close()

    return jsonify({"msg": "Inserted into MASTER"})

# ---------------- PUT (MASTER) ----------------
@app.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):
    data = request.json

    conn = get_master_conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE employees SET name=%s, role=%s WHERE id=%s",
        (data["name"], data["role"], id)
    )
    conn.commit()
    conn.close()

    return jsonify({"msg": "Updated in MASTER"})

# ---------------- DELETE (MASTER) ----------------
@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):

    conn = get_master_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return jsonify({"msg": "Deleted in MASTER"})


if __name__ == "__main__":
    app.run(debug=True)