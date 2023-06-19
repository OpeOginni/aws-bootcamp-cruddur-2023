from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os
import sys

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

from lib.cognito_jwt_token import CognitoJwtToken, extract_access_token, TokenVerifyError

# HoneyComb --------
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# X-RAY --------
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# CLOUDWATCH LOGS --------
import watchtower
import logging
from time import strftime

# MIDDLEWARE
from middleware.jwt_middleware import verify_jwt

# Configuring Logger to Use CloudWatch
# LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)
# console_handler = logging.StreamHandler()
# cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
# LOGGER.addHandler(console_handler)
# LOGGER.addHandler(cw_handler)
# LOGGER.info("Test Log")

# HoneyComb --------
# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)

# X-RAY --------
# xray_url = os.getenv("AWS_XRAY_URL")
# xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)


# Shows the logs within the backend-flask app
# simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
# provider.add_span_processor(simple_processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# IMPORTANT PYTHON APP DECLARATION
app = Flask(__name__)

cognito_jwt_token = CognitoJwtToken(
  user_pool_id= os.getenv('AWS_COGNITO_USER_POOL_ID'),
  user_pool_client_id= os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID"),
  region= os.getenv("AWS_DEFAULT_REGION")
  )

# X-RAY --------
# XRayMiddleware(app, xray_recorder)

# HoneyComb --------
# Initialize automatic instrumentation with Flask
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
origins = [frontend, backend]
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  headers=['Content-Type', 'Authorization'], 
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
)

# Used to log errors to AWS CloudWatch
# @app.after_request
# def after_request(response):
#     timestamp = strftime('[%Y-%b-%d %H:%M]')
#     LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
#     return response

@app.route('/api/health-check')
def health_check():
  return {'success': True, 'ver': 1}, 200

@app.route("/api/message_groups", methods=['GET'])
# Using my verify_jwt middleware
@verify_jwt("message_groups_endpoint")
# This middleware passes the claim in the req and it can be obtained using request.claims

def data_message_groups():

  if request.claims is not None:
    try:
      app.logger.debug("authenticated")
      app.logger.debug(request.claims['sub'])
      cognito_user_id = request.claims['sub']
      model = MessageGroups.run(cognito_user_id=cognito_user_id)

      if model['errors'] is not None:
        return model['errors'], 422
      else:
        return model['data'], 200

    except TokenVerifyError as e:
      app.logger.debug('unauthenticated')
      data = HomeActivities.run()
      return {}, 401
  else:
    app.logger.debug('unauthenticated')
    data = HomeActivities.run()
    return {}, 401


@app.route("/api/messages/<string:message_group_uuid>", methods=['GET'])

@verify_jwt("message_group_endpoint")

def data_messages(message_group_uuid):

  if request.claims is not None:
    try:
      app.logger.debug("authenticated")
      app.logger.debug(request.claims['sub'])
      cognito_user_id = request.claims['sub']
      model = Messages.run(
        cognito_user_id=cognito_user_id,
        message_group_uuid=message_group_uuid
        )
      if model['errors'] is not None:
        return model['errors'], 422
      else:
        return model['data'], 200

    except TokenVerifyError as e:
      app.logger.debug('unauthenticated')
      data = HomeActivities.run()
      return {}, 401
  else:
    app.logger.debug('unauthenticated')
    data = HomeActivities.run()
    return {}, 401

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()

@verify_jwt("post_message_endpoint")


def data_create_message():
  message_group_uuid   = request.json.get('message_group_uuid',None)
  user_receiver_handle = request.json.get('handle',None)
  message = request.json['message']

  if request.claims is not None:
    try:
      app.logger.debug("authenticated")
      app.logger.debug(request.claims['sub'])
      cognito_user_id = request.claims['sub']
      if message_group_uuid == None:
        # Create for the first time
        app.logger.debug(message_group_uuid)
        app.logger.debug(user_receiver_handle)
        model = CreateMessage.run(
          mode="create",
          message=message,
          cognito_user_id=cognito_user_id,
          user_receiver_handle=user_receiver_handle
        )
      else:
        # Push onto existing Message Group
        model = CreateMessage.run(
          mode="update",
          message=message,
          message_group_uuid=message_group_uuid,
          cognito_user_id=cognito_user_id
        )

      if model['errors'] is not None:
        return model['errors'], 422
      else:
        return model['data'], 200

    except TokenVerifyError as e:
      app.logger.debug('unauthenticated')
      data = HomeActivities.run()
      return {}, 401
  else:
    app.logger.debug('unauthenticated')
    data = HomeActivities.run()
    return {}, 401

@app.route("/api/activities/home", methods=['GET'])
  # New Method
  # Middleware that checks the jwt and passes the info to a request param aclled claims
@verify_jwt("home_activities_endpoint")
def data_home():

  # Old Method

  # access_token = extract_access_token(request.headers)
  # try:
  #   claims = cognito_jwt_token.verify(access_token)
  #   # authenticated request
  #   app.logger.debug("authenicated")
  #   app.logger.debug(claims)
  #   app.logger.debug(claims['username'])
  #   data = HomeActivities.run(cognito_user_id=claims['username'])
  # except TokenVerifyError as e:
  #   # unathenticated request
  #   app.logger.debug(e)
  #   app.logger.debug("unauthenicated")
  #   data = HomeActivities.run()
  #   #data = HomeActivities.run(Logger=LOGGER)
  # return data, 200
  data = HomeActivities.run(request.claims)
  app.logger.debug("########################")
  app.logger.debug(request.claims)

  return data, 200


@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities.run()
  return data, 200

@app.route("/api/activities/@<string:handle>", methods=['GET'])
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():


  # access_token = extract_access_token(request.headers)
  try:
    # claims = cognito_jwt_token.verify(access_token)
    # cognito_user_id = claims["sub"]

    # This is a method I used to pass in the user handle to the create
    # activities endpoint worked for me
    user_handle  = request.json['user_handle']
    message = request.json['message']
    ttl = request.json['ttl']
    model = CreateActivity.run(message, user_handle, ttl)
    # model = CreateActivity.run(message, cognito_user_id, ttl)
    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200
  except TokenVerifyError as e:
    # unauthenticated request
    app.logger.debug(e)
    return {}, 401
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
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/users/@<string:handle>/short", methods=['GET'])
def data_users_short(handle):
  data = UsersShort.run(handle)
  return data, 200


@app.route("/api/profile/update", methods=['POST','OPTIONS'])
@cross_origin()

# Still making use of my Verify JWT Middleware

@verify_jwt("update_profile_endpoint")

def data_update_profile():
  bio          = request.json.get('bio',None)
  display_name = request.json.get('display_name',None)
  access_token = extract_access_token(request.headers)
  app.logger.debug("########################")
  app.logger.debug(request.claims)
  try:
    claims = cognito_jwt_token.verify(access_token)
    cognito_user_id = request.claims['sub']
    model = UpdateProfile.run(
      cognito_user_id=cognito_user_id,
      bio=bio,
      display_name=display_name
    )
    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200
  except TokenVerifyError as e:
    # unauthenicatied request
    app.logger.debug(e)
    return {}, 401




if __name__ == "__main__":
  app.run(debug=True)