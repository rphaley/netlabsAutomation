async def removePod():

    async with NetlabClient() as connection:
        await connection.pod_remove_task(pod_id=OldCurrentPodId, remove_vms=enums.RemoveVMS.DISK)
