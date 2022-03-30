import googleapiclient.discovery
import logging

compute = googleapiclient.discovery.build('compute', 'v1')
def tag_instance(instance: str, project: str, zone: str, creator_email: str):
        # if instance tag was successful and the instance volume list exists
    instance_tag = tag_vm(instance, project, zone, creator_email)
    if instance_tag and instance_tag['instance_disks_list']:
        disks_list = instance_tag['instance_disks_list']
        # tag volumes
        disks_tag = tag_disks(disks_list, project, zone, instance, creator_email)
        if disks_tag:
            return True
    


def tag_vm(instance: str, project: str, zone: str, creator_email: str):
    # tag (label) the instance and return a list of the disk volumes
    instance_information = compute.instances().get(project=project, zone=zone, instance=instance).execute()
    instance_disks_list = [disk['deviceName'] for disk in instance_information['disks']]
    logging.info(f'going to tag disk {instance_disks_list}')
    instance_fingerprint = instance_information['labelFingerprint']
    labels = {
        'created-by' : creator_email,
        'created-date' : instance_information['creationTimestamp'].lower().replace(':', '_', ).replace('.', '_')
    } 

    if 'labels' in instance_information: labels.update(instance_information['labels'])

    instance_labels = {'labels': labels, 'labelFingerprint': instance_fingerprint}
    request = compute.instances().setLabels(project=project, zone=zone, instance=instance, body=instance_labels)
    try:
        request.execute()
        return {'status': True, 'instance_disks_list': instance_disks_list}
    except Exception as e:
        print(str(e))
        return {'status': False, instance_disks_list: []}


def tag_disks(disks_list: list, project: str, zone: str, instance_name: str, creator_email: str):
    # tag a volume from the instance volume list
    for disk in disks_list:
        logging.info(f'going to tag disk {disk}')
        try:
            disk_data = compute.disks().get(project=project, zone=zone, disk=disk).execute()
        # if the instance is part of instace template - the api volume name is the instance template name, but the actual volume name is the instance name
        except googleapiclient.errors.HttpError:
            disk_data = compute.disks().get(project=project, zone=zone, disk=instance_name).execute()
            disk = instance_name
            
        disk_fingerprint = disk_data['labelFingerprint']
        disk_labels = {'labels': {'created-by': creator_email, 'instance': instance_name},
                       'labelFingerprint': disk_fingerprint}
        try:
            compute.disks().setLabels(project=project, zone=zone, resource=disk, body=disk_labels).execute()
        except Exception as e:
            print(str(e))
    return True