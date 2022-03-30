from google.cloud import container_v1

def tag_cluster(name: str, creator_email: str):
    client = container_v1.ClusterManagerClient()
    cluster = client.get_cluster(name=name)
    labels = {
        'created_by' : creator_email,
        'created-date' : cluster.create_time.split("+")[0].lower().replace(':', '_', ).replace('.', '_')
    }
    # Add any existing labels
    labels.update(cluster.resource_labels)

    request = container_v1.SetLabelsRequest(
        label_fingerprint=cluster.label_fingerprint,
        resource_labels=labels,
        name=name
    )

    try:
        client.set_labels(request=request)
        return True
    except Exception as e:
        print(str(e))
        return False