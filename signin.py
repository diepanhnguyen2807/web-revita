from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'hehehe'  # Use a strong secret key in production


# Route for the sign-in page
@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Validate user credentials
        user = get_user_by_email_password(email, password)

        if user:
            # Store user data in session
            session['user'] = {
                'id': user[0],
                'email': user[1],
                'name': user[2],
                'phone_number': user[3],
                'password': user[4]
            }
            return redirect(url_for('home'))  # Redirect to the home page or dashboard
        else:
            # Invalid credentials, show an error message
            return render_template('sign-in.html', error="Invalid email or password")

    return render_template('sign-in.html')  # GET request, display the sign-in page


# Function to fetch user data from the database based on email and password
def get_user_by_email_password(email, password):
    conn = sqlite3.connect('db/users.db')
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE email = ? AND password = ?"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    conn.close()

    return user


# Home route for logged-in users
@app.route('/home')
def home():
    if 'user' in session:
        return f"Hello {session['user']['name']}! You are logged in."
    else:
        return redirect(url_for('sign_in'))  # Redirect to sign-in if not logged in


# Run the application
if __name__ == '__main__':
    app.run(debug=True)