from pymongo import MongoClient
import pprint
import csv

# MongoDB connection details
mongo_uri = "mongodb://localhost:27017/"  # Replace with your MongoDB URI if needed
database_name = "bxss-database"      # Replace with your database name
collection_name = "findings"  # Replace with your collection name
pp = pprint.PrettyPrinter(indent=2)

dataTMP=[["Website", "Scripts"]]

def websiteToScriptMap():
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)

        # Access the database and collection
        db = client[database_name]
        collection = db[collection_name]

        # Read all documents from the collection
        documents = collection.find()

        # Print each document
        siteToScript={}
        scriptToSite={}
        for document in documents:
            # pp.pprint(document)
            if document["base_url"] not in siteToScript:
                siteToScript[document["base_url"]]=set()
            siteToScript[document["base_url"]].add(document["script"])

            if document["script"] not in scriptToSite:
                scriptToSite[document["script"]]=set()
            scriptToSite[document["script"]].add(document["base_url"])


            for taint in document["taint"]:
                for flow in taint["flow"]:
                    if flow["location"]["filename"] != "":
                        siteToScript[document["base_url"]].add(flow["location"]["filename"])

                        if flow["location"]["filename"] not in scriptToSite:
                            scriptToSite[flow["location"]["filename"]]=set()
                        scriptToSite[flow["location"]["filename"]].add(document["base_url"])

        # for website,values in siteToScript.items():
        #     dataTMP.append([website, "   ".join(list(values))])
        # pp.pprint(siteToScript)
        for k,v in scriptToSite.items():
            if len(v)>1:
                print(k, v)

        # with open("groundTruth.csv", mode='w', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerows(dataTMP)

        # Close the connection
        client.close()

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to read items
websiteToScriptMap()
