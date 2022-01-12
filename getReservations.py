import asyncio
from pprint import pprint
from netlab.async_client import NetlabClient
import datetime

async def main():
    async with NetlabClient() as connection:
        connection: NetlabConnection
        status = await connection.system_status_get()
        out = await connection.reservation_summary()
        pprint(out)
        out2 = await connection.reservation_query(cls_id=11)
        for i in out2:
            if i['cls_id'] == 3:
                a = await connection.user_account_get(acc_id=i['acc_id'])
                print(f"User:{i['acc_full_name']}\nActive:{i['res_is_active']}\nStart:{str(i['res_start'])}\n{a['acc_email']}\n{i['pod_name']}\n")

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
