#Created by Ryan Haley - DePaul University
##API Documentation
##https://netlab-py.s3.amazonaws.com/docs/api/autoapi/netlab.api.html#netlab.api.PodApiMixin.pod_clone_task
##
##https://www.netdevgroup.com/support/documentation/netlabve/netlabve_application_program_interface_guide.pdf
##
##https://www.netdevgroup.com/support/documentation/netlabve/netlabve_administrator_guide.pdf
##
import asyncio
from pprint import pprint
from netlab.async_client import NetlabClient
from clone import clonePod
import podState
import configparser

async def main():
    config = configparser.ConfigParser()
    config.read('settings.txt')
    masterPodName = config['DEFAULT']['masterPodName']
    datastore = config['DEFAULT']['datastore']
    newPodName = config['DEFAULT']['newPodName']
    podStart = int(config['DEFAULT']['podStart']) #THIS SHOULD NEVER BE 1!
    podStop = int(config['DEFAULT']['podStop'])
    replacePod = bool(config['DEFAULT']['replacePod']) #true if you want to replace existing pod, false if you want to create new pod
    replacePodNum = bool(config['DEFAULT']['replacePodNum'])
    
    async with NetlabClient() as connection:
        #Test connection/auth is working properly
        try:
            info = await asyncio.wait_for(connection.system_status_get(),timeout=1)
        except:
            print('[-] Could not connect to server.  Is VPN up?')
        if info: print("[+]Successfully connected!")
        pprint(info)

        #Clone PODs
        await podState.bringPodDown(connection,newPodName,podStart,podStop)
        await clonePod(connection,masterPodName,datastore,newPodName,podStart,podStop,replacePod,replacePodNum)

        #Bring pod up/down
        await podState.bringPodUp(connection,newPodName,podStart,podStop)
##        await podState.bringPodDown(connection,newPodName,podStart,podStop)
 

    
        
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
