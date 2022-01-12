from netlab.async_client import NetlabClient

async def setACL(connection,CurrentPodId,pc_clone_specs):
    async with NetlabClient() as connection:
        #Set ACLs on new pod
        print('='*20 + 'Setting ACL on new pod' + '='*20 )
        await connection.pod_update(pod_id=CurrentPodId,pod_acl_enabled=True)
        if '378' in pc_clone_specs[0]['clone_name']:
            cls_id = 11
        elif '380' in pc_clone_specs[0]['clone_name']:
            cls_id = 12
        elif '388' in pc_clone_specs[0]['clone_name']:
            cls_id = 3
        elif '395' in pc_clone_specs[0]['clone_name']:
            cls_id = 13
        elif '340' in pc_clone_specs[0]['clone_name']:
            cls_id = 18
        elif '594' in pc_clone_specs[0]['clone_name']:
            cls_id = 15
        try:
            acls = await connection.pod_acl_add(com_id=1, pod_id=CurrentPodId, acc_id=None, cls_id=cls_id, team=None)
        except:
            print('Duplicate ACL found. Skipping...')
