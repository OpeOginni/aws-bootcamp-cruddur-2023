import os
import sys

from flask import Flask
from flask import request, g
from flask_cors import cross_origin

from lib.rollbar import init_rollbar
from lib.xray import init_xray
from lib.honeycomb import init_honeycomb
from lib.cors import init_cors
from lib.cognito_jwt_token import jwt_required
from lib.cloudwatch import init_cloudwatch

from services.users_short import *
from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *
from services.update_profile import *

# MIDDLEWARE
from middleware.jwt_middleware import verify_jwt

# IMPORTANT PYTHON APP DECLARATION
app = Flask(__name__)

# initialization -------------
init_xray(app)
# with app.app_context():
#   init_rollbar()

init_honeycomb(app)
init_cors(app)

# Used to log errors to AWS CloudWatch
# @app.after_request
# def after_request(response):


def model_json(model):
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route('/api/health-check')
def health_check():
  return {'success': True, 'ver': 1}, 200

@app.route("/api/message_groups", methods=['GET'])
# Using my verify_jwt middleware
@verify_jwt("message_groups_endpoint")
# This middleware passes the claim in the req and it can be obtained using request.claims
@jwt_required()
def data_message_groups():

  if request.claims is not None: # If statement for my verify_juwt middleware
    model = MessageGroups.run(cognito_user_id=g.cognito_user_id)
    return model_json(model)
  else:
    app.logger.debug('unauthenticated')
    data = HomeActivities.run()
    return {}, 401

@app.route("/api/messages/<string:message_group_uuid>", methods=['GET'])
# Using my verify_jwt middleware
@verify_jwt("message_group_endpoint")
@jwt_required()
def data_messages(message_group_uuid):

  if request.claims is not None: # If statement for my verify_juwt middleware
    model = Messages.run(
      cognito_user_id=g.cognito_user_id,
      message_group_uuid=message_group_uuid
      )
    return model_json(model)
  else:
    app.logger.debug('unauthenticated')
    data = HomeActivities.run()
    return {}, 401

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
# Using my verify_jwt middleware
@verify_jwt("post_message_endpoint")
@jwt_required()
def data_create_message():
  message_group_uuid   = request.json.get('message_group_uuid',None)
  user_receiver_handle = request.json.get('handle',None)
  message = request.json['message']

  if request.claims is not None:
    if message_group_uuid == None:
      # Create for the first time
      app.logger.debug(message_group_uuid)
      app.logger.debug(user_receiver_handle)
      model = CreateMessage.run(
        mode="create",
        message=message,
        cognito_user_id=g.cognito_user_id,
        user_receiver_handle=user_receiver_handle
        )
    else:
      # Push onto existing Message Group
      model = CreateMessage.run(
        mode="update",
        message=message,
        message_group_uuid=message_group_uuid,
        cognito_user_id=g.cognito_user_id
        )
    return model_json(model)
  else:
    app.logger.debug('unauthenticated')
    data = HomeActivities.run()
    return {}, 401

def default_home_feed(e):
  # unathenticated request
  app.logger.debug(e)
  app.logger.debug("unauthenicated")
  data = HomeActivities.run()
  return data, 200

@app.route("/api/activities/home", methods=['GET'])
  # New Method
  # Middleware that checks the jwt and passes the info to a request param aclled claims
@verify_jwt("home_activities_endpoint")
@jwt_required(on_error=default_home_feed)
def data_home():
  data = HomeActivities.run(cognito_user_id=g.cognito_user_id)
  return data, 200


@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities.run()
  return data, 200

@app.route("/api/activities/@<string:handle>", methods=['GET'])
def data_handle(handle):
  model = UserActivities.run(handle)
  return return_model(model)

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  return model_json(model)

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():

  # This is a method I used to pass in the user handle to the create
  # activities endpoint worked for me
  user_handle  = request.json['user_handle']
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, user_handle, ttl)
  # model = CreateActivity.run(message, g.cognito_user_id, ttl)
  return model_json(model)

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  user_handle  = 'andrewbrown'
  message = request.json['message']
  model = CreateReply.run(message, user_handle, activity_uuid)
  return model_json(model)

@app.route("/api/users/@<string:handle>/short", methods=['GET'])
def data_users_short(handle):
  data = UsersShort.run(handle)
  return data, 200


@app.route("/api/profile/update", methods=['POST','OPTIONS'])
@cross_origin()

# Still making use of my Verify JWT Middleware
@verify_jwt("update_profile_endpoint")
@jwt_required()
def data_update_profile():
  bio          = request.json.get('bio',None)
  display_name = request.json.get('display_name',None)
  access_token = extract_access_token(request.headers)

  model = UpdateProfile.run(
    cognito_user_id=g.cognito_user_id,
    bio=bio,
    display_name=display_name
    )
  return model_json(model)

if __name__ == "__main__":
  app.run(debug=True)