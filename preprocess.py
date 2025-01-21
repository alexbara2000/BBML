from pymongo import MongoClient
import pprint

# MongoDB connection details
mongo_uri = "mongodb://localhost:27017/"  # Replace with your MongoDB URI if needed
database_name = "bxss-database"      # Replace with your database name
collection_name = "findings"  # Replace with your collection name
pp = pprint.PrettyPrinter(indent=2)

def read_all_items():
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)

        # Access the database and collection
        db = client[database_name]
        collection = db[collection_name]

        # Read all documents from the collection
        documents = collection.find()

        # Print each document
        scripts={}
        for document in documents:
            # pp.pprint(document)
            if document["script"] in scripts:
                scripts[document["script"]].append(document)
            else:
                scripts[document["script"]]=[document]
        for script,values in scripts.items():
            numberFlows=len(values)
            sources=set()
            sinks=set()
            for value in values:
                for source in value["sources"]:
                    sources.add(source)
                sinks.add(value["sink"])
            print(script, numberFlows, len(sources), len(sinks))


        # script, number of flows, numberSources, numberSinks, isBB
        # Close the connection
        client.close()

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to read items
read_all_items()
