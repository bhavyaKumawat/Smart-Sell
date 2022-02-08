from lb_processor_svc.lb_proc_batch import process_sm_lb
import asyncio
if __name__ == '__main__':
    asyncio.run(process_sm_lb())
