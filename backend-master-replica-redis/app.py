from flask import Flask, request, jsonify
import redis
import json

from db import get_master_conn, get_replica_conn
from config import Config

app = Flask(__name__)

# ---------------- REDIS ----------------
cache = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    decode_responses=True
)

CACHE_KEY = "employees_all"

# ---------------- GET ----------------
@app.route("/api/employees", methods=["GET"])
def get_employees():

    # 1. check cache
    cached = cache.get(CACHE_KEY)
    if cached:
        return jsonify({
            "source": "redis",
            "data": json.loads(cached)
        })

    # 2. fallback replica
    conn = get_replica_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()
    conn.close()

    # 3. store cache
    cache.set(CACHE_KEY, json.dumps(data), ex=60)

    return jsonify({
        "source": "replica",
        "data": data
    })

# ---------------- POST ----------------
@app.route("/api/employees", methods=["POST"])
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

    cache.delete(CACHE_KEY)

    return jsonify({"msg": "Inserted in MASTER + cache cleared"})

# ---------------- PUT ----------------
@app.route("/api/employees/<int:id>", methods=["PUT"])
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

    cache.delete(CACHE_KEY)

    return jsonify({"msg": "Updated in MASTER + cache cleared"})

# ---------------- DELETE ----------------
@app.route("/api/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):

    conn = get_master_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    cache.delete(CACHE_KEY)

    return jsonify({"msg": "Deleted in MASTER + cache cleared"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
