import psycopg2
import sys

def get_database_connection():
	"""Connect to postgres db using psycopg2"""
	conn_string = "dbname='unbabel'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	return conn, cursor
