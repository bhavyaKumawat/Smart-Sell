from archive_processor_svc.archive_proc_batch import process_sm_archive
import asyncio
if __name__ == '__main__':
    asyncio.run(process_sm_archive())
