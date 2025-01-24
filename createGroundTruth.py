from pymongo import MongoClient
import pprint
import csv

# MongoDB connection details
mongo_uri = "mongodb://localhost:27017/"  # Replace with your MongoDB URI if needed
database_name = "bxss-database"      # Replace with your database name
collection_name = "findings"  # Replace with your collection name
pp = pprint.PrettyPrinter(indent=2)

dataTMP=[["scripts", "is BB"]]

def createGroundTruth():
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
            allScripts=set()
            for taint in document["taint"]:
                for flow in taint["flow"]:
                    if flow["location"]["filename"] != "":
                        allScripts.add(flow["location"]["filename"])
            for script in allScripts:
                if script in scripts:
                    scripts[script].append(document)
                else:
                    scripts[script]=[document]

            # if document["script"] in scripts:
            #     scripts[document["script"]].append(document)
            # else:
            #     scripts[document["script"]]=[document]
        for script,values in scripts.items():
            dataTMP.append([script, 0])

        # with open("groundTruth.csv", mode='w', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerows(dataTMP)

        # Close the connection
        client.close()

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to read items
createGroundTruth()
