from pymongo import MongoClient

# MongoDB connection details
mongo_uri = "mongodb://localhost:27017/"  # Replace with your MongoDB URI if needed
database_name = "bxss-database"      # Replace with your database name
collection_name = "findings"  # Replace with your collection name

def delete_collection():
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)

        # Access the database
        db = client[database_name]

        # Delete the collection
        db.drop_collection(collection_name)
        print(f"The collection '{collection_name}' has been deleted.")

        # Close the connection
        client.close()

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to delete the collection
delete_collection()
