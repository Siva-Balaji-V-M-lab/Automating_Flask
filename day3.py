from flask import Flask, request, render_template_string, redirect, url_for
import csv
import io

app = Flask(__name__)

uploaded_data = None
current_index = 0


@app.route('/')
def index():
    global uploaded_data, current_index

    if uploaded_data is None:
        return "<h2>Waiting for CSV upload... Use curl to upload your file.</h2>"

    if current_index == 0:
        return """
        <h2>No rows displayed yet. Press Enter to start.</h2>
        <form id="nextForm" method="POST" action="/next">
            <button type="submit">Next</button>
        </form>
        <script>
            document.addEventListener("keydown", function(event) {
                if (event.key === "Enter") {
                    event.preventDefault();
                    document.getElementById("nextForm").submit();
                }
            });
        </script>
        """

    # Show rows up to current_index
    rows_to_display = uploaded_data[:current_index]

    table_html = "<h2>CSV Rows Displayed:</h2><table border='1'>"
    for row in rows_to_display:
        table_html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
    table_html += "</table>"

    html = f"""
    {table_html}
    <br>
    <form id="nextForm" method="POST" action="/next">
        <button type="submit">Next</button>
    </form>
    <script>
        document.addEventListener("keydown", function(event) {{
            if (event.key === "Enter") {{
                event.preventDefault();
                document.getElementById("nextForm").submit();
            }}
        }});
    </script>
    """

    # If all rows shown, stop
    if current_index >= len(uploaded_data):
        html = table_html + "<h3>✅ All rows displayed!</h3>"

    return html


@app.route('/next', methods=['POST'])
def next_row():
    global current_index, uploaded_data
    if uploaded_data and current_index < len(uploaded_data):
        current_index += 1
    return redirect(url_for('index'))


@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    global uploaded_data, current_index
    file = request.files['file']
    if not file:
        return "No file uploaded", 400

    # Read CSV
    stream = io.StringIO(file.stream.read().decode("utf-8"))
    reader = csv.reader(stream)
    uploaded_data = list(reader)
    current_index = 0

    return "CSV uploaded successfully! Now open http://127.0.0.1:5000/"


if __name__ == '__main__':
    app.run(debug=True)
