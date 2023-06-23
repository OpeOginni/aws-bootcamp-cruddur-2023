# flask
from flask import request, g
from flask_cors import cross_origin

# decorators
from aws_xray_sdk.core import xray_recorder
from lib.cognito_jwt_token import jwt_required
from middleware.jwt_middleware import verify_jwt

# helpers
from lib.helpers import model_json

# servicees
from services.home_activities import HomeActivities
from services.notifications_activities import NotificationsActivities
from services.create_activity import CreateActivity
from services.search_activities import SearchActivities
from services.show_activity import ShowActivities
from services.create_reply import CreateReply

def load(app):
    def default_home_feed(e):
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
        data = ShowActivities.run(activity_uuid=activity_uuid)
        return data, 200

    @app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
    @cross_origin()
    def data_activities_reply(activity_uuid):
        user_handle  = 'andrewbrown'
        message = request.json['message']
        model = CreateReply.run(message, user_handle, activity_uuid)
        return model_json(model)
