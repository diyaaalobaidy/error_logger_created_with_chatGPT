import sqlite3
import traceback
from datetime import datetime

def log_error(error):
    # Connect to the database
    conn = sqlite3.connect('errors.db')
    cursor = conn.cursor()

    # Create the errors table if it doesn't already exist
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS errors (
            error_text TEXT,
            line INTEGER,
            function TEXT,
            filename TEXT,
            timestamp TEXT,
            traceback TEXT
        )
        '''
    )

    # Get the traceback and extract the relevant information
    tb = traceback.extract_tb(error.__traceback__)
    line = tb[-1].lineno
    function = tb[-1].name
    filename = tb[-1].filename

    # Format the traceback into a string
    traceback_str = ''.join(traceback.format_tb(error.__traceback__))

    # Get the current time
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert the error into the database
    cursor.execute(
        '''
        INSERT INTO errors (error_text, line, function, filename, timestamp, traceback)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (error, line, function, filename, timestamp, traceback_str)
    )

    # Save the changes to the database
    conn.commit()

    # Close the database connection
    conn.close()
