import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from PIL import Image, ImageTk

# MySQL Database configuration - UPDATE THESE WITH YOUR CREDENTIALS
db_config = {
    'host': 'localhost',
    'user': 'root',  # Default MySQL username
    'password': '',  # Your MySQL password (empty if no password)
    'database': 'donations_db'
}

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect without specifying a database
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error creating database: {err}")

# Database setup
def setup_db():
    create_database()
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS donations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                amount DECIMAL(10, 2) NOT NULL
            )
        """)
        conn.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def add_donation(name, amount):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO donations (name, amount) VALUES (%s, %s)", (name, amount))
        conn.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def get_total_donations():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM donations")
        total = cursor.fetchone()[0]
        return total if total else 0
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return 0
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def get_donators():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT name, amount FROM donations ORDER BY amount DESC")
        donators = cursor.fetchall()
        return donators
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return []
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Main window
root = tk.Tk()
root.title("تبرع للأطفال في العيد")
root.geometry("600x400")

# Background image
try:
    bg_image = Image.open("eid-al-fitr-feature.jpg")  
    bg_image = bg_image.resize((600, 400), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo  
except Exception as e:
    print(f"Error loading background image: {e}")
    bg_photo = None

# [Rest of your GUI code remains exactly the same...]
# [Include all your welcome_page(), donation_page(), summary_page() functions]
# [They don't need any changes]

# Start the application
setup_db()
welcome_page()
root.mainloop()