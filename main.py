from flask import Flask, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

stations_df = pd.read_csv("data-small\stations.txt", skiprows=17)
stations = stations_df[['STAID','STANAME                                 ']][:92]
@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())

@app.route("/api/v1/<station>/<date>")
def report(station, date):
    # Reading CSV file to load data
    filename = r"data-small\TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    # Making Good columns to get Good data
    df['TG0'] = df['   TG'].mask(df[' Q_TG']==9, np.nan)
    df["TG"] = df['TG0'] / 10
    # Getting the Temperature
    temperature = df.loc[df['    DATE']== date]['TG'].squeeze()
    
    return {"station": station,
            "date": date,
            "temperature": temperature}

if __name__ == "__main__":
    app.run(debug=True)