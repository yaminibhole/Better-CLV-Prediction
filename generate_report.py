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
path_wkhtmltopdf = r"wkhtmltox\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)





def generate_report(customer_data,prediction,recommendation_list):

    #print("Plot 1 : ",plot_url1)
    #print("Plot 2 : ",plot_url2)
    # Assuming your script is located in the main directory
    static_folder_path = os.path.join(os.getcwd(), 'static')
                                    
    if not isinstance(recommendation_list, list):
        recommendation_list = recommendation_list.split('\n')

    if not isinstance(prediction,int):
        prediction=int(prediction)

    #time.sleep(10)
    options = {'enable-local-file-access': None}  

    html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Customer Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ text-align: center; }}
                table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                table, th, td {{ border: 1px solid black; }}
                th, td {{ padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .recommendation-section {{ margin-top: 20px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9; }}
                .recommendation-list {{ list-style-type: disc; margin-left: 20px; font-size: 16px; }}

                .visualization-section {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: space-between;
                }}

                .plot {{
                    flex: 0 0 48%; /* Adjust the percentage to fit the width of two plots per row */
                    margin-bottom: 20px; /* Adds space between rows */
                }}

                .plot img {{
                    width: 100%;
                    height: auto; /* Maintains aspect ratio */
                }}
            </style>
        </head>
        <body>
            <h1>Customer Report</h1>
            <h2>Customer Account No.: {{{{ customer_data.ID if customer_data.ID else \'manual data\' }}}}</h2>
            <table>
                <tr><th>Field</th><th>Value</th></tr>
                {{ '{{% for key, value in customer_data.items() if key not in [\'ID\', \'prediction\', \'CLV\', \'recommendation\'] %}}' }}
                <tr><td>{{{{ key.replace(\'_\', \' \').title() }}}}</td><td>{{{{ value }}}}</td></tr>
                {{ '{{% endfor %}}' }}
            </table>
            <h2>Prediction: {prediction  }</h2>
            <h2>Calculated CLV: {customer_data["CLV"]}</h2>
            <div class="recommendation-section">
                <h3>Personalized Recommendations:</h3>
                <ul class="recommendation-list">
                    {{ '{{% for item in recommendation_list %}}' }}
                    <li> {{{{ item }}}} </li>
                    {{ '{{% endfor %}}' }}
                </ul>
            </div>
            <h2>Visualizations:</h2>
                    <div class="visualization-section">
                <div class="plot">
                    <h3>Plot 1: Average Purchase History per Customer</h3>
                    <img src="{os.path.join(static_folder_path, 'average_purchase_history.png')}" alt="Average Purchase History per Customer">
                </div>

                <div class="plot">
                    <h3>Plot 2: Distribution of Credit Utilization</h3>
                    <img src="{os.path.join(static_folder_path, 'credit_utilization_distribution.png')}" alt="Distribution of Credit Utilization">
                </div>
                <div class="plot">
                    <h3>Plot 3: Distribution Of Balance</h3>
                    <img src="{os.path.join(static_folder_path, 'balance_distribution.png')}" alt="Distribution Of Balance">
                </div>

                <div class="plot">
                    <h3>Plot 4: Proportion Of Total Credit Utilized</h3>
                    <img src="{os.path.join(static_folder_path, 'credit_utilization_donut.png')}" alt="Proportion Of Total Credit Utilized">
                </div>
                <div class="plot">
                    <h3>Plot 5: Loan-To-Income Ratio and Debt-to-Income Ratio</h3>
                    <img src="{os.path.join(static_folder_path, 'loan_debt_ratios.png')}" alt="Loan-To-Income Ratio and Debt-to-Income Ratio">
                </div>

                <div class="plot">
                    <h3>Plot 6: Distribution Of Monthly Payment Burden</h3>
                    <img src="{os.path.join(static_folder_path, 'monthly_payment_burden.png')}" alt="Distribution Of Monthly Payment Burden">
                </div>
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
