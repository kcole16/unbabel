import psycopg2
import sys
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

def get_database_connection():
	conn_string = "dbname='unbabel'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	return cursor
