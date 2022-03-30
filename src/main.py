import functions
import logging
import json
import base64
from google.auth import compute_engine

credentials = compute_engine.Credentials()

def hello_pubsub(event, context):
    pubsub_message = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    # pubsub variables
    user_email = pubsub_message['protoPayload']['authenticationInfo']['principalEmail'].replace('@', '_', ).replace('.', '-')
    if 'zone' in pubsub_message['resource']['labels']: zone = pubsub_message['resource']['labels']['zone']
    project_id = pubsub_message['resource']['labels']['project_id']
    path_resource_name = pubsub_message['protoPayload']['resourceName']
    resource_name = functions.get_resource_name(path_resource_name)                  # Parse path to retrive instance name
    # method name for different resource creations
    method_name = pubsub_message['protoPayload']['methodName']

    if method_name == "storage.buckets.create":
        
        logging.info(f'new bucket created, going to tag bucket {resource_name}')
        return functions.tag_bucket(resource_name, user_email)

    elif method_name == "beta.compute.instances.insert":
        
        logging.info(f'new instance created, going to tag instance {resource_name}')
        return functions.tag_instance(resource_name, project_id, zone, user_email)

    elif method_name == "google.container.v1beta1.ClusterManager.CreateCluster":

        logging.info(f'new cluster created, going to tag {resource_name}')
        return functions.tag_cluster(creator_email=user_email, name=path_resource_name)