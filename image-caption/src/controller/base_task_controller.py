import threading
from concurrent.futures import ThreadPoolExecutor, Future
from uuid import UUID

from fastapi.responses import JSONResponse, Response
from starlette import status


class BaseTaskController:
    def __init__(self, task_executor, logger):
        self.log = logger
        self.task_executor = task_executor
        self.network_lock = threading.RLock()
        self.tasks_lock = threading.RLock()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.tasks: dict[UUID, Future] = dict()

    def _get_result(self, task_key: UUID) -> Response:
        if task_key not in self.tasks:
            self.log.debug(f'Requested not existing task: {task_key}')
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        task = self.tasks[task_key]

        if not task.done():
            self.log.debug(f'Requested task that is not ready: {task_key}')
            return Response(status_code=status.HTTP_425_TOO_EARLY)

        result = task.result()

        self.tasks.pop(task_key)

        self.log.debug(f'Task received: {task_key}')

        return JSONResponse(
            content=result.dict(exclude_none=True)
        )

    def _request_task_execution(self, body, task_key: UUID) -> Response:
        if task_key not in self.tasks:
            self.log.info(f'Submitted task {task_key}')
            self.tasks[task_key] = self.executor.submit(self.task_executor, body)
        else:
            self.log.info(f'Task already exists: {task_key}')

        return Response(
            status_code=status.HTTP_201_CREATED
        )
