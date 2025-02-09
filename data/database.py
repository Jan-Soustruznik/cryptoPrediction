import mysql.connector
from mysql.connector import Error
from utils.logging_utils import log_change


# Save data to database
def save_to_database(timestamp, symbol, interval, real_price, predicted_price, decision, DATABASE_CONFIG):
    try:
        # connect to db
        with mysql.connector.connect(**DATABASE_CONFIG) as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO predictions (timestamp, symbol, cycle, real_price, predicted_price, decision)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                # prepare data
                data = (
                    int(timestamp),           # integer
                    str(symbol),              # string
                    str(interval),            # string
                    float(real_price),        # float
                    float(predicted_price),   # float
                    str(decision)             # string
                )
                # insert to db
                cursor.execute(query, data)
                connection.commit()
                log_change(f"Prediction saved to database: {real_price} -> {predicted_price}, Decision: {decision}")

    except mysql.connector.Error as e:
        log_change(f"Database error: {e}")


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