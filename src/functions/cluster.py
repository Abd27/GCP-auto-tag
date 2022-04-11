from google.cloud import container_v1

import helper_functions

def tag_cluster(pubsub_message):
    creator_email = pubsub_message['protoPayload']['authenticationInfo']['principalEmail']
    cluster_name = pubsub_message['protoPayload']['resourceName']
    client = container_v1.ClusterManagerClient()
    cluster = client.get_cluster(name=cluster_name)
    labels = helper_functions.gen_labels(creator_email)
    # Add any existing labels
    labels.update(cluster.resource_labels)

    request = container_v1.SetLabelsRequest(
        label_fingerprint=cluster.label_fingerprint,
        resource_labels=labels,
        name=cluster_name
    )

    try:
        client.set_labels(request=request)
        return True
    except Exception as err:
        print(str(err))
        return False
