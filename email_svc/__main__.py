import os

import uvicorn
from email_svc.api import ss_email

host = os.environ["host_name"]
port = os.environ["port_no"]
if __name__ == '__main__':
    uvicorn.run(ss_email, host=host, port=int(port))
