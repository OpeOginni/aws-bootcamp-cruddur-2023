from flask import request
from lib.cognito_jwt_token import CognitoJwtToken, extract_access_token, TokenVerifyError
import os


cognito_jwt_token = CognitoJwtToken(
  user_pool_id= os.getenv('AWS_COGNITO_USER_POOL_ID'),
  user_pool_client_id= os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID"),
  region= os.getenv("AWS_DEFAULT_REGION")
  )

  # Had to Debug my MiddleWare Used ChatGPT

def verify_jwt(func_name):
    def decorator(func):
      def wrapper(*args, **kwargs):
          try:
              access_token = extract_access_token(request.headers)
              claims = cognito_jwt_token.verify(access_token)
              request.claims = claims
          except TokenVerifyError as e:
              claims = None
              request.claims = claims
          return func(*args, **kwargs)
      wrapper.__name__ = f"{func_name}_wrapper"
      return wrapper
    return decorator
