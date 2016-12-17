from jenkinsapi.jenkins import Jenkins
from datetime import datetime

import sqlite3


def get_server_instance():
    jenkins_url = 'http://localhost:8080'
    server = Jenkins(jenkins_url, username='abc123', password='abc123')
    return server


def create_connection(jenkins_job_db):
    """ create a database connection to the SQLite database
    :param : database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(jenkins_job_db)
        return conn
    except Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "jenkins_job_db.db"

    sql_create_projects_table = """ CREATE TABLE
									IF NOT EXISTS jenkins_job_table (
									 job_name TEXT NOT NULL,
									 job_description TEXT,
									 is_running TEXT NOT NULL,
									 is_enabled TEXT NOT NULL,
									 last_build TEXT NOT NULL,
									 last_good_build TEXT NOT NULL,
									 last_good_build_revision TEXT NOT NULL,
									 check_time TEXT NOT NULL
									); """

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create jobs table
        create_table(conn, sql_create_projects_table)
        get_job_details(conn)
    else:
        print("Error! cannot create the database connection.")


"""Get job details of each job that is running on the Jenkins instance"""


def get_job_details(conn):
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()

    for j in server.get_jobs():
        job_instance = server.get_job(j[0])
        item = [str(job_instance.name), str(job_instance.get_description()), str(job_instance.is_running()), \
                 str(job_instance.is_enabled()), str(job_instance.get_last_build()), str(job_instance.get_last_good_build()), \
                 str(job_instance.get_last_good_build().get_revision()), str(datetime.now())]
        c = conn.cursor()
        c.execute('INSERT INTO jenkins_job_table VALUES (?,?,?,?,?,?,?,?)', item)
    conn.commit()
    c.execute('SELECT * FROM jenkins_job_table')
    for row in c:
        print (row)
    conn.close()

if __name__ == '__main__':
    main()
