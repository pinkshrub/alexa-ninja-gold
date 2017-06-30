# Application to play ninja Gold
import random
# Somethings to have avaialabled
VERSION = 1.0
states = {
    "INGAME": 'playing',
    "INLOBBY": 'waiting'
}

past_tenses = {
    "mine": "mined",
    "farm": "farmed",
    "collect wood": "Collected Wood",
    "fight a dragon": "Fought a Dragon"
}



# this method is the generic handler of a 'request', it contains an event and context
# the event contains information about what was directly said in the request and teh context has other user information
def request_handler(event, context):
    # What an event looks like:

            #     {
            #   "session": {
            #     "sessionId": "SessionId.7f458bac-8fba-464c-ab0d-ca88256b36fb",
            #     "application": {
            #       "applicationId": "amzn1.ask.skill.43fcf8a4-0eaf-413a-bd9f-1579dd3ffb76"
            #     },
            #     "attributes": {},
            #     "user": {
            #       "userId": "amzn1.ask.account.AHJBX3Z3DXMBSPRXJLGBUSSZMDDNC5VSV6B7DTRUYOHLR3CHIEJ3D4M3G6RMQZHIPJLGL7CEMDPYCLAOC35W6JVG36ODAA7LAVZEBBFEHLMVDV4UZAV4NI5D65LB2RU3RZ2BYIZS7KLVPBDGH2TFKB7ZCAPOITFQELZY262RJLJDTENZHCAT2CZLNYJ6GMHEKSRPXWSAHRRFVIY"
            #     },
            #     "new": true
            #   },
            #   "request": {
            #     "type": "IntentRequest",
            #     "requestId": "EdwRequestId.2fcdbb5b-9990-47d4-9851-3917cbb4c4b3",
            #     "locale": "en-US",
            #     "timestamp": "2017-06-29T21:18:51Z",
            #     "intent": {
            #       "name": "DojoStaffIntent",
            #       "slots": {}
            #     }
            #   },
            #   "version": "1.0"
            # }

    # The following lines to prevent other skills sending requests to this function
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    # Need to handle different intent types at this point, "routing"
    # starting
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    # ninjagolding
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    # ending
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

# this method will handle launchage
def on_launch(request, session):
    # build welcome response and set up session attributes
    session["attributes"]["state"] = states["INLOBBY"]
    return start_new_game(request, session)

# this method will handle the end ofthe session
def on_session_ended(request, session):
    # lets us know we donezo
    print ("The Ninjas are done Golding!")


# this handles not starting/stopping events
def on_intent(request, session):
    # this will be our routing center

    # figure out what the request wants to do!
    intent_name = request['intent']['name']
    if intent_name == "ActionIntent":
        # This will need to handle the different actions we can do
        return handle_action_intent(request, session)
    elif intent_name == "StartIntent":
        # this will start a game anew
        return start_new_game(request, session)
    elif intent_name == "AMAZON.HelpIntent":
        # needs to provide helpful infomrations
        return give_help(request, session)
    elif intent_name == "AMAZON.StopIntent":
        # stops the thing
        return stop_everything(request, session)
    else:
        # for boops
        raise ValueError("Invalid Intent")

def stop_everything(request, session):
    # sop handler
    title = "Ending Session"
    output = "Thank you for playing and earning {} Gold".format(session['attributes']['gold'])
    reprompt = None
    endsession = true
    new_response = build_response(title, output, reprompt, endsession)
    return build_full_response(new_response)

def give_help(request, session):
    lobby_help = "Ninja Gold is a game that lets you perform one of four activities to earn gold over time. You may mine, farm, collect wood, or fight a dragon. Dragons are mean."
    game_help = "The actions you can take are mine, collect wood, farm, and fight a dragon. Tell Alexa what you'd like to do to earn gold."
    state = session['attributes']['state']
    title = "Help!"
    output = game_help if state == states["INGAME"] else lobby_help
    reprompt = output
    endsession = False
    new_response = build_response(title, output, reprompt, endsession)
    ses_attrs = session['attributes']
    return build_full_response(new_response, ses_attrs)

def start_new_game(request, session):
    # to start a new game we need to reset total gold and change session state
    session["attributes"]["gold"] = 0
    session["attributes"]["state"] = states["INGAME"]
    title = "Started NINJA GOLD"
    output = "You are a broke ninja, what would you like to do?"
    reprompt = "Your can mine, collect wood, farm, or fight a dragon"
    endsession=False
    new_response = build_response(title, output, reprompt, endsession)
    return build_full_response(new_response, session["attributes"])

def process_action(action_type):
    golds = 0
    if action_type == "mine":
        golds = random.randint(-10,50)
    elif action_type == "farm":
        golds = random.randint(10, 30)
    elif action_type == "fight a dragon":
        golds = random.randint(150, 300) if random.randint(1,100) > 95 else random.randint(-300, -150)
    elif action_type == "collect wood":
        golds = random.randint(15, 25)
    else:
        golds = 0
    return golds

def handle_action_intent(request, session):
    # grab activity
    action_type = request["intent"]["slots"]["Action"]["value"].lower()
    # update total gold
    new_gold = process_action(action_type)
    session["attributes"]["gold"]+=new_gold
    title = "Went to Work!"
    output = "You went and {} which earned you {} gold pieces. You now have {} gold pieces, what would you like to do next?".format(past_tenses[action_type], new_gold, session["attributes"]["gold"])
    reprompt = "What would you like to do?"
    endsession = False
    new_response = build_response(title, output, reprompt, endsession)
    return build_full_response(new_response, session["attributes"])

def build_response(title, output, reprompt, endsession=True):
    # response needs to contain th einformation for:
    # title, output, reprompt, endsession
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt" : {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt
            }
        },
        "shouldEndSession": endsession
    }

def build_full_response(response, sessionAttributes={}):
    # response has a lot of components:
    # response keys are version, response, sessionattributes,
    # response is assembled in another function and session attributes are passed in
    # version should be provided, via global variable

            #     {
            #   "version": "1.0",
            #   "response": {
            #     "outputSpeech": {
            #       "type": "PlainText",
            #       "text": "The Coding Dojo has a number of instructors at different locations. Our current locations are San Jose, Seattle, Burbank, Dallas, Washington DC, and Chicago. If you want information about a particular location you can ask the Coding Dojo skill. So for example you can ask... who are the instructors at the Chicago location."
            #     },
            #     "card": {
            #       "content": "SessionSpeechlet - The Coding Dojo has a number of instructors at different locations. Our current locations are San Jose, Seattle, Burbank, Dallas, Washington DC, and Chicago. If you want information about a particular location you can ask the Coding Dojo skill. So for example you can ask... who are the instructors at the Chicago location.",
            #       "title": "SessionSpeechlet - Dojo_Staff",
            #       "type": "Simple"
            #     },
            #     "reprompt": {
            #       "outputSpeech": {
            #         "type": "PlainText",
            #         "text": "The Coding Dojo has a number of instructors at different locations. Our current locations are San Jose, Seattle, Burbank, Dallas, Washington DC, and Chicago. If you want information about a particular location you can ask the Coding Dojo skill. So for example you can ask... who are the instructors at the Chicago location."
            #       }
            #     },
            #     "speechletResponse": {
            #       "outputSpeech": {
            #         "text": "The Coding Dojo has a number of instructors at different locations. Our current locations are San Jose, Seattle, Burbank, Dallas, Washington DC, and Chicago. If you want information about a particular location you can ask the Coding Dojo skill. So for example you can ask... who are the instructors at the Chicago location."
            #       },
            #       "card": {
            #         "title": "SessionSpeechlet - Dojo_Staff",
            #         "content": "SessionSpeechlet - The Coding Dojo has a number of instructors at different locations. Our current locations are San Jose, Seattle, Burbank, Dallas, Washington DC, and Chicago. If you want information about a particular location you can ask the Coding Dojo skill. So for example you can ask... who are the instructors at the Chicago location."
            #       },
            #       "reprompt": {
            #         "outputSpeech": {
            #           "text": "The Coding Dojo has a number of instructors at different locations. Our current locations are San Jose, Seattle, Burbank, Dallas, Washington DC, and Chicago. If you want information about a particular location you can ask the Coding Dojo skill. So for example you can ask... who are the instructors at the Chicago location."
            #         }
            #       },
            #       "shouldEndSession": true
            #     }
            #   },
            #   "sessionAttributes": {}
            # }

    return {
        "version": VERSION,
        "sessionAttributes": sessionAttributes,
        "response": response
    }
