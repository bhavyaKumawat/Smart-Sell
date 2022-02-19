import asyncio
from lookup_svc.lookup_svc_batch import process_sm_lookup

if __name__ == '__main__':
    asyncio.run(process_sm_lookup())

