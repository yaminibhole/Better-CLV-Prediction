import os
import pickle
import secrets
import urllib.parse

import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdfkit
from flask import (Flask, jsonify, redirect, render_template, request,
                   send_file, session, url_for)
from jinja2 import Template

secret_key = secrets.token_hex(16)



# Configure pdfkit to use wkhtmltopdf
path_wkhtmltopdf = r"wkhtmltox\bin\wkhtmltopdf.exe"  # Use raw string
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


def generate_report(customer_data,prediction,recommendation_list):

    #print("Plot 1 : ",plot_url1)
    #print("Plot 2 : ",plot_url2)

                                    
    if not isinstance(recommendation_list, list):
        recommendation_list = recommendation_list.split('\n')

    if not isinstance(prediction,int):
        prediction=int(prediction)

    #time.sleep(10)
    options = {'enable-local-file-access': None}  

    html_template = r"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Customer Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { text-align: center; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
            table, th, td { border: 1px solid black; }
            th, td { padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .recommendation-section { margin-top: 20px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9; }
            .recommendation-list { list-style-type: disc; margin-left: 20px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>Customer Report</h1>
        <h2>Customer ID: {{customer_data.ID if customer_data.ID else 'manual data' }}</h2>
        <table>
            <tr><th>Field</th><th>Value</th></tr>
            {% for key, value in customer_data.items() if key not in ['ID', 'prediction', 'CLV', 'recommendation'] %}
            <tr><td>{{ key.replace('_', ' ').title() }}</td><td>{{ value }}</td></tr>
            {% endfor %}
        </table>
        <h2>Prediction: {{ prediction }}</h2>
        <h2>Calculated CLV: {{ customer_data.CLV }}</h2>
        <div class="recommendation-section">
            <h3>Personalized Recommendations:</h3>
            <ul class="recommendation-list">
                {% for item in recommendation_list %}
                <li>{{ item }}</li>
                {% endfor %}
            </ul>
        </div><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
        <h2>Visualizations:</h2>
        <div class="visualization-section">
            <h3>Plot 1: Average Purchase History per Customer</h3>
            <img src="C:\Users\asusb\OneDrive\Desktop\NPM PROgram\1.-Better-Customer-Lifetime-Value-CLV-Prediction\static\average_purchase_history.png" alt="Average Purchase History per Customer">

            <h3>Plot 2: Credit utilization distribution</h3>
            <img src="C:\Users\asusb\OneDrive\Desktop\NPM PROgram\1.-Better-Customer-Lifetime-Value-CLV-Prediction\static\credit_utilization_distribution.png">

        </div>

    </body>
    </html>
    """
    template = Template(html_template)
    html_content = template.render(customer_data=customer_data,
                                   prediction=prediction,
                                   recommendation_list=recommendation_list)

    # Debug print the HTML content
    # print("Generated HTML Content:")
    # print(html_content)

    pdf_file_path = f'reports/customer_report.pdf'
    pdfkit.from_string(html_content, pdf_file_path, configuration=config,options=options)

    return pdf_file_path
