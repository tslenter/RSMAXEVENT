#import required modules
import requests
import json

#set elastic variables
output=''
username='MY_USER'
password='MY_PASSWORD'
backtime='now-1h/h'
index='rse*'
searchword='Disjoined'
headers={'Accept': 'application/json', 'Content-type': 'application/json'}
data_url = 'http://localhost:9200/'+index+'/_search'
json_data = { "query" : { "bool" : { "must": [ { "match": { "MESSAGE": searchword } }, { "range": { "@timestamp": { "gte": backtime } } } ] } } , "size": 10000 }
#Can be used to validate the count (debug)
#json_count = { "size": 0, "query": { "bool" : { "must": [ { "match": { "MESSAGE": searchword } }, { "range": { "@timestamp": { "gte": backtime } } } ] } } }

#Process data
query = json.dumps(json_data)
data_response = requests.get(data_url, data = query, auth=(username,password), verify=False, headers = headers)
#Check valid request
if data_response.status_code == 200:
#   Could be used to print the json response pretty (Debug)
#    print(json.dumps(response.json(), indent=4, sort_keys=True))
    json_data_processed = json.loads(json.dumps(data_response.json()))
    count = len(json_data_processed['hits']['hits'])
    #Loop count with data and add a new line
    for i in range(count):
        output += str(json_data_processed['hits']['hits'][i]['_source']['MESSAGE'])+"<br/>"+"\n"
    #check if the output is null
    if output == "":
        print("Nothing to do ...")
        exit()
else:
    print("Nothing to do ...")
    exit()

#Show requested output
print(output)

#set maximo variables
max_username = 'MAXIMO_USER'
max_password = 'MAXIMO_PASSWORD'
maximo_url = 'http://controldesk.ORGANISATION.LOCAL/maxrest/oslc/os/mxapiincident?lean=1'
maximo_headers={'Accept': 'application/json', 'Content-type': 'application/json'}
maximo_data = {
"assetsiteid":"ORGANIMSATION",
"assetnum":"000AVXFX",
"_comment1":"asset and locatie (location) are optional, when a asset and location is given the the siteid is needed",
"description":"Network issue detected!",
"description_longdescription": output,
"internalpriority":3,
"ownergroup":"NETWERK SOC",
"reportedby":"MAXIMO_USER",
"_comment2":"reportedby is optioneel",
"classstructureid":"1111",
"_comment3":"get internal value for classification: classstructureid from Maximo",
"externalrecid":"1234",
"_comment4":"optioneel, record id externe system, lengte 20"
}

maximo_query = json.dumps(maximo_data)
maximo_post = requests.post(maximo_url, data = maximo_query, verify=False, headers = maximo_headers, auth=(max_username, max_password))

print(maximo_post)
