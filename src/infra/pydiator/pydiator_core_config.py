from src.infra.pydiator.local_mediatr_container import MediatrContainer
from src.infra.pydiator.resolver import TodoResolver
from src.infra.pydiator.test_pipeline import TestPipeline
from src.notification.todo_transaction.transaction_log_subscriber import TransactionLogSubscriber
from src.infra.config.app_config import CACHE_PIPELINE_IS_ENABLED, LOG_PIPELINE_IS_ENABLED
from src.infra.pydiator.cache_provider import get_cache_provider

from pydiator_core.mediatr import pydiator
from pydiator_core.pipelines.cache_pipeline import CachePipeline
from pydiator_core.pipelines.log_pipeline import LogPipeline

from src.core.service.todo.get_todo_all import GetTodoAllRequest
from src.core.service.todo.get_todo_by_id import GetTodoByIdRequest
from src.core.service.todo.add_todo import AddTodoRequest
from src.core.service.todo.update_todo import UpdateTodoRequest
from src.core.service.todo.delete_todo_by_id import DeleteTodoByIdRequest
from src.notification.todo_transaction.transaction_notification import TodoTransactionNotification
from src.notification.todo_transaction.remove_cache_subscriber import TodoRemoveCacheSubscriber


def set_up_pydiator():
    container = MediatrContainer()

    container.register_pipeline(TestPipeline(mediatr_container=container))

    if LOG_PIPELINE_IS_ENABLED:
        container.register_pipeline(LogPipeline())

    if CACHE_PIPELINE_IS_ENABLED:
        cache_pipeline = CachePipeline(get_cache_provider())
        container.register_pipeline(cache_pipeline)

    # Service usecases mapping
    container.register_request(GetTodoAllRequest, TodoResolver.get_todo_all_resolver)
    container.register_request(GetTodoByIdRequest, TodoResolver.get_todo_by_id_resolver)
    container.register_request(AddTodoRequest, TodoResolver.add_todo_resolver)
    container.register_request(UpdateTodoRequest, TodoResolver.update_todo_resolver)
    container.register_request(DeleteTodoByIdRequest, TodoResolver.delete_todo_resolver)

    # Notification mapping
    container.register_notification(TodoTransactionNotification,
                                    [TodoRemoveCacheSubscriber(), TransactionLogSubscriber()])

    # Start
    pydiator.ready(container=container)
