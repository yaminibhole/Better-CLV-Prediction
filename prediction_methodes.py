import os
import pickle

import google.generativeai as genai
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for

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

#     if 'ID' in data.columns:
#         data.loc[:, 'ID'] = data['ID'].astype(str)

#     # Plot 1: Average Purchase History per Customer (Bar Chart)
#     plt.figure(figsize=(7, 4))  # Consistent figure size for alignment
#     bar_width = 0.4
#     x = np.arange(len(data))
#     plt.bar(x, data['average_purchase_history'], width=bar_width, color='lightgreen', edgecolor='k')
#     plt.title('Average Purchase History per Customer')
#     plt.xlabel('Customer ID' if not is_manual else 'Manual Input')
#     plt.ylabel('Average Purchase History')
#     if 'ID' in data.columns:
#         plt.xticks(x, data['ID'], rotation=90)
#     else:
#         plt.xticks(x, range(1, len(data) + 1), rotation=90)
    
#     y_min = data['average_purchase_history'].min() * 0.9
#     y_max = data['average_purchase_history'].max() * 1.1
#     plt.ylim(y_min, y_max)
    
#     plot1_path = 'static/average_purchase_history.png'
#     plt.tight_layout()
#     plt.savefig(plot1_path)
#     plt.close()

#     # Plot 2: Distribution of Credit Utilization and Payments (Pie Chart)
#     plt.figure(figsize=(7, 4))  # Consistent figure size for alignment
#     categories = ['Credit Utilized', 'Paid Principal', 'Credit Limit']  # Example categories
#     values = [
#         data['total_credit_utilized'].sum(),
#         data['paid_principal'].sum(),
#         data['total_credit_limit'].sum()
#     ]
    
#     def autopct_format(values):
#         def my_format(pct):
#             total = sum(values)
#             val = int(round(pct * total / 100.0))
#             return f'{pct:.1f}%\n({val:d})'
#         return my_format
    
#     plt.pie(values, labels=categories, autopct=autopct_format(values), startangle=140, colors=['gold', 'lightcoral', 'lightskyblue'])
#     plt.title('Distribution of Credit Utilization and Payments')
    
#     plot2_path = 'static/credit_utilization_distribution.png'
#     plt.tight_layout()
#     plt.savefig(plot2_path)
#     plt.close()

#     return plot1_path, plot2_path



def generate_visualizations(data, is_manual=False):
    # Ensure 'static' directory exists for saving images
    if not os.path.exists('static'):
        os.makedirs('static')

    # Calculate 'average_purchase_history' based on 'monthly_payment_burden' and 'total_credit_utilized'
    data['average_purchase_history'] = data['monthly_payment_burden'] * data['total_credit_utilized']

    # Convert 'ID' column to string for consistent labeling, if it exists
    if 'ID' in data.columns:
        data['ID'] = data['ID'].astype(str)

    record = data.iloc[0]  # Assuming only one record for the new visualizations

    ### Original Graphs

    # Plot 1: Average Purchase History per Customer (Bar Chart)

    plt.figure(figsize=(7, 4))  # Consistent figure size for alignment
    bar_width = 0.4
    x = np.arange(len(data))

    # Create the bar plot
    bars = plt.bar(x, data['average_purchase_history'], width=bar_width, color='lightgreen', edgecolor='k')
    plt.title('Average Purchase History per Customer')
    plt.xlabel('Customer Account Number' if not is_manual else 'Manual Input')
    plt.ylabel('Average Purchase History')

    # Adjust x-ticks based on whether 'ID' column is present
    if 'ID' in data.columns:
        plt.xticks(x, data['ID'], rotation=90)
    else:
        plt.xticks(x, range(1, len(data) + 1), rotation=90)

    # Set y-axis limits to ensure proper display of bars
    y_min = data['average_purchase_history'].min() * 0.9
    y_max = data['average_purchase_history'].max() * 1.1
    plt.ylim(y_min, y_max)

    # Annotate each bar with its value
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', 
                ha='center', va='bottom')

    # Save the plot
    plot1_path = 'static/average_purchase_history.png'
    plt.tight_layout()
    plt.savefig(plot1_path)
    plt.close()


    # Plot 2: Distribution of Credit Utilization and Payments (Pie Chart)
    plt.figure(figsize=(7, 4))  # Consistent figure size for alignment
    categories = ['Credit Utilized', 'Paid Principal', 'Credit Limit']  # Categories for the pie chart
    values = [
        data['total_credit_utilized'].sum(),
        data['paid_principal'].sum(),
        data['total_credit_limit'].sum()
    ]
    
    # Custom function to format the percentage display with actual values
    def autopct_format(values):
        def my_format(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return f'{pct:.1f}%\n({val:d})'
        return my_format
    
    # Create the pie chart
    plt.pie(values, labels=categories, autopct=autopct_format(values), startangle=140, colors=['gold', 'lightcoral', 'lightskyblue'])
    plt.title('Distribution of Credit Utilization and Payments')
    
    # Save the second plot
    plot2_path = 'static/credit_utilization_distribution.png'
    plt.tight_layout()
    plt.savefig(plot2_path)
    plt.close()

    ### New Graphs

    # # Plot 3: Loan-to-Income Ratio and Debt-to-Income Ratio (Bar Chart)

    # Create the bar chart
    plt.figure(figsize=(7, 4))
    ratios = ['Loan_Taken', 'Annual_Income']
    values = [record['loan_to_income_ratio'] * record['annual_income'], record['annual_income']]

    bars = plt.bar(ratios, values, color=['skyblue', 'lightgreen'], edgecolor='k')

    # Annotate the values on the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2f}', ha='center', va='bottom')

    # Set title and labels
    plt.title('Loan-to-Income Ratio and Debt-to-Income Ratio')
    plt.ylabel('Ratio')

    # Save the plot
    plot3_path = 'static/loan_debt_ratios.png'
    plt.tight_layout()
    plt.savefig(plot3_path)
    plt.close()


    # Plot 4: Credit Utilization Ratio (Gauge Chart)
    plt.figure(figsize=(7, 4))
    plt.subplot(1, 1, 1, projection='polar')
    theta = np.linspace(0, 2 * np.pi, 100)
    plt.fill_between(theta, 0, 1, color='lightgrey', alpha=0.5)
    
    theta_utilization = np.linspace(0, 2 * np.pi * record['credit_utilization_ratio'], 100)
    plt.fill_between(theta_utilization, 0, 1, color='gold')
    plt.title('Credit Utilization Ratio')
    plot4_path = 'static/credit_utilization_gauge.png'
    plt.tight_layout()
    plt.savefig(plot4_path)
    plt.close()

    # Plot 6: Monthly Payment Burden (Column Chart)
    plt.figure(figsize=(7, 4))
    plt.bar(['Monthly Payment Burden'], [record['monthly_payment_burden']], color='lightblue', edgecolor='k')
    plt.title('Monthly Payment Burden')
    plt.ylabel('Burden as % of Income')
    plot6_path = 'static/monthly_payment_burden.png'
    plt.tight_layout()
    plt.savefig(plot6_path)
    plt.close()

    # Plot 7: Proportion of Total Credit Utilized (Donut Chart)
    plt.figure(figsize=(7, 4))
    categories = ['Credit Utilized', 'Remaining Credit']
    values = [record['total_credit_utilized'], record['total_credit_limit'] - record['total_credit_utilized']]
    
    plt.pie(values, labels=categories, autopct=autopct_format(values), startangle=140, colors=['gold', 'lightgrey'])
    center_circle = plt.Circle((0,0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(center_circle)
    plt.title('Proportion of Total Credit Utilized')
    plot7_path = 'static/credit_utilization_donut.png'
    plt.tight_layout()
    plt.savefig(plot7_path)
    plt.close()

    # Return paths to all generated plots
    return plot1_path, plot2_path, plot3_path, plot4_path, plot6_path, plot7_path

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
                    plot1_path, plot2_path, plot3_path, plot4_path, plot6_path, plot7_path = generate_visualizations(manual_data, is_manual=True)

                    session["plt1_path"]=plot1_path
                    session["plt2_path"]=plot2_path
                    session["plt3_path"]=plot3_path
                    session["plt4_path"]=plot4_path
                    session["plt6_path"]=plot6_path
                    session["plt7_path"]=plot7_path

                    
                    # Convert manual data to HTML
                    manual_data_html = manual_data.to_html(classes='data', header="true")

                    customer_profile_serializable = {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in customer_profile.items()}

                    session['customer_profile'] = customer_profile_serializable
                    session['prediction'] = prediction[0].tolist()
                    session['recommendation'] = recommendation_list

                    return plot1_path,plot2_path,manual_data_html,recommendation_list


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
                        plot1_path, plot2_path, plot3_path, plot4_path, plot6_path, plot7_path = generate_visualizations(filtered_data)

                        session["plt1_path"]=plot1_path
                        session["plt2_path"]=plot2_path
                        session["plt3_path"]=plot3_path
                        session["plt4_path"]=plot4_path
                        session["plt6_path"]=plot6_path
                        session["plt7_path"]=plot7_path

                        # Convert data to JSON serializable format
                        customer_profile_serializable = {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in customer_profile.items()}




                        # Store data in session
                        session['customer_profile'] = customer_profile_serializable
                        session['prediction'] = prediction[0].tolist()
                        session['recommendation'] = recommendation_list
                        return plot1_path, plot2_path,recommendation_list
