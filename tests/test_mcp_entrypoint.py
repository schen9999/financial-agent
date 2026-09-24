"""financial-agent-mcp entrypoint: transport selection semantics."""
import mcp_server


def test_main_is_the_declared_console_entrypoint():
    assert callable(mcp_server.main)


def test_http_flag_wins(monkeypatch):
    monkeypatch.setenv("MCP_TRANSPORT", "sse")
    assert mcp_server._select_transport(True) == "streamable-http"


def test_env_preserved_without_flag(monkeypatch):
    # The K8s deployment relies on exactly this: env var, no flags.
    monkeypatch.setenv("MCP_TRANSPORT", "streamable-http")
    assert mcp_server._select_transport(False) == "streamable-http"
    monkeypatch.delenv("MCP_TRANSPORT", raising=False)
    assert mcp_server._select_transport(False) == "stdio"
