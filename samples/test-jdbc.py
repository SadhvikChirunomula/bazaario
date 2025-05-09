#!/usr/bin/env python3

"""
python3 test-jdbc.py
Test PostgreSQL Database Connection
This script demonstrates how to connect to a PostgreSQL database using the psycopg2 library.
It includes examples of:
- Connecting to the database
- Fetching data from a table    
- Demonstrating transaction handling with commit and rollback
- Running more complex queries to demonstrate the marketplace functionality
- Using a connection pool for improved performance in web applications"""

import psycopg2
import sys
from psycopg2 import pool


def connect_to_db():
    """Connect to PostgreSQL database using connection parameters"""
    try:
        # Update these parameters with your actual database credentials
        connection_params = {
            'host': 'localhost',
            'port': '5432',
            'database': 'postgres',
            'user': 'yeedu',
            'password': 'yeedu'
        }
        
        print("Connecting to PostgreSQL database...")
        connection = psycopg2.connect(**connection_params)
        
        return connection
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        sys.exit(1)


# def create_connection_pool(min_conn=1, max_conn=5):
#     """Create a connection pool for improved performance in web applications"""
#     try:
#         # Update these parameters with your actual database credentials
#         connection_params = {
#             'host': 'localhost',
#             'port': '5432',
#             'database': 'bazario_db',
#             'user': 'postgres',
#             'password': 'postgres'
#         }
        
#         connection_pool = psycopg2.pool.SimpleConnectionPool(
#             min_conn, 
#             max_conn,
#             **connection_params
#         )
        
#         if connection_pool:
#             print("Connection pool created successfully!")
            
#         return connection_pool
#     except Exception as e:
#         print(f"Error creating connection pool: {e}")
#         sys.exit(1)


def fetch_users():
    """Fetch all users from the database"""
    connection = None
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Execute a simple query
        cursor.execute("SELECT id, name, email_id, role_id FROM USERS")
        
        # Fetch all rows
        users = cursor.fetchall()
        
        # Print column names
        column_names = [desc[0] for desc in cursor.description]
        print("\nUSERS TABLE:")
        print("-" * 80)
        print(f"{column_names[0]:<5} | {column_names[1]:<20} | {column_names[2]:<25} | {column_names[3]:<8}")
        print("-" * 80)
        
        # Print rows
        for user in users:
            print(f"{user[0]:<5} | {user[1]:<20} | {user[2]:<25} | {user[3]:<8}")
        
        cursor.close()
        
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        if connection:
            connection.close()
            print("\nDatabase connection closed.")


def demo_transactions():
    """Demonstrate transaction handling with commit and rollback"""
    connection = None
    try:
        connection = connect_to_db()
        connection.autocommit = False
        cursor = connection.cursor()
        
        print("\nDEMONSTRATING TRANSACTIONS:")
        print("-" * 80)
        
        # Begin a transaction
        print("Starting transaction...")
        
        # Insert a new role (this is just a demo - we'll roll back)
        cursor.execute(
            "INSERT INTO ROLES (role_name) VALUES (%s) RETURNING id;",
            ("Guest",)
        )
        
        role_id = cursor.fetchone()[0]
        print(f"Inserted new role with ID: {role_id}")
        
        # Insert a new user with the new role
        cursor.execute(
            """
            INSERT INTO USERS (name, email_id, phone_number, password, role_id) 
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
            """,
            ("Guest User", "guest@example.com", "1234567890", "guestpass", role_id)
        )
        
        user_id = cursor.fetchone()[0]
        print(f"Inserted new user with ID: {user_id}")
        
        # Demonstrate rollback
        print("Rolling back transaction (changes won't be saved)...")
        connection.rollback()
        
        # Verify the rollback worked
        cursor.execute("SELECT COUNT(*) FROM ROLES WHERE role_name = 'Guest';")
        count = cursor.fetchone()[0]
        print(f"Roles with name 'Guest' after rollback: {count}")
        
        cursor.close()
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error in transaction: {e}")
    finally:
        if connection:
            connection.close()
            print("Transaction demo completed.")


def query_marketplace_data():
    """Run more complex queries to demonstrate the marketplace functionality"""
    connection = None
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Query active seller listings with item details
        print("\nACTIVE SELLER LISTINGS:")
        print("-" * 100)
        cursor.execute("""
            SELECT 
                sr.id, 
                u.name as seller_name, 
                i.item_type, 
                sr.quantity, 
                i.unit,
                sr.price,
                sr.preferred_date,
                (SELECT COUNT(*) FROM SELLER_BUYER_LINEAGE_REQUESTS 
                 WHERE seller_request_id = sr.id) as bid_count
            FROM SELLERS_REQUESTS sr
            JOIN USERS u ON sr.seller_id = u.id
            JOIN ITEMS_STORE i ON sr.item_id = i.id
            WHERE sr.is_closed = FALSE
            ORDER BY sr.preferred_date;
        """)
        
        listings = cursor.fetchall()
        
        # Print column names
        column_names = [desc[0] for desc in cursor.description]
        print(f"{column_names[0]:<3} | {column_names[1]:<15} | {column_names[2]:<15} | "
              f"{column_names[3]:<8} | {column_names[4]:<4} | {column_names[5]:<8} | "
              f"{column_names[6]:<12} | {column_names[7]:<9}")
        print("-" * 100)
        
        # Print rows
        for listing in listings:
            print(f"{listing[0]:<3} | {listing[1]:<15} | {listing[2]:<15} | "
                  f"{listing[3]:<8} | {listing[4]:<4} | {listing[5]:<8} | "
                  f"{listing[6]} | {listing[7]:<9}")
        
        cursor.close()
        
    except Exception as e:
        print(f"Error executing marketplace query: {e}")
    finally:
        if connection:
            connection.close()
            print("\nMarketplace query completed.")


if __name__ == "__main__":
    print("=" * 80)
    print("BAZARIO DATABASE CONNECTION TEST")
    print("=" * 80)
    
    # Run demo functions
    fetch_users()
    demo_transactions()
    query_marketplace_data()
    
    print("\nAll tests completed.")
