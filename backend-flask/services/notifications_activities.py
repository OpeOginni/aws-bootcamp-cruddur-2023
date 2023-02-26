from datetime import datetime, timedelta, timezone

# X-RAY --------
from aws_xray_sdk.core import xray_recorder

class NotificationsActivities:
  def run():

    # X-RAY --------
    #segment = xray_recorder.begin_segment('user_activities')
    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()
    results = [{
      'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
      'handle':  'Coco',
      'message': 'I am a white unicorn',
      'created_at': (now - timedelta(days=2)).isoformat(),
      'expires_at': (now + timedelta(days=5)).isoformat(),
      'likes_count': 5,
      'replies_count': 1,
      'reposts_count': 0,
      'replies': [{
        'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea67',
        'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
        'handle':  'Worf',
        'message': 'This post has no honor!',
        'likes_count': 0,
        'replies_count': 0,
        'reposts_count': 0,
        'created_at': (now - timedelta(days=2)).isoformat()
      }],
    },
    ]

    # X-RAY --------
    subsegment = xray_recorder.begin_subsegment('mock-data')
    # Adding Test Annotations
    subsegment.put_annotation('user', "Me: Opeyemi")
    subsegment.put_annotation('annotation_type', "Test Annotation")
    # Adding Metadata
    dict = {
      "now": now.isoformat(),
      "results-size": len(results)
    }
    subsegment.put_metadata('key', dict, 'namespace')
    # You have to END the subsegment
    xray_recorder.end_subsegment()
    return results