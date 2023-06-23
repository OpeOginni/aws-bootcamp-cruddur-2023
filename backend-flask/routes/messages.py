# flask
from flask import request, g
from flask_cors import cross_origin

# decorators
from aws_xray_sdk.core import xray_recorder
from lib.cognito_jwt_token import jwt_required
from middleware.jwt_middleware import verify_jwt

# helpers
from lib.helpers import model_json

# services
from services.create_message import *
from services.messages import *
from services.message_groups import *


def load(app):
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
