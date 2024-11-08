"""Functions for establishing a MySQL database connection and pulling data
   from a specified table"""

import mysql.connector


def connect_to_server(config: tuple) -> mysql.connector.connection.MySQLConnection:
    """Executes the database query and returns the data from a specified
       table

    Input Parameters:
    -----------------
    config          Type:   tuple
                    Use:    Tuple containing the host name, username, user
                            password and desired database to connect with

    Output Parameters:
    -----------------

    data            Type:   mysql.connector.connection.MySQLConnection
                    Use:    Object establishing the connection to a specified
                            MySQL database
    """
    try:
        connection = mysql.connector.MySQLConnection(
            host=config[0],
            user=config[1],
            password=config[2],
            database=config[3]
        )
        print("Connection established with " + str(config[0]))
        return connection

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    return []


def fetch_data(cursor: mysql.connector.cursor.MySQLCursor, query: str) -> list:
    """Executes the database query and returns the data from a specified
       table

    Input Parameters:
    -----------------
    cursor          Type:   mysql.connector.cursor.MySQLCursor
                    Use:    Object that executes database operations, in this
                            case fetching data from a table

    query           Type:   str
                    Use:    Query for the server in SQL. In this case, fetching
                            the data we want from a database
                            (e.g SELECT * FROM database_name)

    Output Parameters:
    -----------------

    data            Type:   list
                    Use:    Data extracted from the MySQL database in list format
    """
    data = []

    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            data.append(list(row))
        return data

    print("No data found in the table")
    return []


def interact_with_server(connection: mysql.connector.connection.MySQLConnection, query:str) -> list:
    """Sets up a cursor object that executes the SQL query, closes the server
       connection on completion

    Input Parameters:
    -----------------
    connection      Type:   mysql.connector.connection.MySQLConnection
                    Use:    Object establishing the connection to a specified
                            MySQL server

    query           Type:   str
                    Use:    Query for the server in SQL. In this case, fetching
                            the data we want from a database
                            (e.g SELECT * FROM database_name)

    Output Parameters:
    -----------------

    data            Type:   list
                    Use:    Data extracted from the MySQL database in list format
    """
    if connection.is_connected():

        cursor = connection.cursor()
        data = fetch_data(cursor, query)
        columns = cursor.column_names

        cursor.close()
        connection.close()
        print("Connection closed")

        return data, columns

    return [], []
