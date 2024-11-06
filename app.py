from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64

app = Flask(__name__)

def generate_plot(df):
    fig = px.line(df, x="test_date", y="score", color="section", title="Score Over Time")
    img = BytesIO()
    fig.write_image(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

@app.route('/')
def home():
    return render_template("dashboard.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if not file:
        return "No file selected"
    df = pd.read_csv(file)
    plot_url = generate_plot(df)
    return render_template("dashboard.html", plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
