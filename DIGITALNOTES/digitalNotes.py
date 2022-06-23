from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json
import uuid
import time
from bson import json_util

# Connect to MongoDB
client = MongoClient(host='mongodb',port=27017)   
db = client['DigitalNotes']
# collections
users = db['users']
notes = db['notes']

# Flask App
app = Flask(__name__)

users_sessions = {}
admin_sessions={}
authusername={}
# function for creating uid
def create_session(username):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (username)
    return user_uuid  

# function for checking if uid is valid
def is_session_valid(user_uuid):
    return user_uuid in users_sessions
def is_admin_session_valid(user_uuid):
    return user_uuid in admin_sessions





@app.route('/createmongo', methods=['POST'])
def cremon():
    client=MongoClient('mongodb://localhost:27017/') # Connect to MongoDB
    db = client['DigitalNotes'] # Create database
    users = db['Users'] # Create collections
    notes = db['notes'] 
    return Response("created!");


# create simple user
@app.route('/createSimpleUser', methods=['POST'])
def create_simple_user():
    data = None 
    
    try:
        data = json.loads(request.data)
        print(data)
    except Exception as e:
        print("HJ")
        print(data)
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "name" in data or not "e-mail" in data or not "password" or not "username" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    # if user not in database already
    if users.count_documents({"username":data["username"]}) == 0 :
    # update category for simple user
        category = {'category':'simple user'}
        data.update(category)
        
        users.insert_one(data) # add user
        return Response("User "+data['name']+" was added.\n", mimetype='application/json', status=200) 
    else: # if user already in database 
        return Response("A user with the given username already exists\n", mimetype='application/json', status=400) 

# login
@app.route('/login', methods=['POST'])
def login():
    print("LOF")
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content !",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    # if email or password is not given
    if not "username" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    # if email, password found in database
    if users.find_one({"username":data["username"], "password":data["password"]}):
    # call function create session, return uuid
    
        user_uuid = create_session(data["username"])
        passy=users.find_one({"username":data["username"], "password":data["password"]})
        print(passy)
        print(passy) 
        
        if (passy['password']=='admnew'):
            if not "newpassword" in data:
            
                return Response("You are a new assigned admin, should give newwpassword")                     
            else:
                users.update_one({'username':data['username']},{'$set': {'password':data['newpassword']}})

        if users.find_one({"username":data["username"], "password":data["password"],"category":'admin'}):
            admin_sessions[user_uuid]=data['username']
        return Response('Userid for user ' + data['username']+ ' : '+ user_uuid+"\n", mimetype='application/json',status=200) 
    else:
        return Response("Wrong email or password.\n",mimetype='application/json', status=400) 

@app.route('/createNote', methods=['POST'])
def add_Note():
    from datetime import date

    today = date.today()
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        print(data)
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    print(data)
    if not "title" in data or not "text" in data or not "words" in data:
        return Response("Title,text,words must be inserted.\n")
  
    uuid = request.headers.get('Authorization')
    # Check if uuid is valid
    verify = is_session_valid(uuid)
    if verify:
        d1 = today.strftime("%d/%m/%Y")
        
        data['date']=d1
        data['username']=users_sessions[uuid]
        notes.insert_one(data) 
        return Response('NOTE '+data['title']+' was added to database.\n', mimetype='application/json', status=200) 
    else:
        return Response('Not verified', mimetype='application/json', status=200)
  

@app.route('/deleteNote', methods=['POST'])
def delete_Note():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    # if no id given
    if not "title" in data:
        return Response("No note specified by title!\n",status=500,mimetype="application/json")
    
    
    uuid = request.headers.get('Authorization')
    # Check if uuid is valid
    verify = is_session_valid(uuid)
    if verify:
    
        print(users_sessions[uuid])
        note = notes.find_one({'title':data["title"],'username':users_sessions[uuid]})
        if note != None:
            notes.delete_one(note)
            return Response ("Note with title "+note["title"] + " was deleted.\n", status=200, mimetype='application/json')
        else:
            return Response("No note found with title " + data["title"]+"\n")
    else:
        return Response('Not verified', mimetype='application/json', status=200)
 

@app.route('/deleteUser', methods=['POST'])
def delete_User():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    # if no id given
   
    
    
    uuid = request.headers.get('Authorization')
    # Check if uuid is valid
    verify = is_session_valid(uuid)
    if verify:
    
        print(users_sessions[uuid])
        user = users.find_one({'username':users_sessions[uuid]})
        if user != None:
            users.delete_one(user)
            return Response ("User with username "+users_sessions[uuid]+ " was deleted.\n", status=200, mimetype='application/json')
        else: 
            return Response("No user found with username" + users_sessions[uuid]+"\n")
    else:
        return Response('Not verified', mimetype='application/json', status=200)
@app.route('/deleteUserAdm', methods=['POST'])
def delete_UserAdm():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    # if no id given
   
    
    
    uuid = request.headers.get('Authorization')
    # Check if uuid is valid
    verify = is_session_valid(uuid)
    if verify:
        ver2=is_admin_session_valid(uuid)
        if ver2:
            print("HELLO ADMIN");
            if "username" in data:
                user = users.find_one({'username':data['username']})
               
                if user != None:
                    users.delete_one(user)
                    return Response ("User with username "+data['username']+ " was deleted.\n", status=200, mimetype='application/json')
                else: 
                    return Response("No user found with username" +data['username']+"\n")
            else:
                return Response("NOT GIVEN username to Delete\n")
        else:
            return  Response("YOU ARE NOT ADMIN! \n")
    else:
        return Response('Not verified', mimetype='application/json', status=200)
        

@app.route('/assignUserAdm', methods=['POST'])
def assign_UserAdm():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    # if no id given
   
    
    
    uuid = request.headers.get('Authorization')
    # Check if uuid is valid
    verify = is_session_valid(uuid)
    if verify:
        ver2=is_admin_session_valid(uuid)
        if ver2:
            print("HELLO ADMIN!");
            if "username" in data:
                user = users.find_one({'username':data['username']})
                if user != None:
                   
                    users.update_one({'username':data['username']},{'$set': {'category':'admin','password':'admnew'}})

                    
                    return Response ("User with username "+data['username']+ " was assign admin.\n", status=200, mimetype='application/json')
                else: 
                    return Response("No user found with username" +data['username']+"\n")
            else:
                return Response("NOT GIVEN username to ASSIGN ADM\n")
        else:
            return  Response("YOU ARE NOT ADMIN! \n")
    else:
        return Response('Not verified', mimetype='application/json', status=200)
@app.route('/searchNote', methods=['POST'])
def search_Note():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "title" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    # Get uuid from header type authorization
    uuid = request.headers.get('Authorization')
    # Check if uuid is valid
    verify = is_session_valid(uuid)
    if verify:
        if "title" in data:
            notesList = notes.find({'title':data["title"],'username':users_sessions[uuid]})
            notesArray=[]
            for note in notesList:
                print(note)
                note = {'title': note["title"], 'text': note["text"], 'words': note["words"]}
                notesArray.append(note)
            if  notesArray!= []:
                return Response(json.dumps(notesArray,indent=4)+"\n", status=200, mimetype='application/json')
            else:
                return Response("Not found any !\n")
        else:       
            return Response("Not providing a title .\n")
    else: # If uuid was not valid
        return Response("User can't be verified.\n", status=401)

@app.route('/searchWord', methods=['POST'])
def search_Word():
    import re

    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "words" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    # Get uuid from header type authorization
    uuid = request.headers.get('Authorization')
    # Check if uuid is valid
    verify = is_session_valid(uuid)
    if verify:
        if "words" in data:
            arg='/'+data['words']+'/'
            
            pat = re.compile('.*(%s).*' %data['words'])

            print(arg)
            notesList = notes.find({'words': {'$regex': pat}})
            notesArray=[]
            for note in notesList:
                print(note)
                note = {'title': note["title"], 'text': note["text"], 'words': note["words"]}
                notesArray.append(note)
            if  notesArray!= []:
                return Response(json.dumps(notesArray,indent=4)+"\n", status=200, mimetype='application/json')
            else:
                return Response("Not found any !\n")
                
        else:       
            return Response("Not providing a word .\n")
    else: # If uuid was not valid
        return Response("User can't be verified.\n", status=401)
    
    
    
@app.route('/showOrder', methods=['POST'])
def show_Order():
    import re

    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "rank" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    # Get uuid from header type authorization
    uuid = request.headers.get('Authorization')
    # Check if uuid is valid
    verify = is_session_valid(uuid)
    if verify:
        if "rank" in data:
            
            print(data['rank'])
            inta=int(data['rank'])
           
            notesList = notes.find({}).sort('date',inta)
            notesArray=[]
            # store data in dictionary
            for note in notesList:
                print(note)
                note = {'date':note['date'],'title': note["title"], 'text': note["text"], 'words': note["words"]}
                notesArray.append(note)
            if  notesArray!= []:
                return Response(json.dumps(notesArray,indent=4)+"\n", status=200, mimetype='application/json')
            else:
                return Response("Not found any !\n")
                
        else:       
            return Response("Not providing rank 1 or -1.\n")
    else: # If uuid was not valid
        return Response("User can't be verified.\n", status=401)   
    
  
    

@app.route('/updateNote', methods=['POST'])
def update_Νote():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    # check if no data missing
    if not "title" in data:
        return Response("Not given title",status=500,mimetype="application/json")
  
    if not ("titlenew" in data or "words" in data or "text" in data):
        return Response("Give at least one of (titlenew,words,text) \n",status=500,mimetype="application/json")
    # Get uuid from header type authorization
    uuid = request.headers.get('Authorization')
    # Check if uuid is valid
    verify = is_session_valid(uuid)
    if verify:
        note= notes.find_one({'title':data["title"]})
        if note != None:
            if 'titlenew' in data:
                tn=data['titlenew']
            else:
                tn=note['title']
            if 'words' in data:
                wd=data['words']
            else:
                wd=note['text']
            if 'text' in data:
                tx=data['text']
            else:
                tx=note['text'] 
                
            notes.update_one({'title':data["title"]},{'$set': {'title':tn,'words':wd,'text':tx}})
            return Response('UPDATED '+data['title']+" \n")

           
            print("h")
    
        else: #=
            return Response("No note find found with title '"+data["title"]+"'.\n")
    else: # If uuid was not valid
        return Response("User can't be verified.\n", status=401)






# Εκτέλεση flask service σε debug mode, στην port 5000. 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)[0]