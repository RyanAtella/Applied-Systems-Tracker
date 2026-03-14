from database import engine

try:
    # Try to connect
    connection = engine.connect()
    print("✅ Database connection successful!")
    connection.close()
except Exception as e:
    print("❌ Database connection failed!")
    print(e)