import json
import base64
from google.auth import compute_engine
import functions

credentials = compute_engine.Credentials()

def hello_pubsub(event, context):
    pubsub_message = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    method_name = pubsub_message['protoPayload']['methodName']
    if method_name == "storage.buckets.create":
        # logging.info(f'new bucket created, going to tag bucket {resource_name}')
        return functions.tag_bucket(pubsub_message)

    if method_name == "beta.compute.instances.insert":
        # logging.info(f'new instance created, going to tag instance {resource_name}')
        return functions.tag_instance(pubsub_message)

    if method_name == "google.container.v1beta1.ClusterManager.CreateCluster":
        # logging.info(f'new cluster created, going to tag {resource_name}')
        return functions.tag_cluster(pubsub_message)
