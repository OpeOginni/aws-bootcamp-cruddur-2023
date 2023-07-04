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
from services.users_short import UsersShort
from services.update_profile import UpdateProfile
from services.user_activities import UserActivities
from services.show_activity import ShowActivity


def load(app):
    @app.route("/api/activities/@<string:handle>", methods=['GET'])
    def data_users_activities(handle):
        model = UserActivities.run(handle)
        return model_json(model)

    @app.route("/api/activities/@<string:handle>/status/<string:activity_uuid>", methods=['GET'])
    @cross_origin()
    def data_show_activities(handle, activity_uuid):
        data = ShowActivity.run(activity_uuid)
        # print(data)
        return data, 200 # The type of data was an array so I had to return the first index

    @app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
    def data_show_activity(handle, activity_uuid):
        data = ShowActivity.run(activity_uuid=activity_uuid)
        return data, 200

    @app.route("/api/users/@<string:handle>/short", methods=['GET'])
    def data_users_short(handle):
        data = UsersShort.run(handle)
        return data, 200

    @app.route("/api/profile/update", methods=['POST', 'OPTIONS'])
    @cross_origin()
    # Still making use of my Verify JWT Middleware
    @verify_jwt("update_profile_endpoint")
    @jwt_required()
    def data_update_profile():
        bio = request.json.get('bio', None)
        display_name = request.json.get('display_name', None)
        access_token = extract_access_token(request.headers)

        model = UpdateProfile.run(
            cognito_user_id=g.cognito_user_id,
            bio=bio,
            display_name=display_name
        )
        return model_json(model)
