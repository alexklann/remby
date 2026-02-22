# remby

A modern, fully-typed Python API wrapper for Emby Server. 

Built with Pydantic V2 and HTTPX, `remby` provides strict type hinting, automatic JSON validation and a clean interface for interacting with your Emby media server.

## Features
* **Fully Typed:** Autocomplete and type-checking out of the box.
* **Modern HTTP:** Built on `httpx` for robust, thread-safe network requests.
* **Pydantic V2 Models:** API responses are automatically parsed into strictly typed Python objects.
* **Context Manager Support:** Safely manage connection pooling using `with` blocks.

## Installation

`remby` is currently in active alpha development.  
You can install it directly from the Codeberg package registry.

Using `uv` (Recommended):
```bash
uv add remby --extra-index-url "https://codeberg.org/api/packages/klann/pypi/simple"
```

Using `pip`:
```bash
pip install remby --extra-index-url "https://codeberg.org/api/packages/klann/pypi/simple"
```

## Quick Start
```py
from remby import EmbyClient

# Initialize the client using a context manager
with EmbyClient(base_url="http://localhost:8096", api_key="YOUR_API_KEY") as client:
    
    # Check if the server is alive
    is_online = client.system.check_system_ping_head()
    print(f"Server online: {is_online}")

    # Fetch server info (returns a strictly typed Pydantic model)
    info = client.system.get_system_info()
    print(f"Connected to Emby Server v{info.version}")
```

## Currently Supported Endpoints
- `/System`: Server info, logs, restarting and pings (100%)

## Development

This project uses `uv` for dependency management and `pytest` for testing.

```bash
# Clone the repository
git clone [https://codeberg.org/klann/remby.git](https://codeberg.org/klann/remby.git)
cd remby

# Run the test suite
uv run pytest
```

## License
This project uses a `GPL-3.0-or-later` license.  
For more information see `LICENSE`.