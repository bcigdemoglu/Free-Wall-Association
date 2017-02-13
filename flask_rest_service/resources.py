"""
Summary
"""
from flask import request, abort, json, session, current_app
import flask_restful as restful
from flask_restful import reqparse
from . import api, hashpwd
from bson.objectid import ObjectId
from . import app
from datetime import datetime
import uuid
from pprint import pformat

class Root(restful.Resource):
    def get(self):
        session['uuid'] = uuid.uuid4()
        print(session['uuid'])
        return current_app.send_static_file('index.html')

# uuid.uuid4()), 200

class DB(restful.Resource):
    def get(self):
        return list(app.mongo.db.journey.find({}, {'_id': False, 'uuid': False})), 200

class Journey(restful.Resource):
    def post(self):
        uuid = session.get('uuid', None)
        print(uuid)
        word = request.form['word']
        app.mongo.db.journey.update({'uuid': uuid}, {'$push': {'journey': word.lower()}}, upsert=True)
        return {'word': word}, 200

    def get(self):
        uuid = session.get('uuid', None)
        print(uuid)
        user = app.mongo.db.journey.find_one({'uuid': uuid})
        if not user:
            return {'word': "wall"}
        else:
            return {'word': user['journey'][-1].lower()}

class AddWord(restful.Resource):
    def get(self, word):
        uuid = session.get('uuid', None)
        print(uuid)
        app.mongo.db.journey.update({'uuid': uuid}, {'$push': {'journey': word.lower()}}, upsert=True )
        return {'user': app.mongo.db.journey.find_one({'uuid': uuid}, {'_id': False})}

api.add_resource(Root, '/')
api.add_resource(DB, '/db')
api.add_resource(Journey, '/journey/')
api.add_resource(AddWord, '/journey/<word>')

# class Root(restful.Resource):
#     def get(self):
#         return {
#             'mongo': str(app.mongo.db),
#             'users': list(app.mongo.db.users.find({}, {'_id': False})),
#             'events': list(app.mongo.db.event.find({}, {'_id': False})),
#             'itinenaries': list(app.mongo.db.itin.find({}, {'_id': False})),
#             'rfctrainers': list(app.mongo.db.rfctrainers.find({}, {'_id': False})),
#             'rfcchoices': list(app.mongo.db.rfcchoices.find({}, {'_id': False})),
#             'userrating': list(app.mongo.db.yelp.find({}, {'_id': False}))
#         }, 200

# class Login(restful.Resource):
#     def post(self):
#         username  = request.get_json()['username']

#         user = app.mongo.db.users.find_one({"username": username})
#         if not user:
#             return {"error": "Invalid username"}, 400

#         password_form  = request.get_json()['password']
#         encrypted_pass = hashpwd(password_form)

#         if user["password"] != encrypted_pass:
#             return {"error": "Incorrect password"}, 401

#         # Success
#         session[username] = username
#         return user, 200

# class Register(restful.Resource):
#     def post(self):
#         user = {"username": request.get_json()['username'],
#                 "password": hashpwd(request.get_json()['password']),
#                 "name": request.get_json()['name'],
#                 "displayName": request.get_json().get('displayName') or request.get_json()['name']}

#         if app.mongo.db.users.find_one({"username": user["username"]}):
#             return {"error": "User already exists"}, 400

#         # Sucess
#         app.mongo.db.users.insert(user)
#         return user, 201

# class ChangePassword(restful.Resource):
#     def post(self, username):
#         user = app.mongo.db.users.find_one({"username": username})
#         if not user:
#             return {"error": "Invalid username"}, 400

#         if not hashpwd(request.get_json()['old_password']) == user["password"]:
#             return {"error": "Incorrect password"}, 400

#         user["password"] = hashpwd(request.get_json()['new_password'])

#         # Sucess
#         app.mongo.db.users.update({"username": username}, user)
#         return user, 200

# class ChangeDisplayName(restful.Resource):
#     def post(self, username):
#         user = app.mongo.db.users.find_one({"username": username})
#         if not user:
#             return {"error": "Invalid username"}, 400

#         if not hashpwd(request.get_json()['password']) == user["password"]:
#             return {"error": "Incorrect password"}, 400

#         user["displayName"] = request.get_json()['displayName']

#         # Sucess
#         app.mongo.db.users.update({"username": username}, user)
#         return user, 200

# class CreateItinerary(restful.Resource):
#     def post(self, username):
#         if not app.mongo.db.users.find_one({"username": username}):
#             return {"error": "Invalid username"}, 400

#         itinerary_name = request.get_json().get('name') or request.get_json()['date']

#         itinerary = {"createdBy": username,
#                      "name": itinerary_name,
#                      "date": request.get_json()['date'],
#                      "uid": ""}

#         # Generate itid
#         itinerary['uid'] = str(username + "_" + itinerary['date'])

#         if app.mongo.db.itin.find_one({"uid": itinerary['uid']}):
#             return {"error": "Itinerary date already in use"}, 400

#         # Sucess
#         app.mongo.db.itin.insert(itinerary)
#         return itinerary, 201

# class CreateEvent(restful.Resource):
#     def post(self, username):
#         if not app.mongo.db.users.find_one({"username": username}):
#             return {"error": "Invalid username"}, 400

#         if not request.get_json().get('uid'):
#             # If event does not exist, create it
#             event = {"start": request.get_json()['start'],
#                      "end": request.get_json()['end'],
#                      "date": request.get_json()['date'],
#                      "yelpId": "",
#                      "invited": [username],
#                      "acceptedBy": [],
#                      "uid": ""}
#             event['uid'] = str(username + "_" + event['start'] + event['end'])
#         else:
#             # If event already exists, retrieve it
#             event = app.mongo.db.event.find_one({'uid': request.get_json()['uid']})


#         if (event['start'] >= event['end']):
#             return {"error": "Invalid date range"}, 400

#         # Check for collision between other events
#         for e in app.mongo.db.event.find({'date': event['date'],
#                                           'acceptedBy': username }):
#             if self.checkCollision(event, e):
#                 return {"error": "Collision with another event"}, 400

#         if not app.mongo.db.itin.find_one({"createdBy": username,
#                                            "date": event['date']}):
#             return {"error": "Itinerary for the day not found"}, 400

#         # Verify the person is invited
#         if username in event['invited']:
#             # Now remove from invite and add to accepted
#             event['invited'].remove(username)
#             event['acceptedBy'].append(username)
#         else:
#             return {"error": "User is not invited"}, 400

#         # Sucess
#         if not request.get_json().get('uid'):
#             app.mongo.db.event.insert(event)
#         else:
#             app.mongo.db.event.update({'uid': event['uid']}, event)
#         return event, 201

#     @staticmethod
#     def checkCollision(event1, event2):
#         return (event1['start'] < event2['end']) and (event2['start'] < event1['end'])

# class InviteToEvent(restful.Resource):
#     '''
#         invited -> username of the invited person
#         uid -> event id
#     '''
#     def post(self, username):
#         if not app.mongo.db.users.find_one({"username": username}):
#             return {"error": "Invalid username"}, 400

#         event = findEvent(username)

#         if not event:
#             return {"error": "Event not found"}, 400

#         sharedUser = request.get_json()['invited']

#         if not app.mongo.db.users.find_one({"username": sharedUser}):
#             return {"error": "Shared user does not exist"}, 400

#         if sharedUser in event['invited']:
#             return {"error": "Already sent invitation"}, 400

#         if sharedUser in event['acceptedBy']:
#             return {"error": "Already shared with user"}, 400

#         event['invited'].append(sharedUser)
#         app.mongo.db.event.update({'uid': event['uid']}, event)
#         return event, 201

# class GetItineraryFromId(restful.Resource):
#     '''
#         uid -> Itinerary uid
#     '''
#     def get(self, username):
#         if not app.mongo.db.users.find_one({"username": username}):
#             return {"error": "Invalid username"}, 400

#         itinerary = app.mongo.db.itin.find_one({'uid': request.get_json()['uid'],
#                                                 'createdBy': username})

#         if not itinerary:
#             return {"error": "Itinerary not found"}, 400

#         return itinerary, 200

# class GetEventFromId(restful.Resource):
#     '''
#         uid -> event uid
#     '''
#     def get(self, username):
#         if not app.mongo.db.users.find_one({"username": username}):
#             return {"error": "Invalid username"}, 400


#         event = findEvent(username)

#         if not event:
#             return {"error": "Event not found"}, 400

#         return event, 200

# class DeleteEvent(restful.Resource):
#     '''
#         uid -> event uid
#     '''
#     def delete(self, username):
#         if not app.mongo.db.users.find_one({"username": username}):
#             return {"error": "Invalid username"}, 400

#         event = findEvent(username)

#         if not event:
#             return {"error": "Event not found"}, 400

#         app.mongo.db.event.delete_one({'uid': event['uid']})

#         return event, 200

# class UpdateEvent(restful.Resource):
#     '''
#         uid -> event uid
#     '''
#     def post(self, username):
#         if not app.mongo.db.users.find_one({"username": username}):
#             return {"error": "Invalid username"}, 400

#         event = findEvent(username)

#         if not event:
#             return {"error": "Event not found"}, 400

#         # Update the ML classifier
#         choice = request.get_json()['choice']
#         suggestionId = request.get_json()['suggestionId']

#         # Update event
#         event["yelpId"] = app.mongo.db.suggestions.find_one({'uid': suggestionId})['yelpId'][int(choice)]
#         app.mongo.db.event.update({'uid': event['uid']}, event)

#         classifier.updateModel(choice, suggestionId)
#         # Alex's code
#         app.mongo.db.unchosenSuggestions.delete_one({'uid': suggestionId})

#         everything = {
#             'business': app.mongo.db.suggestions.find_one({'uid': suggestionId})['biz'][int(choice)],
#             'event': event,
#             'uid': suggestionId
#             }

#         app.mongo.db.unratedSuggestions.insert({'username' : username,
#                                                      'date' : event['date'],
#                                                      'uid' : event["yelpId"],
#                                                      'business': everything['business']})


#         return event, 200

# class GetSuggestions(restful.Resource):
#     '''
#         uid -> event uid
#     '''
#     def get(self, username):
#         if not app.mongo.db.users.find_one({"username": username}):
#             return {"error": "Invalid username"}, 400

#         event = findEvent(username)
#         if not event:
#             return {"error": "Event not found"}, 400

#         date = event['date']

#         query = request.get_json()['query']

#         events = list(app.mongo.db.event.find({'date': date,
#                                                 'acceptedBy': username},
#                                               {'_id': False}))
#         [prev_event, next_event] = classifier.getPrevAndNextEvent(events, event)

#         bizList = yelp.getBusinessList(query, 10)
#         all_suggestions = []
#         for biz in bizList:
#             suggestion = classifier.getSuggestionArray(yelp,
#                                                        biz['id'],
#                                                        prev_event, next_event)
#             all_suggestions.append(suggestion)

#         suggested = classifier.pickSuggestions(bizList, all_suggestions)

#         top_biz = suggested['business']
#         top_ids = suggested['ids']
#         top_sugs = suggested['sugs']
#         top_probs = suggested['probs']

#         suggestionId = username + "_" + str(app.mongo.db.suggestions.count() + 1)
#         '''
#             Alex editted this below here
#         '''
#         app.mongo.db.unchosenSuggestions.insert({'username' : username,
#                                                      'date' : date,
#                                                      'uid' : suggestionId})

#         app.mongo.db.suggestions.insert({'uid': suggestionId,
#                                          'sugs': top_sugs,
#                                          'yelpId': top_ids,
#                                          'biz': top_biz})

#         return {'uid': suggestionId,
#                 'business': top_biz,
#                 'scores': top_probs}, 200
#     def post(self, username):
#         return self.get(username)


# class PostSuggestions(restful.Resource):
#     ''' This post(self, username) also done by Alex'''
#     def post(self, username):
#         if not app.mongo.db.users.find_one({"username": username}):
#             return {"error": "Invalid username"}, 400
#         event = findEvent(username)
#         if not event :
#             return {"error": "Event not found"}, 400

#         date = event['date']
#         choice = request.get_json().get('choice')
#         suggestionId = request.get_json().get('uid')
#         chosenSuggestion = app.mongo.db.unchosenSuggestions.remove({'username' : username,
#                                                                     'date' : date,
#                                                                     'uid' : suggestionId})


#         app.mongo.db.unratedSuggestions.insert(chosenSuggestion)
#         return {"message" : "Choice received."}, 200

# class DeleteItinerary(restful.Resource):
#     '''
#         uid -> itinerary uid
#     '''
#     def delete(self, username):
#         if not app.mongo.db.users.find_one({"username": username}):
#             return {"error": "Invalid username"}, 400

#         itinerary = app.mongo.db.itin.find_one({'uid': request.get_json()['uid'],
#                                                 'createdBy': username})

#         if not itinerary:
#             return {"error": "Itinerary not found"}, 400

#         app.mongo.db.itin.delete_one({'uid': request.get_json()['uid'],
#                                       'createdBy': username})

#         # Remove acceptance of events
#         events = app.mongo.db.event.find({'date': itinerary['date'],
#                                           'acceptedBy': username})
#         for e in events:
#             e['acceptedBy'].remove(username)
#             if e['acceptedBy'] == []:
#                 app.mongo.db.event.delete_one({'uid': e['uid']})
#             else:
#                 app.mongo.db.event.update({'uid': e['uid']}, e)

#         return itinerary, 200

# class GetEventsForItinerary(restful.Resource):
#     '''
#         date -> Itinerary date
#     '''
#     def get(self, username):
#         if not app.mongo.db.users.find_one({"username": username}):
#             return {"error": "Invalid username"}, 400

#         if not app.mongo.db.itin.find_one({"createdBy": username,
#                                            "date": request.get_json()['date']}):
#             return {"error": "Itinerary for the day not found"}, 400

#         events = app.mongo.db.event.find({'date': request.get_json()['date'],
#                                           'acceptedBy': username})

#         return {'events': events}, 200


# class GetItineraryList(restful.Resource):
#     def get(self, username):
#         if not app.mongo.db.users.find_one({"username": username}):
#             return {"error": "Invalid username"}, 400

#         itineraries = app.mongo.db.itin.find({"createdBy": username})

#         # Success
#         return {'itineraries': itineraries }, 200

# class SearchYelp(restful.Resource):
#     def get(self, query):
#         return {'yelpResponse': yelp.getBusinessList(query, 1)}, 201

# class RatePlace(restful.Resource):
#     def post(self, username):
#         rating = request.get_json().get('rating')
#         uid = request.get_json().get('uid')
#         ratings = []
#         stored_yelp = app.mongo.db.yelp.find_one({'uid': uid})
#         date = request.get_json().get('date')
#         app.mongo.db.unratedSuggestions.remove({'username' : username,
#                                                     'date' : date,
#                                                     'uid' : uid})
#         if stored_yelp:
#             ratings = stored_yelp['ratings']

#         ratings.append(rating)

#         yelp_rating = {'uid': uid,
#                        'ratings': ratings}

#         # Sucess
#         if stored_yelp:
#             app.mongo.db.yelp.update({'uid': uid}, yelp_rating)
#         else:
#             app.mongo.db.yelp.insert(yelp_rating)
#         return yelp_rating, 200
#         #Alex made this method
#     def get(self, username):
#         if not app.mongo.db.users.find_one({"username": username}):
#             return {"error": "Invalid username"}, 400

#         places = list(app.mongo.db.unratedSuggestions.find({'username' : username}))

#         '''
#         app.mongo.db.unratedSuggestions.insert({'username' : username,
#                                                      'date' : event['date'],
#                                                      'uid' : event["yelpId"]})
#         '''

#         if places == []:
#             return {"message" : "No places to Rate!"}, 201
#         return {'places' : places}, 200

# class PopulateDB(restful.Resource):
#     def post(self):
#         usernames = ["alex", "naina", "amy", "bugi"]
#         for username in usernames:
#             # Do not populate if user exists
#             if app.mongo.db.users.find_one({"username": username}):
#                 continue
#             app.mongo.db.users.insert({"username": username,
#                                        "password": hashpwd(username + "123"),
#                                        "name": username.title()})

#         return {'users': list(app.mongo.db.users.find())}, 201

#     def get(self):
#         return self.post()

# class PopulateItineraries(restful.Resource):
#     def post(self):
#         usernames = ["alex", "naina", "amy", "bugi"]
#         itineraryCounter = 1
#         for username in usernames:
#             for i in range(5):
#                 itineraryName = "itin"+ str(i + 1)
#                 itinuid = str(username + "_" + itineraryName)

#                 # Do not populate if itinerary exists
#                 if app.mongo.db.itin.find_one({"uid": itinuid}):
#                     continue
#                 app.mongo.db.itin.insert({"createdBy": username,
#                                           "name": itineraryName,
#                                           "uid": itinuid,
#                                           "date": "0"})

#         return {'itineraries': list(app.mongo.db.itin.find())}, 201

#     def get(self):
#         return self.post()

# def findEvent(username):
#     return app.mongo.db.event.find_one({'uid': request.get_json()['uid'],
#                                         'acceptedBy': username})

# api.add_resource(Login, '/login')
# api.add_resource(Register, '/register')
# api.add_resource(ChangePassword, '/changePassword/<username>')
# api.add_resource(ChangeDisplayName, '/changeDisplayName/<username>')
# api.add_resource(PopulateDB, '/testdb/populatedb')
# api.add_resource(PopulateItineraries, '/testdb/populateItineraries')
# api.add_resource(GetItineraryList, '/itinerarylistshells/<username>')
# api.add_resource(CreateItinerary, '/createItinerary/<username>')
# api.add_resource(CreateEvent, '/createEvent/<username>')
# api.add_resource(InviteToEvent, '/inviteToEvent/<username>')
# api.add_resource(GetEventsForItinerary, '/getEventsForItinerary/<username>')
# api.add_resource(GetEventFromId, '/getEventFromId/<username>')
# api.add_resource(UpdateEvent, '/updateEvent/<username>')
# api.add_resource(GetItineraryFromId, '/getItineraryFromId/<username>')
# api.add_resource(DeleteItinerary, '/deleteItinerary/<username>')
# api.add_resource(DeleteEvent, '/deleteEvent/<username>')
# api.add_resource(GetSuggestions, '/getSuggestions/<username>')
# api.add_resource(PostSuggestions, '/postSuggestions/<username>')
# api.add_resource(RatePlace, '/ratePlace/<username>')
# api.add_resource(SearchYelp, '/searchYelp/<query>')