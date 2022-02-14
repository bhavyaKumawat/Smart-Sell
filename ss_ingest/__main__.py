import os

import uvicorn
from ss_ingest.api import ss_ingest

host = os.environ["host_name"]
port = os.environ["ss_ingest_port_no"]
if __name__ == '__main__':
    uvicorn.run(ss_ingest, host=host, port=int(port))
