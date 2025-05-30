import asyncio
import os
from io import BytesIO

import uvicorn
from miniopy_async import Minio


async def async_main():
    pass


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    # main()
    # sys.exit(0)
    port: int = int(os.environ.get('SERVER_PORT', '8081'))
    host: str = os.environ.get('SERVER_HOST', '0.0.0.0')

    uvicorn.run("main:app", host=host, port=port, reload=False, workers=1, log_config='logging.yaml')
