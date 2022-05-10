import os

import uvicorn
from file.api import ss_file

host = os.environ["host_name"]
port = os.environ["port_no"]
if __name__ == '__main__':
    uvicorn.run(ss_file, host=host, port=int(port))
