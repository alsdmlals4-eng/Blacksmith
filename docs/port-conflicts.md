# Port 8000 is in use by another process

Godot AI's Python server listens on HTTP port `8000` and WebSocket port `9500`. Port `8000` is a popular default for Django, `python -m http.server`, and other local development tools, so a foreign process may already occupy it.

When a **non-Godot-AI** process is bound to `8000`, the dock cannot reclaim the port because it cannot prove ownership. It stops and displays a message similar to:

> Port 8000 is occupied by an incompatible server. Port 8001 is free — set `godot_ai/http_port` in Editor Settings, then update your client config.

If the dock offers **Restart Server**, the occupant is an older Godot AI server that can be reclaimed. Use Restart Server instead of changing ports.

## 1. Pick free ports

The plugin uses two ports:

- HTTP `8000`: MCP clients connect here.
- WebSocket `9500`: the Python server and Godot editor communicate here.

The crash panel suggests free values such as HTTP `8001` and WebSocket `9501`. On Windows the suggestions are checked against Hyper-V, WSL2, and Docker reservation ranges.

## 2. Change the Editor Settings

1. Open **Editor → Editor Settings** in Godot.
2. Search for `godot_ai/http_port` and set the suggested free HTTP port.
3. Search for `godot_ai/ws_port` and set the suggested free WebSocket port.
4. Reload the plugin from **Project → Project Settings → Plugins**, or restart Godot.

These are Editor Settings, not project settings. They apply to every project opened by that editor installation.

## 3. Reconfigure MCP clients

Changing Editor Settings moves the server, but clients still point to the previous URL. In the Godot AI dock, click **Configure** for each client or **Configure all** to rewrite the client configuration with the current server URL.

For a manually configured Claude Code client, an example is:

```bash
claude mcp remove godot-ai
claude mcp add --scope user --transport http godot-ai http://127.0.0.1:8001/mcp
```

For config-file clients such as Codex, Grok Build, Antigravity, or Cursor, update the `url` or `serverUrl` field to the new port. The integrated plugin overview is at [`addons/godot_ai/README.md`](../addons/godot_ai/README.md), and the full upstream documentation is maintained in the Godot AI repository.

## Reverting

When the conflicting process is gone, set `godot_ai/http_port` back to `8000` and `godot_ai/ws_port` back to `9500`, reload the plugin, and run **Configure all** again.
