require 'aws-sdk-s3'
require 'json'

def handler(event:,context:)
    puts event
    s3 = Aws::S3::Resource.new
    bucket_name = ENV["UPLOADS_BUCKET_NAME"]
    object_key = 'mock.jpg'

    obj = s3.bucket(bucket_name).object(object_key)
    url = obj.presigned_url(:put, expires_in: 60 * 5)
    url # This is the data that will be returned
    body = {url: url}.to_json
    {
        headers: {
            "Access-Control-Allow-Headers": "*, Authorization",
            "Acess-Control-Allow-Origin": "https://*.gitpod.io"
            "Acess-Control-Allow-Mehods": "OPTIONS,GET,POST"
        },
        statusCode: 200, 
        body: body }
         # This is the data that will be returned
end
