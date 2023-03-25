import threading
from concurrent.futures import ThreadPoolExecutor, Future
from uuid import UUID

from cachetools import TTLCache
from fastapi.responses import JSONResponse, Response
from starlette import status

from .model.responses import BasicResponse, ResponseStatus, HistoryGenerationResponse


class BaseTaskController:
    def __init__(
            self,
            task_executor,
            logger,
            max_cached_results: float,
            cached_results_ttl: float,
    ):
        self.log = logger
        self._task_executor = task_executor
        self._network_lock = threading.RLock()
        self._tasks_lock = threading.RLock()
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._tasks: dict[UUID, Future] = dict()
        self._results = TTLCache(maxsize=max_cached_results, ttl=cached_results_ttl)

    def _get_result(self, task_key: UUID) -> JSONResponse:
        if task_key not in self._tasks and task_key not in self._results:
            self.log.debug(f'Requested not existing task: {task_key}')

            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=HistoryGenerationResponse(
                    status=ResponseStatus.NOT_FOUND,
                ).dict(exclude_none=True)
            )

        task: Future

        if task_key in self._tasks:
            task = self._tasks[task_key]
        else:
            task = self._results[task_key]

        if not task.done():
            self.log.debug(f'Requested task that is not ready: {task_key}')

            return JSONResponse(
                status_code=status.HTTP_425_TOO_EARLY,
                content=HistoryGenerationResponse(
                    status=ResponseStatus.TOO_EARLY,
                ).dict(exclude_none=True)
            )

        result = task.result()

        self._tasks.pop(task_key)

        self.log.debug(f'Task received: {task_key}')

        return JSONResponse(
            content=result.dict(exclude_none=True)
        )

    def _request_task_execution(self, body, task_key: UUID) -> JSONResponse:
        try:
            if task_key not in self._tasks and task_key not in self._results:
                self._tasks[task_key] = self._executor.submit(self._task_executor, body)

                self.log.info(f'Submitted task {task_key}')
            else:
                self.log.info(f'Task already exists: {task_key}')

            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED,
                content=BasicResponse(status=ResponseStatus.OK).dict(exclude_none=True)
            )
        except RuntimeError as e:
            self.log.error('An exception has occurred:', e)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=BasicResponse(
                    status=ResponseStatus.INTERNAL_SERVER_ERROR,
                    error_message=f'{e.__class__.__name__}: {e}')
                .dict(exclude_none=True)
            )
