from pymongo import MongoClient
import pprint
import csv

# MongoDB connection details
mongo_uri = "mongodb://localhost:27017/"  # Replace with your MongoDB URI if needed
database_name = "bxss-database"      # Replace with your database name
collection_name = "findings"  # Replace with your collection name
pp = pprint.PrettyPrinter(indent=2)

allSinksAndSources=["element.after","element.before","EventSource","Function.ctor","Range.createContextualFragment(fragment)","WebSocket","WebSocket.send","XMLHttpRequest.open(password)","XMLHttpRequest.open(url)","XMLHttpRequest.open(username)","XMLHttpRequest.send","XMLHttpRequest.setRequestHeader(name)","XMLHttpRequest.setRequestHeader(value)","a.href","area.href","document.cookie","document.writeln","document.write","element.style","embed.src","eval","eventHandler","fetch.body","fetch.url","form.action","iframe.src","iframe.srcdoc","img.src","img.srcset","innerHTML","insertAdjacentHTML","insertAdjacentText","localStorage.setItem","localStorage.setItem(key)","location.assign","location.hash","location.host","location.href","location.pathname","location.port","location.protocol","location.replace","location.search","media.src","MessagePort.PostMessage","navigator.sendBeacon(body)","navigator.sendBeacon(url)","object.data","outerHTML","script.innerHTML","script.src","script.text","script.textContent","sessionStorage.setItem","sessionStorage.setItem(key)","setInterval","setTimeout","source","srcset","track.src","window.open","window.postMessage","KeyboardEvent.charCode","KeyboardEvent.keyCode", "KeyboardEvent.key","KeyboardEvent.altKey","KeyboardEvent.ctrlKey","MouseEvent.screenX","MouseEvent.screenY","MouseEvent.pageX","MouseEvent.pageY","MouseEvent.clientX","MouseEvent.clientY","MouseEvent.x","MouseEvent.y","MouseEvent.offsetX","MouseEvent.offsetY","MouseEvent.ctrlKey","MouseEvent.shiftKey","MouseEvent.region","MouseEvent.movementX","MouseEvent.movementY", "Worker.PostMessage", "HTMLInputElemnet.setValue", "TextEncoder.encode", "BrowsingContext.PostMessage"]
data=[["scripts"]+allSinksAndSources]
# dataTMP=[["scripts", "is BB"]]

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
            scriptInfo={key:0 for key in allSinksAndSources}
            for value in values:
                for source in value["sources"]:
                    scriptInfo[source]+=1
                scriptInfo[value["sink"]]+=1
            # print(scriptInfo)
            data.append([0]*len(data[0]))
            for index in range(1,len(data[0])):
                data[-1][index]=scriptInfo[data[0][index]]
            data[-1][0]=script
            # dataTMP.append([script, 0])
        # print(data)

        with open("trainData.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        # with open("groundTruth.csv", mode='w', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerows(dataTMP)

        # script, number of flows, numberSources, numberSinks, isBB
        # Close the connection
        client.close()

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to read items
read_all_items()
