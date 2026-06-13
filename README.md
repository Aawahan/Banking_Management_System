# Banking Management System

A modern, responsive banking system built with Flask and JSON for data storage. No databases, no APIs, no paid services required.

## Features

✅ User registration and login with password hashing
✅ Deposit and withdraw money
✅ Transfer money between users
✅ Check account balance
✅ Transaction history
✅ Admin dashboard (user management, balance control)
✅ Responsive mobile-friendly UI
✅ Session-based authentication

## Installation

### Prerequisites
- Python 3.8 or higher

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
python app.py
```

3. **Access the application:**
Open your browser and go to `http://localhost:5000`

## Default Admin Account

- **Username:** admin
- **Password:** password

Change this password immediately after first login!

## Project Structure

```
.
├── app.py                 # Flask application with all routes
├── requirements.txt       # Python dependencies
├── users.json            # User data storage
├── transactions.json     # Transaction history storage
└── templates/
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── dashboard.html    # User dashboard
    └── admin.html        # Admin panel
```

## Usage

### For Regular Users

1. **Register:** Click "Register" and create an account
2. **Login:** Enter your credentials
3. **Deposit:** Add funds to your account
4. **Withdraw:** Withdraw funds (balance must be sufficient)
5. **Transfer:** Send money to another user
6. **View History:** See all transactions in dashboard

### For Admins

1. **Access Admin Panel:** Click "Admin Panel" on dashboard
2. **View Users:** See all users and their balances
3. **Edit Balance:** Manually adjust user balances
4. **Promote User:** Make a user an admin
5. **Delete User:** Remove a user account

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - Login user
- `GET /logout` - Logout user

### User Operations
- `GET /api/balance` - Get current balance
- `POST /api/deposit` - Deposit money
- `POST /api/withdraw` - Withdraw money
- `POST /api/transfer` - Transfer to another user
- `GET /api/transactions` - Get transaction history

### Admin Operations
- `GET /api/admin/users` - Get all users
- `POST /api/admin/user/<username>/balance` - Update user balance
- `POST /api/admin/user/<username>/make-admin` - Promote to admin
- `POST /api/admin/user/<username>/delete` - Delete user

## Security Notes

- Passwords are hashed using SHA-256
- Session-based authentication
- JSON files should be backed up regularly
- For production, consider using a proper database

## Troubleshooting

**Port already in use:**
```bash
python -c "import os; os.environ['FLASK_ENV']='production'; exec(open('app.py').read())"
```

**JSON decode error:**
Delete `users.json` and `transactions.json`, they will be recreated automatically.

**Session not persisting:**
Clear browser cookies and login again.

## License

Free to use and modify.
