from google.cloud import storage
import helper_functions


def tag_bucket(pubsub_message):
    creator_email, bucket_name = helper_functions.unload_pubsub(pubsub_message)
    bucket = storage.Client().get_bucket(bucket_name)
    labels = helper_functions.gen_labels(creator_email)
    # Add any existing labels
    labels.update(bucket.labels)
    bucket.labels = labels
    try:
        bucket.patch()
        return True
    except Exception as e:
        print(str(e))
        return False
   
