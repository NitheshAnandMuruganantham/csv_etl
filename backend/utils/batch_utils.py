import math
from loguru import logger
import psutil


def calculate_batch_count(len_df):
    if len_df < 10000:
        batch_size = len_df
    else:
        batch_size = 10000

    return batch_size
