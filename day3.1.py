from flask import Flask, render_template_string, request
import os
import csv

app = Flask(__name__)
CSV_PATH = os.path.expanduser("~/Desktop/sample.csv")

# HTML Template with auto-refresh every 3 sec
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CSV Viewer</title>
    <meta http-equiv="refresh" content="3"> <!-- Auto-refresh every 3 sec -->
</head>
<body>
    <h1>CSV Data</h1>
    {% if rows %}
        <table border="1" cellpadding="5">
            <tr>
                {% for col in header %}
                    <th>{{ col }}</th>
                {% endfor %}
            </tr>
            {% for row in rows %}
                <tr>
                    {% for col in row %}
                        <td>{{ col }}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
        </table>
    {% else %}
        <p>Waiting for CSV file upload...</p>
    {% endif %}
</body>
</html>
"""

def read_csv():
    if not os.path.exists(CSV_PATH):
        return [], []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        rows = list(reader)
        if rows:
            return rows[0], rows[1:]
        return [], []
        
@app.route("/")
def index():
    header, rows = read_csv()
    return render_template_string(HTML_TEMPLATE, header=header, rows=rows)

@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    file = request.files["file"]
    file.save(CSV_PATH)
    return "CSV uploaded successfully!"

if __name__ == "__main__":
    app.run(debug=True)
