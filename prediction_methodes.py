import os
import pickle

from dotenv import load_dotenv
import google.generativeai as genai
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
from flask import Flask, redirect, render_template, request, url_for,session



# Load the saved model

# model_file_path = 'random_forest_model_semifinal.pkl'
# with open(model_file_path, 'rb') as model_file:
#     model = pickle.load(model_file)


# Here is the TEMp FUntion
matplotlib.use('Agg')
load_dotenv()
# Configure the API key and generative model
# Load the saved model
model_file_path = 'random_forest_model_semifinal.pkl'
with open(model_file_path, 'rb') as model_file:
    model = pickle.load(model_file)
    
def categorize_customer(row):
    if (row['CLV'] >= 10000 and row['annual_income'] >= 80000 and 
        row['debt_to_income'] <= 0.2 and row['credit_utilization_ratio'] <= 0.3):
        return 'Platinum'
    elif (row['CLV'] >= 5000 and row['annual_income'] >= 50000 and 
          row['debt_to_income'] <= 0.4 and row['credit_utilization_ratio'] <= 0.5):
        return 'Gold'
    elif (row['CLV'] >= 2000 and row['annual_income'] >= 30000 and 
          row['debt_to_income'] <= 0.6 and row['credit_utilization_ratio'] <= 0.7 ):
        return 'Silver'
    else:
        return 'Bronze'

# Configure the API key and generative model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

generation_model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config
)

def generate_recommendation(tier, customer_profile):
    chat_session = generation_model.start_chat(history=[])
    prompt = (f"Generate personalized recommendations for a {tier} customer with the following profile: {customer_profile}. The goal is to provide offers and suggestions that will help to retain the customer for future Transactions. Format the recommendations as simple bullet points and include only the top 4 best offers that would be most appealing to the customer. The output format should be simple bullet points with plain Text no formatting")
    response = chat_session.send_message(prompt)
    recommendations = response.text.strip()
    return recommendations



# Generate Visulization


# def generate_visualizations(data, is_manual=False):
#     if not os.path.exists('static'):
#         os.makedirs('static')

#     data.loc[:, 'average_purchase_history'] = data['monthly_payment_burden'] * data['total_credit_utilized']

#     data.loc[:, 'average_purchase_value'] = np.where(data['total_credit_limit'] == 0,0,data['paid_principal'] / (data['total_credit_limit'] + 1e-6))


#     if 'ID' in data.columns:
#         data.loc[:, 'ID'] = data['ID'].astype(str)

#     # Plot 1: Average Purchase History per Customer
#     plt.figure(figsize=(6,2))
#     bar_width = 0.4  # Set the bar width here
#     x = np.arange(len(data))  # X locations for the groups
#     plt.bar(x, data['average_purchase_history'], width=bar_width, color='lightgreen', edgecolor='k')
#     plt.title('Average Purchase History per Customer')
#     plt.xlabel('Customer ID' if not is_manual else 'Manual Input')
#     plt.ylabel('Average Purchase History')
#     if 'ID' in data.columns:
#         plt.xticks(x, data['ID'], rotation=90)
#     else:
#         plt.xticks(x, range(1, len(data) + 1), rotation=90)
    
#     # Set custom y-axis limits if needed
#     y_min = data['average_purchase_history'].min() * 0.9
#     y_max = data['average_purchase_history'].max() * 1.1
#     plt.ylim(y_min, y_max)
    
#     plot1_path = 'static/average_purchase_history.png'
#     plt.tight_layout()
#     plt.savefig(plot1_path)
#     plt.close()

#     # Plot 2: Average Purchase Value per Customer
#     plt.figure(figsize=(6, 2))
#     bar_width = 0.4  # Set the bar width here
#     x = np.arange(len(data))  # X locations for the groups
#     plt.bar(x, data['average_purchase_value'], width=bar_width, color='lightblue', edgecolor='k')
#     plt.title('Average Purchase Value per Customer')
#     plt.xlabel('Customer ID' if not is_manual else 'Manual Input')
#     plt.ylabel('Average Purchase Value')
#     if 'ID' in data.columns:
#         plt.xticks(x, data['ID'], rotation=90)
#     else:
#         plt.xticks(x, range(1, len(data) + 1), rotation=90)

#     # Set custom y-axis limits if needed
#     y_min = data['average_purchase_value'].min() * 0.9
#     y_max = data['average_purchase_value'].max() * 1.1
#     plt.ylim(y_min, y_max)
    
#     plot2_path = 'static/average_purchase_value.png'
#     plt.tight_layout()
#     plt.savefig(plot2_path)
#     plt.close()

#     return plot1_path, plot2_path


def generate_visualizations(data, is_manual=False):
    if not os.path.exists('static'):
        os.makedirs('static')

    data.loc[:, 'average_purchase_history'] = data['monthly_payment_burden'] * data['total_credit_utilized']

    if 'ID' in data.columns:
        data.loc[:, 'ID'] = data['ID'].astype(str)

    # Plot 1: Average Purchase History per Customer (Bar Chart)
    plt.figure(figsize=(7, 4))  # Consistent figure size for alignment
    bar_width = 0.4
    x = np.arange(len(data))
    plt.bar(x, data['average_purchase_history'], width=bar_width, color='lightgreen', edgecolor='k')
    plt.title('Average Purchase History per Customer')
    plt.xlabel('Customer ID' if not is_manual else 'Manual Input')
    plt.ylabel('Average Purchase History')
    if 'ID' in data.columns:
        plt.xticks(x, data['ID'], rotation=90)
    else:
        plt.xticks(x, range(1, len(data) + 1), rotation=90)
    
    y_min = data['average_purchase_history'].min() * 0.9
    y_max = data['average_purchase_history'].max() * 1.1
    plt.ylim(y_min, y_max)
    
    plot1_path = 'static/average_purchase_history.png'
    plt.tight_layout()
    plt.savefig(plot1_path)
    plt.close()

    # Plot 2: Distribution of Credit Utilization and Payments (Pie Chart)
    plt.figure(figsize=(7, 4))  # Consistent figure size for alignment
    categories = ['Credit Utilized', 'Paid Principal', 'Credit Limit']  # Example categories
    values = [
        data['total_credit_utilized'].sum(),
        data['paid_principal'].sum(),
        data['total_credit_limit'].sum()
    ]
    
    def autopct_format(values):
        def my_format(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return f'{pct:.1f}%\n({val:d})'
        return my_format
    
    plt.pie(values, labels=categories, autopct=autopct_format(values), startangle=140, colors=['gold', 'lightcoral', 'lightskyblue'])
    plt.title('Distribution of Credit Utilization and Payments')
    
    plot2_path = 'static/credit_utilization_distribution.png'
    plt.tight_layout()
    plt.savefig(plot2_path)
    plt.close()

    return plot1_path, plot2_path


# Handle Manual Form Requirements
def handle_manual_requirements(manual_data,prediction):
                    # Calculate CLV,
                    manual_data.loc[:,'CLV'] = (
                        (manual_data['annual_income'] * manual_data['loan_to_income_ratio']) +
                        (manual_data['paid_interest'] - manual_data['paid_late_fees']) +
                        (manual_data['balance'] * manual_data['credit_utilization_ratio']) -
                        (manual_data['debt_to_income'])
                    )
                    manual_data.loc[:,'tier'] = manual_data.apply(categorize_customer, axis=1)
                    
                    customer_profile = manual_data.to_dict(orient='records')[0]
                    recommendation = generate_recommendation(manual_data['tier'].iloc[0], customer_profile)
                    recommendation_list = recommendation.split('\n')  # Split recommendations by newline
                    
                    # Generate visualizations
                    manual_plot_url1, manual_plot_url2 = generate_visualizations(manual_data, is_manual=True)

                    session["plt1_path"]=manual_plot_url1
                    session["plt2_path"]=manual_plot_url2

                    
                    # Convert manual data to HTML
                    manual_data_html = manual_data.to_html(classes='data', header="true")

                    customer_profile_serializable = {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in customer_profile.items()}

                    session['customer_profile'] = customer_profile_serializable
                    session['prediction'] = prediction[0].tolist()
                    session['recommendation'] = recommendation_list

                    return manual_plot_url1,manual_plot_url2,manual_data_html,recommendation_list


# Handle CLV
def handle_file_requirements(filtered_data,prediction):
                        filtered_data.loc[:,'CLV'] = (
                            (filtered_data['annual_income'] * filtered_data['loan_to_income_ratio']) +
                            (filtered_data['paid_interest'] - filtered_data['paid_late_fees']) +
                            (filtered_data['balance'] * filtered_data['credit_utilization_ratio']) -
                            (filtered_data['debt_to_income'])
                        ).round(2)
                        
                        filtered_data.loc[:,'tier'] = filtered_data.apply(categorize_customer, axis=1)
                        
                        customer_profile = filtered_data.to_dict(orient='records')[0]
                        recommendation = generate_recommendation(filtered_data['tier'].iloc[0], customer_profile)
                        recommendation_list = recommendation.split('\n')  # Split recommendations by newline
                        
                        # Generate visualizations
                        plot_url1, plot_url2 = generate_visualizations(filtered_data)

                        # Convert data to JSON serializable format
                        customer_profile_serializable = {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in customer_profile.items()}

                        # Store data in session
                        session['customer_profile'] = customer_profile_serializable
                        session['prediction'] = prediction[0].tolist()
                        session['recommendation'] = recommendation_list
                        return plot_url1,plot_url2,recommendation_list