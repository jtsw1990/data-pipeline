'''Update tables in database.'''
# %%

import pyodbc
import os
from dotenv import load_dotenv
from pyodbc import Connection


def create_connection(server, db, user, password) -> Connection:
    '''Creates a connection object based on parameters.'''

    conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server +
                          ';DATABASE='+db+';UID='+user+';PWD=' + password)

    return conn


def insert_data_into_table(df, conn) -> None:
    '''Inserts into a dev table for testing.'''

    cursor = conn.cursor()
    for index, row in df.iterrows():
        cursor.execute(
            '''
            insert into dbo.dev_testing 
            (id, firstname, lastname, age) 
            values (?, ?, ?, ?)
            ''',
            row['id'], row['firstname'], row['lastname'], row['age']
        )
    conn.commit()
    cursor.close()


if __name__ == '__main__':
    load_dotenv()
    rds_server = os.environ['rds_server']
    db_name = os.environ['db_name']
    rds_user = os.environ['rds_user']
    rds_password = os.environ['rds_password']

    conn = create_connection(rds_server, db_name, rds_user, rds_password)


# %%
