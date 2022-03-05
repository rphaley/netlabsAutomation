#Created by Ryan Haley - DePaul University
from pprint import pprint
from netlab import enums
from setACLs import setACL

async def clonePod(connection,masterPodName,datastore,newPodName,podStart,podStop,replacePod,replacePodNum):
    #Checking to ensure master pod is not deleted
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
    cnt = 0
    for currentPod in range(podStart,podStop):
        print('='*20 + f'Gathering info to clone new pod' + '='*20 )

        #Determine if we are creating a new pod or replacing an existing pod
        if replacePod:
            for pod in pods:
                if pod["pod_name"]==f"{newPodName}{currentPod}":
                    podName=pod["pod_name"]
                    CurrentPodId = pod["pod_id"]
                    break
                
        elif not replacePod:
            podName = newPodName
            if replacePodNum == 0:
                #Get next available pod ID number
                pods = await connection.pod_list()
                nextAvailablePodID = pods[-1]["pod_id"]+1
                CurrentPodId = nextAvailablePodID
            else:
                CurrentPodId = replacePodNum + cnt
        try:
            OldCurrentPodId = CurrentPodId
        except:
            print(f'[-] Pod name mismatch.  Check that pod being replaced has name of {newPodName}')
        print('='*20 + f'Cloning to pod ID: {CurrentPodId}' + '='*20)
        cnt += 1

        #Remove old pod
        if replacePod:
            ans = input(f'**********\nWARNING: You are about to delete pod:{OldCurrentPodId}. podName:{podName}. Do you wish to continue?\n**********(y/n)')
            if ans.lower() != 'y':
                print('[]Operation aborted due to use cancelation')
                return
            await connection.pod_state_change(pod_id=OldCurrentPodId, state=enums.PodState.OFFLINE)
            await connection.pod_remove_task(pod_id=OldCurrentPodId, remove_vms=enums.RemoveVMS.DISK)
            print(f'[+]Successfully removed pod {CurrentPodId}')


        #Clone pod
        print('='*20 + 'Passing pod parameters for cloning' + '='*20 )
        #Parse throug master pod for cloning paramaters
        pc_clone_specs =[]
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
        print('[+]Master pod parsed successfully')
        pprint(pc_clone_specs)
        
        try:     
            info = await connection.pod_clone_task(source_pod_id=MasterPodId,clone_pod_id=CurrentPodId,
                                                           clone_pod_name=f"{newPodName}{currentPod}",pc_clone_specs=pc_clone_specs)
            print(f'[+]Successfully cloned new pod: {newPodName}{currentPod}')
        except Exception as e:
            print(f'[-]Possible error when cloning pod: {newPodName}{currentPod}')
            print(e)

        #Set ACL on pod
        try:
            await setACL(connection,CurrentPodId,pc_clone_specs)
            print(f'[+]Successfully set ACL on pod: {newPodName}{currentPod}')
        except Exception as e:
            print(f'[-]Possible error when setting ACL on pod: {newPodName}{currentPod}')
            print(f'Error {e}')

       
    print('complete?')

