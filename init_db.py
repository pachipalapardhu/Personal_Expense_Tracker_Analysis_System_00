"""Create the MySQL database and migrate tracker tables for per-user ownership.
Existing shared rows are retained with user_id=NULL and are intentionally hidden
from all accounts until an administrator explicitly assigns them to an owner.
"""
import sys
import mysql.connector
from config import Config
import database


def main():
    try:
        print(f"Connecting to MySQL at {Config.MYSQL_HOST}:{Config.MYSQL_PORT} ...")
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST, port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER, password=Config.MYSQL_PASSWORD,
            connection_timeout=10
        )
        cur = conn.cursor()
        # Database name comes from trusted local environment configuration.
        db_name = Config.MYSQL_DB.replace('`', '')
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cur.close()
        conn.close()
        ok, message = database.init_db()
        print(message)
        if not ok:
            return 1
        print("MySQL is ready. Each account receives private categories and expenses.")
        print("Legacy records with no owner remain hidden; they are not shared with new users.")
        return 0
    except mysql.connector.Error as exc:
        print(f"MySQL connection failed: {exc}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
