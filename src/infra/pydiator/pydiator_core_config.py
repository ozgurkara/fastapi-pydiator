from src.infra.adapter.repository.todo.delete_todo_by_id_data import DeleteTodoByIdDataUseCase, DeleteTodoByIdDataRequest
from src.notification.todo_transaction.transaction_log_subscriber import TransactionLogSubscriber
from src.infra.config.app_config import CACHE_PIPELINE_IS_ENABLED, LOG_PIPELINE_IS_ENABLED
from src.infra.pydiator.cache_provider import get_cache_provider

from pydiator_core.mediatr import pydiator
from pydiator_core.mediatr_container import MediatrContainer
from pydiator_core.pipelines.cache_pipeline import CachePipeline
from pydiator_core.pipelines.log_pipeline import LogPipeline

from src.core.service.todo.get_todo_all import GetTodoAllRequest, GetTodoAllUseCase
from src.core.service.todo.get_todo_by_id import GetTodoByIdRequest, GetTodoByIdUseCase
from src.core.service.todo.add_todo import AddTodoRequest, AddTodoUseCase
from src.core.service.todo.update_todo import UpdateTodoRequest, UpdateTodoUseCase
from src.core.service.todo.delete_todo_by_id import DeleteTodoByIdRequest, DeleteTodoByIdUseCase
from src.notification.todo_transaction.transaction_notification import TodoTransactionNotification
from src.notification.todo_transaction.remove_cache_subscriber import TodoRemoveCacheSubscriber

from src.infra.adapter.repository.todo.get_todo_all_data import GetTodoAllDataRequest, GetTodoAllDataUseCase
from src.infra.adapter.repository.todo.get_todo_by_id_data import GetTodoByIdDataRequest, GetTodoByIdDataUseCase
from src.infra.adapter.repository.todo.add_todo_data import AddTodoDataUseCase, AddTodoDataRequest
from src.infra.adapter.repository.todo.update_todo_data import UpdateTodoDataRequest, UpdateTodoDataUseCase


def set_up_pydiator():
    container = MediatrContainer()


    if LOG_PIPELINE_IS_ENABLED:
        container.register_pipeline(LogPipeline())

    if CACHE_PIPELINE_IS_ENABLED:
        cache_pipeline = CachePipeline(get_cache_provider())
        container.register_pipeline(cache_pipeline)

    # Service usecases mapping
    container.register_request(GetTodoAllRequest, GetTodoAllUseCase())
    container.register_request(GetTodoByIdRequest, GetTodoByIdUseCase())
    container.register_request(AddTodoRequest, AddTodoUseCase())
    container.register_request(UpdateTodoRequest, UpdateTodoUseCase())
    container.register_request(DeleteTodoByIdRequest, DeleteTodoByIdUseCase())

    # Data usecases mapping
    container.register_request(GetTodoAllDataRequest, GetTodoAllDataUseCase())
    container.register_request(GetTodoByIdDataRequest, GetTodoByIdDataUseCase())
    container.register_request(AddTodoDataRequest, AddTodoDataUseCase())
    container.register_request(DeleteTodoByIdDataRequest, DeleteTodoByIdDataUseCase())
    container.register_request(UpdateTodoDataRequest, UpdateTodoDataUseCase())

    # Notification mapping
    container.register_notification(TodoTransactionNotification,
                                    [TodoRemoveCacheSubscriber(), TransactionLogSubscriber()])

    # Start
    pydiator.ready(container=container)
