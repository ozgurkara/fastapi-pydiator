from app.data.todo.handlers.delete_todo_by_id_data_handler import DeleteTodoByIdDataHandler, DeleteTodoByIdDataRequest
from app.utils.config import redis_key_prefix, cache_pipeline_is_active, distributed_cache_is_active
from app.utils.client_factory import get_distributed_cache_provider
from app.utils.distributed_cache_provider import DistributedCacheProvider

from pydiator_core.mediatr import pydiator
from pydiator_core.mediatr_container import MediatrContainer
from pydiator_core.pipelines.cache_pipeline import CachePipeline
from pydiator_core.pipelines.log_pipeline import LogPipeline

from app.resources.todo.handlers.get_todo_all_handler import GetTodoAllRequest, GetTodoAllHandler
from app.resources.todo.handlers.get_todo_by_id_handler import GetTodoByIdRequest, GetTodoByIdHandler
from app.resources.todo.handlers.add_todo_handler import AddTodoRequest, AddTodoHandler
from app.resources.todo.handlers.update_todo_handler import UpdateTodoRequest, UpdateTodoHandler
from app.resources.todo.handlers.delete_todo_by_id_handler import DeleteTodoByIdRequest, DeleteTodoByIdHandler
from app.resources.todo.notifications.todo_cache_remove_handler import TodoChangeNotification, \
    TodoCacheRemoveNotificationHandler

from app.data.todo.handlers.get_todo_all_data_handler import GetTodoAllDataRequest, GetTodoAllDataHandler
from app.data.todo.handlers.get_todo_by_id_data_handler import GetTodoByIdDataRequest, GetTodoByIdDataHandler
from app.data.todo.handlers.add_todo_data_handler import AddTodoDataHandler, AddTodoDataRequest
from app.data.todo.handlers.update_todo_data_handler import UpdateTodoDataRequest, UpdateTodoDataHandler

DistributedCacheProvider.key_prefix = redis_key_prefix


def set_up_pydiator_core():
    container = MediatrContainer()
    container.register_pipeline(LogPipeline())
    if cache_pipeline_is_active is True:
        cache_pipeline = CachePipeline(get_distributed_cache_provider())
        container.register_pipeline(cache_pipeline)

    # Service handlers mapping
    container.register_request(GetTodoAllRequest(), GetTodoAllHandler())
    container.register_request(GetTodoByIdRequest(), GetTodoByIdHandler())
    container.register_request(AddTodoRequest(), AddTodoHandler())
    container.register_request(UpdateTodoRequest(), UpdateTodoHandler())
    container.register_request(DeleteTodoByIdRequest(), DeleteTodoByIdHandler())

    # Data handlers mapping
    container.register_request(GetTodoAllDataRequest(), GetTodoAllDataHandler())
    container.register_request(GetTodoByIdDataRequest(), GetTodoByIdDataHandler())
    container.register_request(AddTodoDataRequest(), AddTodoDataHandler())
    container.register_request(DeleteTodoByIdDataRequest(), DeleteTodoByIdDataHandler())
    container.register_request(UpdateTodoDataRequest(), UpdateTodoDataHandler())

    # Notification mapping
    container.register_notification(TodoChangeNotification(), [TodoCacheRemoveNotificationHandler()])

    # Start
    pydiator.ready(container)
