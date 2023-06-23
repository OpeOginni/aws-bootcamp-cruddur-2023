# General
import os
import sys

# Flask
from flask import Flask
from flask import request, g

# Decorators
from lib.rollbar import init_rollbar
from lib.xray import init_xray
from lib.honeycomb import init_honeycomb
from lib.cors import init_cors
from lib.cognito_jwt_token import jwt_required
from lib.cloudwatch import init_cloudwatch

# MIDDLEWARE
from middleware.jwt_middleware import verify_jwt

import routes.activities
import routes.users
import routes.messages
import routes.general


# IMPORTANT PYTHON APP DECLARATION
app = Flask(__name__)

# initialization -------------
init_xray(app)
init_honeycomb(app)
init_cors(app)
# with app.app_context():
#   g.rollbar = init_rollbar(app)

# load routes -------------
routes.general.load(app)
routes.activities.load(app)
routes.users.load(app)
routes.messages.load(app)







if __name__ == "__main__":
  app.run(debug=True)