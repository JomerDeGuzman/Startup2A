# ===== DATABASE CONFIGURATION =====
# Store your MySQL database connection details here

DB_CONFIG = {
    'host': 'localhost',      # MySQL host
    'user': 'root',           # MySQL username
    'password': '',           # MySQL password (leave empty if no password)
    'database': 'sas_db'      # Database name
}

# This is where credentials should be stored
# In production, use environment variables instead:
# import os
# DB_CONFIG = {
#     'host': os.getenv('DB_HOST', 'localhost'),
#     'user': os.getenv('DB_USER', 'root'),
#     'password': os.getenv('DB_PASSWORD', ''),
#     'database': os.getenv('DB_NAME', 'sas_db')
# }
