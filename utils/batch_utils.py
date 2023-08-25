import math
from loguru import logger
import psutil


def calculate_batch_count(len_df):
    if len_df < 10000:
        batch_size = len_df
    elif len_df > 100000 and len_df <= 1000000:
        batch_size = 100000
    elif len_df > 1000000:
        batch_size = 1000000
    else:
        batch_size = 10000

    return batch_size
