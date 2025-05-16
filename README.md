# Order Management System

## A simple desktop application for managing customer orders built with Python.

![image](https://github.com/user-attachments/assets/f1dd371b-0212-4f93-b8ef-f659732ed8b5)

A demonstrational video: https://youtu.be/y6Ei50GOazk.

## Features

- User authentication system
- Create and manage customer orders
- Track order status (Registered, In Progress, Completed)
- Send SMS notifications to customers
- Filter and sort orders by various criteria

## Requirements

- Python 3.x
- CustomTkinter
- SQLite3

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/order-management-system.git
   ```

2. Install dependencies:
   ```
   pip install customtkinter
   ```

3. Run the application:
   ```
   cd src
   python orders.py
   ```

## Usage

### User Management

To add users to the system, uncomment and modify the appropriate lines in `users.py`:

```python
# add_user("username", "password")
# remove_user("username")
# print_users()
```

### Order Management

1. Login using your credentials
2. Add new orders with customer details
3. View and filter existing orders
4. Update order status
5. Send SMS notifications to customers

## Project Structure

- `src/` - Directory containing source code
   - `orders.py` - Main application file
   - `users.py` - User management module
- `data/` - Directory containing database files
  - `orders.db` - Orders database
  - `users.db` - User credentials database
