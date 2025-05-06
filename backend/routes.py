from flask import render_template, request, redirect, url_for, flash
from backend.server import app
from backend.db import get_db_connection
import mysql.connector

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payment_report', methods=['GET', 'POST'])
def payment_report_form():
    if request.method == 'POST':
        # Get selected month
        selected_month = request.form['month']  # Format: YYYY-MM
        return redirect(url_for('payment_report_results', month=selected_month))

    return render_template('payment_report.html')

@app.route('/payment_report_results', methods=['GET'])
def payment_report_results():
    # Get the selected month from query parameters
    selected_month = request.args.get('month')
    
    if not selected_month:
        return "No month selected. Please try again."

    year, month = selected_month.split('-')

    try:
        # Connect to MySQL
        conn = get_db_connection()
        if conn:
            # Enable prepared statements
            cursor = conn.cursor(prepared=True)

            # Corrected prepared statement to sum up costs per user
            query = """
            SELECT u.userID, u.first, SUM(l.cost) AS total_cost
            FROM USERS u
            JOIN CLASS c ON u.userID = c.userID
            JOIN LEVEL l ON c.levelID = l.levelID
            WHERE YEAR(c.date) = %s AND MONTH(c.date) = %s
            GROUP BY u.userID, u.first
            ORDER BY u.userID
            """

            # Execute query using prepared statement
            cursor.execute(query, (year, month))

            # Fetch all results
            results = cursor.fetchall()

            cursor.close()
            conn.close()

            # Process the results for display
            payment_summary = []
            for userID, first, total_cost in results:
                payment_summary.append({
                    'userID': userID,
                    'name': first,
                    'total_cost': total_cost
                })

            # Render the results
            return render_template(
                'payment_report_results.html',
                month=selected_month,
                payments=payment_summary
            )
        else:
            return "Error connecting to database. Check your configuration."

    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return "Error connecting to database. Check your configuration."


# View all competitions
@app.route('/competitions')
def competitions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Competition ORDER BY startDate DESC")
    competitions = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('competitions.html', competitions=competitions)

# Create new competition
@app.route('/competitions/create', methods=['GET', 'POST'])
def create_competition():
    if request.method == 'POST':
        title = request.form['title']
        startDate = request.form['startDate']
        endDate = request.form['endDate']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Competition (title, startDate, endDate) VALUES (%s, %s, %s)",
            (title, startDate, endDate)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('competitions', success='created'))

    return render_template('create_competition.html')

# Edit competition
@app.route('/competitions/edit/<int:compID>', methods=['GET', 'POST'])
def edit_competition(compID):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        startDate = request.form['startDate']
        endDate = request.form['endDate']

        try:
            # Call the stored procedure instead of using raw SQL
            cursor.callproc('update_competition', (compID, title, startDate, endDate))
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return "Failed to update competition."

        cursor.close()
        conn.close()
        return redirect(url_for('competitions', success='updated'))

    cursor.execute("SELECT * FROM Competition WHERE compID = %s", (compID,))
    competition = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_competition.html', competition=competition)


# Delete competition
@app.route('/competitions/delete/<int:compID>', methods=['POST'])
def delete_competition(compID):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Competition WHERE compID = %s", (compID,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('competitions', success='deleted'))