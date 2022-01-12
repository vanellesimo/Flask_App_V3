from flask import Blueprint, render_template, request, flash, jsonify,redirect
import json
import time
import numpy as np
from hdbcli import dbapi
from nelson_siegel_svensson.calibrate import calibrate_ns_ols
from nelson_siegel_svensson import NelsonSiegelCurve
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline

"""
if name == "main":
    date = input("Enter the desire date: ")
    currency = input("Enter the desire currency: ")
    swap_or_gov = input("Choose between swap or govie: ")
    

"""

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def BuildCurve():
    return render_template("calculation.html")
       
    if request.method == "POST":

       req = request.form 
       
       fin_instrument = req["RFR_value"]
       currency = req["currency"]
       date = "20/10/2021" #req["obs_date"]

       print(fin_instrument, currency, date)

       return redirect("/about")

    file = "swap_eur2" # change here

    conn = dbapi.connect(
        address='localhost',
        port=30015,
        user="S0023847307",
        password="AnnickVan8GiovanitaVan50"
    )

    print('Connected:', conn.isconnected())

    cur = conn.cursor()
    try:
        change_schema = 'SET SCHEMA GROUPE_3_MACHINELEARNING'
        cur.execute(change_schema)
        sql_query = 'SELECT * FROM "' + file + '" WHERE "Dates"=?'
        cur.execute(sql_query, date)
        records = cur.fetchall()
        t = np.array([])
        y = np.array([])
        for row in records:
            if row[2] and row[1]:
                t = np.append(t, float(row[1]))
                y = np.append(y, float(row[2]))

    except (Exception, dbapi.DatabaseError) as error:
        print(error)
    if conn is not None:
        conn.close()

    curve, status = calibrate_ns_ols(t, y, tau0=1.0)  # starting value of 1.0 for the optimization of tau
    xi = t
    yi = curve(t)
    assert status.success

    # positions to inter/extrapolate
    x = np.linspace(0, 60, 61)
    # spline order: 1 linear, 2 quadratic, 3 cubic ...
    order = 1
    # do inter/extrapolation
    s = InterpolatedUnivariateSpline(xi, yi, k=order)
    r = s(x)

    #plt.figure()
    #plt.title('Yield Curve for Nelson Siegel algorithm\nDate: ' + date, fontsize=15)
    #plt.xlabel('Time to Maturity (in months)')
    #plt.ylabel('Yields (%)')
    plt.plot(x, r, label='yield data points')
    plt.grid(linestyle='--', linewidth=1)
    plt.legend()
    plt.show() 

    

@views.route("/about")
def about():
    return """
    <h1 style='color: red;'>I'm a red H1 heading!</h1>
    <p>This is a lovely little paragraph</p>
    <code>Flask is <em>awesome</em></code>
    """