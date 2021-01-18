from app.data.todo.usecases.delete_todo_by_id_data import DeleteTodoByIdDataUseCase, DeleteTodoByIdDataRequest
from app.notification.todo_transaction.transaction_log_subscriber import TransactionLogSubscriber
from app.utils.config import CACHE_PIPELINE_IS_ENABLED, TRACER_IS_ENABLED, LOG_PIPELINE_IS_ENABLED, \
    TRACER_PIPELINE_IS_ENABLED
from app.utils.cache_provider import get_cache_provider

from pydiator_core.mediatr import pydiator
from pydiator_core.mediatr_container import MediatrContainer
from pydiator_core.pipelines.cache_pipeline import CachePipeline
from pydiator_core.pipelines.log_pipeline import LogPipeline
from app.utils.pydiator.pipelines.tracer_pipeline import TracerPipeline

from app.resources.todo.usecases.get_todo_all import GetTodoAllRequest, GetTodoAllUseCase
from app.resources.todo.usecases.get_todo_by_id import GetTodoByIdRequest, GetTodoByIdUseCase
from app.resources.todo.usecases.add_todo import AddTodoRequest, AddTodoUseCase
from app.resources.todo.usecases.update_todo import UpdateTodoRequest, UpdateTodoUseCase
from app.resources.todo.usecases.delete_todo_by_id import DeleteTodoByIdRequest, DeleteTodoByIdUseCase
from app.notification.todo_transaction.transaction_notification import TodoTransactionNotification
from app.notification.todo_transaction.remove_cache_subscriber import TodoRemoveCacheSubscriber

from app.data.todo.usecases.get_todo_all_data import GetTodoAllDataRequest, GetTodoAllDataUseCase
from app.data.todo.usecases.get_todo_by_id_data import GetTodoByIdDataRequest, GetTodoByIdDataUseCase
from app.data.todo.usecases.add_todo_data import AddTodoDataUseCase, AddTodoDataRequest
from app.data.todo.usecases.update_todo_data import UpdateTodoDataRequest, UpdateTodoDataUseCase


def set_up_pydiator():
    container = MediatrContainer()

    if TRACER_IS_ENABLED and TRACER_PIPELINE_IS_ENABLED:
        container.register_pipeline(TracerPipeline())

    if LOG_PIPELINE_IS_ENABLED:
        container.register_pipeline(LogPipeline())

    if CACHE_PIPELINE_IS_ENABLED:
        cache_pipeline = CachePipeline(get_cache_provider())
        container.register_pipeline(cache_pipeline)

    # Service usecases mapping
    # container.register_request(GetSampleByIdRequest, GetSampleByIdUseCase())
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
