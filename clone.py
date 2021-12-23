#Created by Ryan Haley - DePaul University
from pprint import pprint
from netlab import enums

async def clonePod(connection,masterPodName,datastore,newPodName,podStart,podStop,replacePod):
    pc_clone_specs =[]


    if podStart < 2:
        print('podStart cannot be 1 of less!')
        return

    #Parse through all pods
    pods = await connection.pod_list()

    #Find POD ID of master pod
    for i in pods:
        if i["pod_name"]== masterPodName:
            print('='*20 + f'Found master: {i["pod_name"]}' + '='*20 )
            pprint(i)
            MasterPodId = i["pod_id"]
            
    #Get information for current pod to clone
    for currentPod in range(podStart,podStop):
        for pod in pods:
            if pod["pod_name"]==f"{newPodName}{currentPod}":
                    podName=pod["pod_name"]
                    CurrentPodId = pod["pod_id"]
        print('='*20 + f'Gathering info to clone new pod: {podName}' + '='*20 )
        print()
        #Determine if we are creating a new pod or replacing an existing pod
        if replacePod:
             CurrentPodId = CurrentPodId
        elif not replacePod:
             #Get next available pod ID number
             pods = await connection.pod_list()
             nextAvailablePodID = pods[-1]["pod_id"]+1
             CurrentPodId = nextAvailablePodID

        #Parse throug master pod for cloning paramaters
        p = await connection.pod_get(pod_id=MasterPodId, properties='all')
        for j in p['remote_pc']:
            tmp = {}
            tmp['source_snapshot'] = 'init'
            tmp['source_vm_id'] = j['vm_id']
            tmp['pc_type'] = 'AVMI'
            #ID of esxi server running VMs
            tmp['clone_vh_id'] = j['vh_id']
            tmp['clone_name'] = j['vm_name'].replace('POD1',f'POD{currentPod}')
            tmp['clone_type'] = 'FULL'
            tmp['clone_role'] = 'NORMAL'
            tmp['clone_datastore'] = datastore
            tmp['clone_storage_alloc'] = 'ONDEMAND'
            tmp['clone_snapshot'] = 'init'
            pc_clone_specs.append(tmp)
        
        ans = input(f'**********\nWARNING: You are about to delete pod:{CurrentPodId}. podName:{podName}. Do you wish to continue?\n**********(y/n)')
        if ans.lower() != 'y':
            print('[]Operation aborted due to use cancelation')
            return
        #Remove old pod
        await connection.pod_state_change(pod_id=CurrentPodId, state=enums.PodState.OFFLINE)
        await connection.pod_remove_task(pod_id=CurrentPodId, remove_vms=enums.RemoveVMS.DISK)
        print(f'[+]Successfully removed pod {CurrentPodId}')


        #Clone pod
        print('='*20 + 'Passing pod parameters for cloning' + '='*20 )
        pprint(pc_clone_specs)
        try:     
            info = await connection.pod_clone_task(source_pod_id=MasterPodId,clone_pod_id=CurrentPodId,
                                                           clone_pod_name=f"{newPodName}{currentPod}",pc_clone_specs=pc_clone_specs)
            print(f'[+]Successfully cloned new pod: {newPodName}{currentPod}')
        except Exception as e:
            print('[-]Possible error when cloning pod: {newPodName}{currentPod}')
        
        #Set ACLs on new pod
        print('='*20 + 'Setting ACL on new pod' + '='*20 )
        await connection.pod_update(pod_id=CurrentPodId,pod_acl_enabled=True)
        if '378' in pc_clone_specs[0]['clone_name']:
            cls_id = 1
        elif '380' in pc_clone_specs[0]['clone_name']:
            cls_id = 2
        elif '388' in pc_clone_specs[0]['clone_name']:
            cls_id = 3
        elif '395' in pc_clone_specs[0]['clone_name']:
            cls_id = 4
        elif '340' in pc_clone_specs[0]['clone_name']:
            cls_id = 5
        elif '594' in pc_clone_specs[0]['clone_name']:
            cls_id = 6
        try:
            acls = await connection.pod_acl_add(com_id=1, pod_id=CurrentPodId, acc_id=None, cls_id=cls_id, team=None)
        except:
            print('Duplicate ACL found. Skipping...')


        
    print('complete?')

