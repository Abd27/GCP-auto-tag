import helper_functions

def unload_pubsub(pubsub_message):
    creator_email = pubsub_message['protoPayload']['authenticationInfo']['principalEmail']
    resource_path = pubsub_message['protoPayload']['resourceName']
    resource_name = helper_functions.get_resource_name(resource_path)                    # Parse path to retrive instance name

    return creator_email, resource_name