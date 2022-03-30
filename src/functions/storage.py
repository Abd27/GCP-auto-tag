from google.cloud import storage

def tag_bucket(bucket_name: str, creator_email: str):
    bucket = storage.Client().get_bucket(bucket_name)
    labels = bucket.labels
    labels['created-by'] = creator_email
    labels["created-date"] = bucket.time_created.strftime("%d-%m-%Y, %H-%M-%S").replace(', ', 't')
    bucket.labels = labels
    try:
        bucket.patch()
        return True
    except Exception as e:
        print(str(e))
        return False    
