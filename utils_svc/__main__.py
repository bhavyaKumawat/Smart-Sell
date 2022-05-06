import os
import uvicorn
from utils_svc.api import ss_utils

host = os.environ["host_name"]
port = os.environ["port_no"]
if __name__ == '__main__':
    uvicorn.run(ss_utils, host=host, port=int(port))
