from pymongo import MongoClient
import pprint
import csv

# MongoDB connection details
mongo_uri = "mongodb://localhost:27017/"  # Replace with your MongoDB URI if needed
database_name = "bxss-database"      # Replace with your database name
collection_name = "findings"  # Replace with your collection name
pp = pprint.PrettyPrinter(indent=2)

allFeatures=["number of taint reports","number of taints", "total taint flows","element.after","element.before","EventSource","Function.ctor","Range.createContextualFragment(fragment)","WebSocket","WebSocket.send","XMLHttpRequest.open(password)","XMLHttpRequest.open(url)","XMLHttpRequest.open(username)","XMLHttpRequest.send","XMLHttpRequest.setRequestHeader(name)","XMLHttpRequest.setRequestHeader(value)","a.href","area.href","document.cookie","document.writeln","document.write","element.style","embed.src","eval","eventHandler","fetch.body","fetch.url","form.action","iframe.src","iframe.srcdoc","img.src","img.srcset","innerHTML","insertAdjacentHTML","insertAdjacentText","localStorage.setItem","localStorage.setItem(key)","location.assign","location.hash","location.host","location.href","location.pathname","location.port","location.protocol","location.replace","location.search","media.src","MessagePort.PostMessage","navigator.sendBeacon(body)","navigator.sendBeacon(url)","object.data","outerHTML","script.innerHTML","script.src","script.text","script.textContent","sessionStorage.setItem","sessionStorage.setItem(key)","setInterval","setTimeout","source","srcset","track.src","window.open","window.postMessage","KeyboardEvent.charCode","KeyboardEvent.keyCode", "KeyboardEvent.key","KeyboardEvent.altKey","KeyboardEvent.ctrlKey","MouseEvent.screenX","MouseEvent.screenY","MouseEvent.pageX","MouseEvent.pageY","MouseEvent.clientX","MouseEvent.clientY","MouseEvent.x","MouseEvent.y","MouseEvent.offsetX","MouseEvent.offsetY","MouseEvent.ctrlKey","MouseEvent.shiftKey","MouseEvent.region","MouseEvent.movementX","MouseEvent.movementY", "MouseEvent.movementX","MouseEvent.movementY","KeyboardEvent.shiftKey","KeyboardEvent.metaKey","KeyboardEvent.location","KeyboardEvent.repeat","KeyboardEvent.isComposing","MouseEvent.altKey","MouseEvent.metaKey","MouseEvent.button","MouseScrollEvent.axis","PointerEvent.pointerId","PointerEvent.width","PointerEvent.height","PointerEvent.pressure","PointerEvent.tangentialPressure","PointerEvent.tiltX","PointerEvent.tiltY","PointerEvent.twist","PointerEvent.isPrimary","Touch.identifier","Touch.screenX","Touch.screenY","Touch.clientX","Touch.clientY","Touch.pageX","Touch.pageY","Touch.radiusX","Touch.radiusY","Touch.rotationAngle","Touch.force","TouchEvent.altKey","TouchEvent.metaKey","TouchEvent.ctrlKey","TouchEvent.shiftKey", "Worker.PostMessage", "HTMLInputElemnet.setValue", "TextEncoder.encode", "BrowsingContext.PostMessage", "TypedArray.setElem", "TypedArray.setFromArray", "element.append"]
data=[["domain","scripts"]+allFeatures]

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
        i=0
        for document in documents:
            if i%100==0:
                print(i)
            i+=1
            domain=document["domain"]
            allScripts=set()
            allScripts.add((domain,document["script"]))
            for taint in document["taint"]:
                for flow in taint["flow"]:
                    if flow["location"]["filename"] != "":
                        allScripts.add((domain,flow["location"]["filename"]))
            for script in allScripts:
                if script in scripts:
                    scripts[script].append(document)
                else:
                    scripts[script]=[document]

        print("done")
        for script,values in scripts.items():
            numberOfReports=len(values)
            numberOfTaints=0
            numberOfFlows=0
            scriptInfo={key:0 for key in allFeatures}
            for value in values:
                for source in value["sources"]:
                    scriptInfo[source]+=1
                scriptInfo[value["sink"]]+=1
                numberOfTaints+=len(value["taint"])
                for flow in value["taint"]:
                    numberOfFlows+=len(flow)

            scriptInfo["number of taint reports"]=numberOfReports
            scriptInfo["number of taints"]=numberOfTaints
            scriptInfo["total taint flows"]=numberOfFlows
            data.append([0]*len(data[0]))
            for index in range(2,len(data[0])):
                data[-1][index]=scriptInfo[data[0][index]]
            data[-1][1]=script[1]
            data[-1][0]=script[0]

        with open("trainData.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        # Close the connection
        client.close()

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to read items
read_all_items()
