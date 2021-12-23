#Created by Ryan Haley - DePaul University
from netlab import enums

async def bringPodUp(connection,newPodName,podStart,podStop):
    pods = await connection.pod_list()
    for currentPod in range(podStart,podStop):
        for pod in pods:
            if pod["pod_name"]==f"{newPodName}{currentPod}":
                podName=pod["pod_name"]
                CurrentPodId = pod["pod_id"]
                print(podName)

    await connection.pod_state_change(pod_id=CurrentPodId, state=enums.PodState.ONLINE)
    print(f'[+]{podName} brought online!')
          
async def bringPodDown(connection,newPodName,podStart,podStop):
    pods = await connection.pod_list()
    for currentPod in range(podStart,podStop):
        for pod in pods:
            if pod["pod_name"]==f"{newPodName}{currentPod}":
                podName=pod["pod_name"]
                CurrentPodId = pod["pod_id"]
                print(podName)

    await connection.pod_state_change(pod_id=CurrentPodId, state=enums.PodState.OFFLINE)
    print(f'[+]{podName} brought offline!')

