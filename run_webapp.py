"""Build webapp"""

import json
from cryptography.fernet import Fernet
import streamlit as st
import process_data
import connect_sql as consql


CONFIG_JSON = "config.json"

STYLE_MODS = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """


def establish_connection(config_file: str, login_details: tuple) -> list:
    """Sets up configuration for the MySQL server connection, decrypts
       user login information and grabs the data using their credentials

    Input Parameters:
    -----------------
    config_file     Type:   str
                    Use:    Filename for the configuration file containing
                            database information and encryption keys

    login_details   Type:   tuple
                    Use:    Tuple containing the user-submitted username 
                            and encrypted password

    Output Parameters:
    -----------------

    data            Type:   list
                    Use:    Data extracted from a table in the MySQL 
                            database
    """
    with open(config_file, 'r') as file:
        config_data = json.load(file)

    fernet = Fernet(config_data['encryption']['key'].encode("utf-8"))
    password = fernet.decrypt(login_details[1]).decode()

    server_config = (config_data['server']['host'],
                    login_details[0],
                    password,
                    config_data['database']['name'])

    query = "SELECT * FROM " + config_data['table']['name']
    connection = consql.connect_to_server(server_config)
    sql_data = consql.interact_with_server(connection, query)

    return sql_data


if __name__ == "__main__":

    st.title("Random Data Plots")
    st.markdown(STYLE_MODS, unsafe_allow_html=True)

    username = st.text_input("Input Username: ")
    key_password = st.text_input("Input Encrypted Password: ")

    if username and key_password:

        # Columns isn't used but it's there if needed  \(o_o)/
        data, columns = establish_connection(CONFIG_JSON, (username, key_password))
        dataframes = process_data.process(data, columns)

        st.subheader("Participant Scores")
        st.scatter_chart(data=dataframes[0], size=0.2)

        st.subheader("Participant Status Breakdown")
        st.bar_chart(dataframes[2], horizontal=False, color=["#E63946", "#EDAE49", "#33768D", "#52489C"])

        st.subheader("Participant Locations")
        st.map(dataframes[1])
