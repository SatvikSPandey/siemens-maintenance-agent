from langgraph.checkpoint.memory import MemorySaver
from config import CHECKPOINT_DB_PATH


def get_checkpointer():
    return MemorySaver()