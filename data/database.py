import mysql.connector
from mysql.connector import Error
from utils.logging_utils import log_change

# Save data to database
def save_to_database(timestamp, real_price, predicted_price, decision, DATABASE_CONFIG):
    try:
        connection = mysql.connector.connect(DATABASE_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()
            query = """
                INSERT INTO predictions (timestamp, real_price, predicted_price, decision)
                VALUES (%s, %s, %s, %s)
            """
            # Konverze dat na nativní typy Pythonu
            data = (
                int(timestamp),            # Ujistěte se, že timestamp je integer
                float(real_price),         # Převeďte numpy.float64 na float
                float(predicted_price),     # Převeďte numpy.float64 na float
                str(decision)              # prevene na string
            )
            # Vložení dat
            cursor.execute(query, data)
            connection.commit()
            log_change(f"Prediction saved to database: {real_price} -> {predicted_price}, Decision: {decision}")
    except Error as e:
        log_change(f"Database error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Fetch predictions from database
def fetch_predictions_from_db(DATABASE_CONFIG):
    try:
        connection = mysql.connector.connect(DATABASE_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT timestamp, real_price, predicted_price FROM predictions ORDER BY timestamp DESC LIMIT 10"
            cursor.execute(query)
            predictions = cursor.fetchall()
            log_change(f"Fetched {len(predictions)} predictions from database.")
            return predictions
    except Error as e:
        log_change(f"Database error while fetching predictions: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()