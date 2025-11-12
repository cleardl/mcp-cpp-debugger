# MCP Debugger

基于MCP协议的C++调试器，为AI大模型提供调试C++程序的能力。

## 快速开始

### 1. 安装依赖

**安装 uv 包管理器：**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**安装项目依赖：**
```bash
uv sync
uv pip install -e .
```

### 2. 启动MCP服务器

```powershell
./mcp-cpp-debugger.exe
```

或使用Python直接运行：
```bash
python -m mcp_cpp_debugger.mcp.server
```

### 3. 配置MCP客户端

在MCP客户端（Claude CLI / Cursor / VS Code Copilot / Visual Studio）中添加配置：

```json
{
  "mcpServers": {
    "mcp-cpp-debugger": {
      "url": "http://localhost:8999/sse/"
    }
  }
}
```

**以Cursor为例：**

在MCP配置中添加后，启动mcp-cpp-debugger服务即可使用：

### 4. 开始调试

在对话中直接向AI描述调试需求，AI将自动调用调试器完成操作。
