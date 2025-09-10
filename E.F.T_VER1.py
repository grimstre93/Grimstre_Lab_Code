from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import json
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import io
import base64
import csv

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Load data from JSON file
def load_data():
    try:
        with open('finance_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default data structure if file doesn't exist
        return {
            "history": [],
            "total_savings": 472000,
            "short_term_savings": 0,
            "food_inventory": {
                "maize": 0,
                "rice": 0,
                "beans": 0,
                "wheat": 0,
                "sorghum": 0
            },
            "food_prices": {
                "maize": {"buy": 2500, "sell": 2200},
                "rice": {"buy": 6000, "sell": 5500},
                "beans": {"buy": 8000, "sell": 7500},
                "wheat": {"buy": 3500, "sell": 3200},
                "sorghum": {"buy": 2000, "sell": 1800}
            }
        }

# Save data to JSON file
def save_data(data):
    with open('finance_data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Home page - Month selector
@app.route('/', methods=['GET', 'POST'])
@app.route('/month_selector', methods=['GET', 'POST'])
def month_selector():
    data = load_data()
    
    if request.method == 'POST':
        month = request.form['month']
        action = request.form['action']
        
        # Check if month already exists
        month_exists = any(m['month'] == month for m in data['history'])
        
        if action == 'new' and month_exists:
            flash(f"Month {month} already exists. Please choose 'Load Existing Month' or select a different month.", 'error')
            return redirect(url_for('month_selector'))
        elif action == 'load' and not month_exists:
            flash(f"No data found for {month}. Please create a new month instead.", 'error')
            return redirect(url_for('month_selector'))
        
        # Store selected month in session or pass as parameter
        if action == 'new':
            # Create new month entry
            new_month = {
                "month": month,
                "income": 0,
                "savings_reserve": 0,
                "investments": 0,
                "emergency_fund": 0,
                "available_budget": 0,
                "expenditures": {
                    "upkeep": 0,
                    "transport": 0,
                    "utilities": 0,
                    "entertainment": 0,
                    "rent": 0
                },
                "food_purchases": [],
                "food_sales": [],
                "savings": {
                    "total": 0,
                    "reserve": 0,
                    "investments": 0,
                    "emergency": 0
                },
                "loan": {
                    "needed": False,
                    "total": 0
                },
                "budget_analysis": {}
            }
            
            # Add to history if it doesn't exist
            if not month_exists:
                data['history'].append(new_month)
                save_data(data)
            
            return redirect(url_for('income', month=month))
        else:  # Load existing
            return redirect(url_for('results', month=month))
    
    return render_template('month_selector.html', data=data)

# Income page
@app.route('/income', methods=['GET', 'POST'])
def income():
    month = request.args.get('month')
    data = load_data()
    
    # Find the current month in history
    current_month = next((m for m in data['history'] if m['month'] == month), None)
    
    if not current_month:
        flash('Month not found. Please select a valid month.', 'error')
        return redirect(url_for('month_selector'))
    
    if request.method == 'POST':
        income = float(request.form['income'])
        
        # Calculate allocations
        savings_reserve = income * 0.3  # 30%
        investments = income * 0.1      # 10%
        emergency_fund = income * 0.1   # 10%
        available_budget = income * 0.5  # 50%
        
        # Update month data
        current_month['income'] = income
        current_month['savings_reserve'] = savings_reserve
        current_month['investments'] = investments
        current_month['emergency_fund'] = emergency_fund
        current_month['available_budget'] = available_budget
        
        # Save data
        save_data(data)
        
        return redirect(url_for('expenditure', month=month))
    
    return render_template('income.html', current_month=current_month, data=data)

# Expenditure page
@app.route('/expenditure', methods=['GET', 'POST'])
def expenditure():
    month = request.args.get('month')
    data = load_data()
    
    # Find the current month in history
    current_month = next((m for m in data['history'] if m['month'] == month), None)
    
    if not current_month:
        flash('Month not found. Please select a valid month.', 'error')
        return redirect(url_for('month_selector'))
    
    if request.method == 'POST':
        # Get regular expenses
        current_month['expenditures']['upkeep'] = float(request.form['upkeep'])
        current_month['expenditures']['transport'] = float(request.form.get('transport', 0))
        current_month['expenditures']['utilities'] = float(request.form.get('utilities', 0))
        current_month['expenditures']['entertainment'] = float(request.form.get('entertainment', 0))
        current_month['expenditures']['rent'] = float(request.form.get('rent', 0))
        
        # Process food transactions
        food_purchases = []
        food_sales = []
        
        for food in data['food_prices'].keys():
            # Update food prices
            buy_price = float(request.form[f'{food}_buy'])
            sell_price = float(request.form[f'{food}_sell'])
            data['food_prices'][food]['buy'] = buy_price
            data['food_prices'][food]['sell'] = sell_price
            
            # Process quantity
            qty = float(request.form.get(f'{food}_qty', 0))
            
            if qty > 0:  # Buying
                cost = qty * buy_price
                food_purchases.append({
                    'food': food,
                    'quantity': qty,
                    'price': buy_price,
                    'cost': cost
                })
                data['food_inventory'][food] = data['food_inventory'].get(food, 0) + qty
            elif qty < 0:  # Selling
                qty_abs = abs(qty)
                if data['food_inventory'].get(food, 0) >= qty_abs:
                    income = qty_abs * sell_price
                    food_sales.append({
                        'food': food,
                        'quantity': qty_abs,
                        'price': sell_price,
                        'income': income
                    })
                    data['food_inventory'][food] = data['food_inventory'].get(food, 0) - qty_abs
        
        current_month['food_purchases'] = food_purchases
        current_month['food_sales'] = food_sales
        
        # Calculate total expenses
        total_expenses = sum(current_month['expenditures'].values())
        total_expenses += sum(item['cost'] for item in food_purchases)
        total_expenses -= sum(item['income'] for item in food_sales)
        
        # Check if loan is needed
        loan_needed = total_expenses > current_month['available_budget']
        loan_amount = max(0, total_expenses - current_month['available_budget'])
        
        current_month['loan']['needed'] = loan_needed
        current_month['loan']['total'] = loan_amount
        
        # Update savings
        if not loan_needed:
            # Add remaining budget to short-term savings
            remaining_budget = current_month['available_budget'] - total_expenses
            data['short_term_savings'] += remaining_budget
            
            # Add to long-term savings
            data['total_savings'] += current_month['savings_reserve']
            data['total_savings'] += current_month['investments']
            data['total_savings'] += current_month['emergency_fund']
        
        # Calculate budget analysis
        planned_budget = current_month['available_budget'] * 0.5  # Assume 50% for regular expenses
        actual_expenses = sum(current_month['expenditures'].values())
        
        variance_percentage = ((actual_expenses - planned_budget) / planned_budget * 100) if planned_budget > 0 else 0
        
        current_month['budget_analysis'] = {
            'planned': {
                'regular': planned_budget,
                'food': current_month['available_budget'] * 0.3,  # 30% for food
                'other': current_month['available_budget'] * 0.2   # 20% for other
            },
            'actual': {
                'regular': actual_expenses,
                'food': sum(item['cost'] for item in food_purchases),
                'other': 0  # Placeholder for other expenses
            },
            'variance': {
                'regular': variance_percentage,
                'food': 0,  # Will be calculated
                'other': 0   # Will be calculated
            },
            'significant': abs(variance_percentage) > 10  # More than 10% variance is significant
        }
        
        # Save data
        save_data(data)
        
        return redirect(url_for('results', month=month))
    
    return render_template('expenditure.html', 
                         current_month=current_month, 
                         data=data,
                         food_prices=data['food_prices'])

# Results page
@app.route('/results')
def results():
    month = request.args.get('month')
    data = load_data()
    
    # Find the current month in history
    current_month = next((m for m in data['history'] if m['month'] == month), None)
    
    if not current_month:
        flash('Month not found. Please select a valid month.', 'error')
        return redirect(url_for('month_selector'))
    
    # Generate graphs
    graphs = generate_graphs(data, current_month)
    
    return render_template('results.html', 
                         current_month=current_month, 
                         data=data,
                         graphs=graphs)

# History page
@app.route('/history')
def history():
    data = load_data()
    return render_template('history.html', data=data)

# Clear all data
@app.route('/clear_data', methods=['POST'])
def clear_data():
    # Reset to initial data structure but keep food prices
    data = load_data()
    initial_food_prices = data['food_prices']
    
    new_data = {
        "history": [],
        "total_savings": 472000,
        "short_term_savings": 0,
        "food_inventory": {
            "maize": 0,
            "rice": 0,
            "beans": 0,
            "wheat": 0,
            "sorghum": 0
        },
        "food_prices": initial_food_prices
    }
    
    save_data(new_data)
    flash('All data has been cleared.', 'info')
    return redirect(url_for('history'))

# Export CSV
@app.route('/export_csv')
def export_csv():
    data = load_data()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Month', 'Income', 'Savings Reserve', 'Investments', 
                    'Emergency Fund', 'Available Budget', 'Upkeep', 'Transport',
                    'Utilities', 'Entertainment', 'Rent', 'Total Savings', 
                    'Loan Needed', 'Loan Amount'])
    
    # Write data
    for month in data['history']:
        writer.writerow([
            month['month'],
            month['income'],
            month['savings_reserve'],
            month['investments'],
            month['emergency_fund'],
            month['available_budget'],
            month['expenditures']['upkeep'],
            month['expenditures']['transport'],
            month['expenditures']['utilities'],
            month['expenditures']['entertainment'],
            month['expenditures']['rent'],
            month['savings']['total'],
            month['loan']['needed'],
            month['loan']['total']
        ])
    
    # Prepare response
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='financial_data.csv'
    )

# Generate graphs
def generate_graphs(data, current_month):
    graphs = {}
    
    # Budget Allocation Pie Chart
    plt.figure(figsize=(8, 6))
    labels = ['Savings Reserve', 'Investments', 'Emergency Fund', 'Available Budget']
    sizes = [
        current_month['savings_reserve'],
        current_month['investments'],
        current_month['emergency_fund'],
        current_month['available_budget']
    ]
    
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Budget Allocation')
    
    # Save to base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    graphs['budget_allocation'] = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    # Expense Breakdown Bar Chart
    plt.figure(figsize=(10, 6))
    expenses = current_month['expenditures']
    categories = list(expenses.keys())
    values = list(expenses.values())
    
    plt.bar(categories, values)
    plt.title('Expense Breakdown')
    plt.xlabel('Categories')
    plt.ylabel('Amount (KES)')
    plt.xticks(rotation=45)
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    graphs['expense_breakdown'] = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    # Savings Progress Chart
    if len(data['history']) > 1:
        plt.figure(figsize=(10, 6))
        months = [m['month'] for m in data['history']]
        savings = [m['savings']['total'] for m in data['history']]
        
        plt.plot(months, savings, marker='o')
        plt.title('Savings Progress Over Time')
        plt.xlabel('Month')
        plt.ylabel('Total Savings (KES)')
        plt.xticks(rotation=45)
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        graphs['savings_progress'] = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
    
    return graphs

if __name__ == '__main__':
    app.run(debug=True)