import datetime
import json
import os

DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def data_dir():
    """Resolve DATA_DIR at call time, so .env loaded by main.py is respected."""
    return os.getenv("DATA_DIR") or DEFAULT_DATA_DIR


def _path(source):
    return os.path.join(data_dir(), f"rates_{source}.json")


def read_data(source):
    """Return (last_value, last_updated) for a source, or (None, None) if unavailable."""
    path = _path(source)
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)
    except FileNotFoundError:
        return None, None
    except (json.JSONDecodeError, OSError) as e:
        print(f"Kunne ikke lese {path}: {e}")
        return None, None

    return content.get("last_value"), content.get("last_updated")


def write_data(source, new_value):
    """Persist the latest value for a source with the current timestamp."""
    path = _path(source)
    os.makedirs(data_dir(), exist_ok=True)
    payload = {
        "last_value": new_value,
        "last_updated": datetime.datetime.now().isoformat(),
    }
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4)
    os.replace(tmp_path, path)
    print(f"write_data {source}: {payload}")
