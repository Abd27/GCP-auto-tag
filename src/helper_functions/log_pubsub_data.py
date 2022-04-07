import base64
import logging

def log_data(event, context):
     # log the incomming pub/sub data on cloud funtion logs for debugging
    print("""This Function was triggered by messageId {} published at {} to {}
    """.format(context.event_id, context.timestamp, context.resource["name"]))
    if 'data' in event:
        name = base64.b64decode(event['data']).decode('utf-8')
    else:
        name = 'World'
    print('Hello {}!'.format(name))
    logging.info(event)
    return