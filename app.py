from flask import Flask, request, redirect, render_template_string
import boto3

app = Flask(__name__)

TABLE_NAME = "lab5-apache-answer-dynamodb"
REGION = "ap-south-1"

dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>DynamoDB CRUD Application</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #e3f2fd, #ede7f6);
            color: #1f2937;
        }
        .header {
            background: linear-gradient(135deg, #1976d2, #7b1fa2);
            color: white;
            padding: 35px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        .header h1 { margin: 0; font-size: 38px; }
        .header p { margin: 10px 0 0; font-size: 17px; }
        .container {
            max-width: 1100px;
            margin: 35px auto;
            padding: 0 20px;
        }
        .card {
            background: white;
            border-radius: 18px;
            padding: 28px;
            margin-bottom: 30px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.10);
        }
        .card h2 { margin-top: 0; color: #512da8; }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
        }
        input {
            width: 100%;
            padding: 13px;
            border: 2px solid #ddd;
            border-radius: 9px;
            font-size: 15px;
        }
        input:focus {
            outline: none;
            border-color: #7b1fa2;
        }
        .skills { grid-column: span 3; }
        button {
            border: none;
            border-radius: 9px;
            padding: 13px 22px;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
        }
        .create-btn {
            background: linear-gradient(135deg, #00b894, #00cec9);
            color: white;
        }
        .refresh-btn {
            background: #1976d2;
            color: white;
            float: right;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th {
            background: linear-gradient(135deg, #512da8, #7b1fa2);
            color: white;
            padding: 14px;
        }
        td {
            padding: 13px;
            border-bottom: 1px solid #eee;
            text-align: center;
        }
        tr:nth-child(even) { background: #f7f4ff; }
        tr:hover { background: #e8eaf6; }
        .update {
            color: #1976d2;
            font-weight: bold;
            text-decoration: none;
        }
        .delete {
            color: #e53935;
            font-weight: bold;
            text-decoration: none;
        }
        .badge {
            background: #d4edda;
            color: #198754;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 13px;
        }
        .footer {
            text-align: center;
            padding: 25px;
            background: #1f2937;
            color: white;
            margin-top: 40px;
        }
        @media (max-width: 800px) {
            .form-grid { grid-template-columns: 1fr; }
            .skills { grid-column: span 1; }
        }
    </style>
</head>

<body>

<div class="header">
    <h1>☁️ DynamoDB CRUD Application</h1>
    <p>AWS Cloud Computing — Assignment 2</p>
</div>

<div class="container">

<div class="card">
    <h2>➕ Create Student</h2>
    <p>Add a new student record to Amazon DynamoDB.</p>

    <form method="POST" action="/create">
        <div class="form-grid">

            <input type="text" name="studentId"
                   placeholder="Student ID" required>

            <input type="number" name="age"
                   placeholder="Age" required>

            <input type="text" name="city"
                   placeholder="City" required>

            <input type="number" name="pincode"
                   placeholder="Pincode" required>

            <input class="skills" type="text" name="skills"
                   placeholder="Skills: AWS, Python, SQL" required>

            <button class="create-btn" type="submit">
                ➕ Create Student
            </button>

        </div>
    </form>
</div>

<div class="card">

    <h2>👨‍🎓 Students</h2>

    <button class="refresh-btn"
            onclick="location.reload()">
        🔄 Refresh
    </button>

    <p>Student records stored in Amazon DynamoDB.</p>

    <table>
        <tr>
            <th>Student ID</th>
            <th>Age</th>
            <th>Active</th>
            <th>City</th>
            <th>Pincode</th>
            <th>Skills</th>
            <th>Actions</th>
        </tr>

        {% for item in items %}
        <tr>

            <td><b>{{ item.get('studentId', '') }}</b></td>

            <td>{{ item.get('age', '') }}</td>

            <td>
                {% if item.get('isActive') %}
                    <span class="badge">Active</span>
                {% else %}
                    Inactive
                {% endif %}
            </td>

            <td>{{ item.get('address', {}).get('city', '') }}</td>

            <td>{{ item.get('address', {}).get('pincode', '') }}</td>

            <td>{{ item.get('skills', []) | join(', ') }}</td>

            <td>
                <a class="update"
                   href="/edit/{{ item.get('studentId', '') }}">
                   ✏️ Update
                </a>
                |
                <a class="delete"
                   href="/delete/{{ item.get('studentId', '') }}"
                   onclick="return confirm('Delete this student?')">
                   🗑️ Delete
                </a>
            </td>

        </tr>
        {% endfor %}

    </table>
</div>

</div>

<div class="footer">
    AWS Cloud Computing Assignment 2 |
    DynamoDB CRUD Application
</div>

</body>
</html>
"""

@app.route("/")
def index():
    response = table.scan()
    items = response.get("Items", [])
    return render_template_string(HTML, items=items)


@app.route("/create", methods=["POST"])
def create():
    student_id = request.form["studentId"]
    age = int(request.form["age"])
    city = request.form["city"]
    pincode = int(request.form["pincode"])

    skills = [
        s.strip()
        for s in request.form["skills"].split(",")
    ]

    table.put_item(
        Item={
            "studentId": student_id,
            "age": age,
            "isActive": True,
            "skills": skills,
            "address": {
                "city": city,
                "pincode": pincode
            }
        }
    )

    return redirect("/")


@app.route("/edit/<student_id>")
def edit(student_id):
    response = table.get_item(
        Key={"studentId": student_id}
    )

    item = response.get("Item")

    if not item:
        return "Student not found", 404

    return f"""
    <html>
    <body style="font-family:Arial;
                 background:linear-gradient(135deg,#e3f2fd,#ede7f6);
                 padding:50px">

    <div style="background:white;max-width:500px;
                margin:auto;padding:35px;border-radius:18px;
                box-shadow:0 8px 25px rgba(0,0,0,.15)">

    <h1>✏️ Update Student</h1>

    <p><b>Student ID:</b> {student_id}</p>

    <form method="POST" action="/update/{student_id}">

        Age:
        <input type="number" name="age"
               value="{item.get('age', '')}" required><br><br>

        City:
        <input type="text" name="city"
               value="{item.get('address', {}).get('city', '')}"
               required><br><br>

        Pincode:
        <input type="number" name="pincode"
               value="{item.get('address', {}).get('pincode', '')}"
               required><br><br>

        <button type="submit"
                style="background:#1976d2;color:white;
                       border:none;padding:12px 25px;
                       border-radius:8px">
            💾 Update Student
        </button>

    </form>

    <br>
    <a href="/">← Back to Students</a>

    </div>
    </body>
    </html>
    """


@app.route("/update/<student_id>", methods=["POST"])
def update(student_id):
    age = int(request.form["age"])
    city = request.form["city"]
    pincode = int(request.form["pincode"])

    table.update_item(
        Key={"studentId": student_id},
        UpdateExpression="SET age = :age, address = :address",
        ExpressionAttributeValues={
            ":age": age,
            ":address": {
                "city": city,
                "pincode": pincode
            }
        }
    )

    return redirect("/")


@app.route("/delete/<student_id>")
def delete(student_id):
    table.delete_item(
        Key={"studentId": student_id}
    )

    return redirect("/")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
