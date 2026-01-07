from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if not file or file.filename == "":
        return "No file uploaded ❌"

    if not file.filename.lower().endswith(".csv"):
        return "Please upload a valid CSV file ❌"

    try:
        df = pd.read_csv(
            file,
            encoding="latin1",
            sep=None,
            engine="python",
            on_bad_lines="skip"
        )
    except Exception as e:
        return f"Error reading CSV ❌<br><br>{e}"

    df_clean = df.dropna(how="all")
    app.df_clean = df_clean

    rows, columns = df_clean.shape
    missing_values = df_clean.isnull().sum().sum()

    column_info = []
    for col in df_clean.columns:
        column_info.append({
            "name": col,
            "dtype": str(df_clean[col].dtype),
            "missing": int(df_clean[col].isnull().sum())
        })

    table = df_clean.head().to_html(index=False)

    return render_template(
        "result.html",
        table=table,
        rows=rows,
        columns=columns,
        missing=missing_values,
        column_info=column_info,
        column_names=list(df_clean.columns)
    )


@app.route("/filter", methods=["POST"])
def filter_columns():
    selected_columns = request.form.getlist("columns")

    if not selected_columns:
        return "No columns selected ❌"

    df = app.df_clean[selected_columns]

    table = df.head().to_html(index=False)

    return render_template(
        "result.html",
        table=table,
        rows=df.shape[0],
        columns=df.shape[1],
        missing=df.isnull().sum().sum(),
        column_info=[
            {
                "name": col,
                "dtype": str(df[col].dtype),
                "missing": int(df[col].isnull().sum())
            }
            for col in df.columns
        ],
        column_names=list(app.df_clean.columns)
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
