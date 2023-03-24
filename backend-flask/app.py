from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os
import sys

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

# MIDDLEWARE


@app.route("/api/message_groups", methods=['GET'])
# Using my verify_jwt middleware
@verify_jwt("message_groups_endpoint")
# This middleware passes the claim in the req and it can be obtained using request.claims

def data_message_groups():

  app.logger.debug("########################")
  app.logger.debug(request.claims)

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


@app.route("/api/messages/@<string:handle>", methods=['GET'])
def data_messages(handle):
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.args.get('user_reciever_handle')

  model = Messages.run(user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.json['user_receiver_handle']
  message = request.json['message']

  model = CreateMessage.run(message=message,user_sender_handle=user_sender_handle,user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

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
  # This bug took me a LONG time to fix lol....
  user_handle  = request.json['user_handle']
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, user_handle, ttl)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

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

if __name__ == "__main__":
  app.run(debug=True)