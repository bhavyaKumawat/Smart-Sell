import os

import uvicorn
from ingest.api import ss_ingest

host = os.environ["host_name"]
port = os.environ["port_no"]
if __name__ == '__main__':
    uvicorn.run(ss_ingest, host=host, port=int(port))
