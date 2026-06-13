from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import json
import os
from datetime import datetime
from hashlib import sha256
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

init_files()
# File paths
USERS_FILE = 'users.json'
TRANSACTIONS_FILE = 'transactions.json'

# Initialize JSON files
def init_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, 'w') as f:
            json.dump({}, f)
# ---------------------------------
@app.route("/health")
def health():
    return "OK", 200
# ---------------------------------
# Hash password
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Load users
def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

# Save users
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

# Load transactions
def load_transactions():
    with open(TRANSACTIONS_FILE, 'r') as f:
        return json.load(f)

# Save transactions
def save_transactions(transactions):
    with open(TRANSACTIONS_FILE, 'w') as f:
        json.dump(transactions, f, indent=2)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or not session.get('is_admin'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'})
        
        users = load_users()
        if username in users:
            return jsonify({'success': False, 'message': 'Username already exists'})
        
        users[username] = {
            'password': hash_password(password),
            'balance': 0.0,
            'is_admin': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        save_users(users)
        
        return jsonify({'success': True, 'message': 'Registration successful'})
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        users = load_users()
        if username not in users or users[username]['password'] != hash_password(password):
            return jsonify({'success': False, 'message': 'Invalid username or password'})
        
        session['user'] = username
        session['is_admin'] = users[username].get('is_admin', False)
        
        return jsonify({'success': True, 'message': 'Login successful'})
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/balance')
@login_required
def get_balance():
    users = load_users()
    balance = users[session['user']]['balance']
    return jsonify({'balance': balance})

@app.route('/api/deposit', methods=['POST'])
@login_required
def deposit():
    data = request.get_json()
    amount = data.get('amount', 0)
    
    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({'success': False, 'message': 'Amount must be positive'})
    except:
        return jsonify({'success': False, 'message': 'Invalid amount'})
    
    users = load_users()
    username = session['user']
    users[username]['balance'] += amount
    save_users(users)
    
    # Log transaction
    transactions = load_transactions()
    if username not in transactions:
        transactions[username] = []
    
    transactions[username].append({
        'type': 'deposit',
        'amount': amount,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'description': 'Deposit'
    })
    save_transactions(transactions)
    
    return jsonify({'success': True, 'message': 'Deposit successful', 'balance': users[username]['balance']})

@app.route('/api/withdraw', methods=['POST'])
@login_required
def withdraw():
    data = request.get_json()
    amount = data.get('amount', 0)
    
    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({'success': False, 'message': 'Amount must be positive'})
    except:
        return jsonify({'success': False, 'message': 'Invalid amount'})
    
    users = load_users()
    username = session['user']
    
    if users[username]['balance'] < amount:
        return jsonify({'success': False, 'message': 'Insufficient balance'})
    
    users[username]['balance'] -= amount
    save_users(users)
    
    # Log transaction
    transactions = load_transactions()
    if username not in transactions:
        transactions[username] = []
    
    transactions[username].append({
        'type': 'withdraw',
        'amount': amount,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'description': 'Withdrawal'
    })
    save_transactions(transactions)
    
    return jsonify({'success': True, 'message': 'Withdrawal successful', 'balance': users[username]['balance']})

@app.route('/api/transfer', methods=['POST'])
@login_required
def transfer():
    data = request.get_json()
    recipient = data.get('recipient', '').strip()
    amount = data.get('amount', 0)
    
    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({'success': False, 'message': 'Amount must be positive'})
    except:
        return jsonify({'success': False, 'message': 'Invalid amount'})
    
    users = load_users()
    username = session['user']
    
    if not recipient or recipient not in users:
        return jsonify({'success': False, 'message': 'Recipient not found'})
    
    if username == recipient:
        return jsonify({'success': False, 'message': 'Cannot transfer to yourself'})
    
    if users[username]['balance'] < amount:
        return jsonify({'success': False, 'message': 'Insufficient balance'})
    
    users[username]['balance'] -= amount
    users[recipient]['balance'] += amount
    save_users(users)
    
    # Log transactions
    transactions = load_transactions()
    if username not in transactions:
        transactions[username] = []
    if recipient not in transactions:
        transactions[recipient] = []
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    transactions[username].append({
        'type': 'transfer_out',
        'amount': amount,
        'timestamp': timestamp,
        'description': f'Transfer to {recipient}'
    })
    transactions[recipient].append({
        'type': 'transfer_in',
        'amount': amount,
        'timestamp': timestamp,
        'description': f'Transfer from {username}'
    })
    save_transactions(transactions)
    
    return jsonify({'success': True, 'message': 'Transfer successful', 'balance': users[username]['balance']})

@app.route('/api/transactions')
@login_required
def get_transactions():
    transactions = load_transactions()
    username = session['user']
    user_transactions = transactions.get(username, [])
    return jsonify({'transactions': user_transactions[-20:][::-1]})  # Last 20, newest first

@app.route('/admin')
@admin_required
def admin():
    return render_template('admin.html')

@app.route('/api/admin/users')
@admin_required
def admin_get_users():
    users = load_users()
    user_list = []
    for username, data in users.items():
        user_list.append({
            'username': username,
            'balance': data['balance'],
            'is_admin': data.get('is_admin', False),
            'created_at': data.get('created_at', '')
        })
    return jsonify({'users': user_list})

@app.route('/api/admin/user/<username>/balance', methods=['POST'])
@admin_required
def admin_set_balance(username):
    data = request.get_json()
    balance = data.get('balance', 0)
    
    try:
        balance = float(balance)
        if balance < 0:
            return jsonify({'success': False, 'message': 'Balance cannot be negative'})
    except:
        return jsonify({'success': False, 'message': 'Invalid balance'})
    
    users = load_users()
    if username not in users:
        return jsonify({'success': False, 'message': 'User not found'})
    
    users[username]['balance'] = balance
    save_users(users)
    
    return jsonify({'success': True, 'message': 'Balance updated'})

@app.route('/api/admin/user/<username>/make-admin', methods=['POST'])
@admin_required
def admin_make_admin(username):
    users = load_users()
    if username not in users:
        return jsonify({'success': False, 'message': 'User not found'})
    
    users[username]['is_admin'] = True
    save_users(users)
    
    return jsonify({'success': True, 'message': 'User promoted to admin'})

@app.route('/api/admin/user/<username>/delete', methods=['POST'])
@admin_required
def admin_delete_user(username):
    if username == session['user']:
        return jsonify({'success': False, 'message': 'Cannot delete your own account'})
    
    users = load_users()
    if username not in users:
        return jsonify({'success': False, 'message': 'User not found'})
    
    del users[username]
    save_users(users)
    
    transactions = load_transactions()
    if username in transactions:
        del transactions[username]
    save_transactions(transactions)
    
    return jsonify({'success': True, 'message': 'User deleted'})

# if __name__ == '__main__':
#     init_files()
#     app.run(debug=True)
if __name__ == '__main__':
    init_files()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
