from __future__ import annotations

from typing import Any

from importlib.resources import files
from io import BytesIO
import os
import pickle

import pandas as pd


def read_to_bytesio(path: str) -> BytesIO:
    """Reads file pre-packaged with SustainGym into a buffered IO stream.

    Args:
        path: path to file

    Returns: BytesIO
    """
    return BytesIO(files('sustaingym').joinpath(path).read_bytes())


def read_csv(csv_path: str, **kwargs: Any) -> pd.DataFrame:
    """Reads CSV data files pre-packaged with SustainGym.

    Args:
        csv_path: path to CSV, relative to main sustaingym package
        **kwargs: parameters to pass on to pd.read_csv()

    Returns: pd.DataFrame
    """
    bytesio = read_to_bytesio(csv_path)
    return pd.read_csv(bytesio, **kwargs)


def get_save_path(path: str) -> str:
    """Converts a relative path to a path within the SustainGym package.

    Creates intermediate directories as needed.

    This method may raise an Exception if the sustaingym package is not
    installed in a write-enabled directory.

    Args:
        path: path for saving file, relative to main sustaingym package
    """
    # sustaingym package
    basedir = os.path.dirname(os.path.dirname(__file__))

    # full path for saving CSV file
    full_path = os.path.join(basedir, path)

    # create directory for saving file if directory does not already exist
    full_path_dir = os.path.dirname(full_path)
    os.makedirs(full_path_dir, exist_ok=True)

    return full_path


def save_pickle(obj: Any, path: str) -> None:
    full_path = get_save_path(path)
    with open(full_path, 'wb') as f:
        pickle.dump(obj, f)


def to_csv(df: pd.DataFrame, path: str, **kwargs: Any) -> None:
    """Writes CSV data files to a path within the SustainGym package.

    This method may raise an Exception if the sustaingym package is not
    installed in a write-enabled directory.

    Args:
        df: DataFrame to save to disk
        path: path to save CSV, relative to main sustaingym package
        **kwargs: parameters to pass on to pd.to_csv()
    """
    full_path = get_save_path(path)

    # save the DataFrame
    df.to_csv(full_path, **kwargs)