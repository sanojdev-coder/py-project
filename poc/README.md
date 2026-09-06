# NORA Coverage Diagnostics POC

This folder contains a minimal Python proof-of-concept for the coverage diagnostics workflow.

## Workflow

1. Build a `CoverageDiagnosticsWorkflow` instance.
2. Validate the incoming `CoverageAssessmentReport`.
3. Run the report through a LangGraph `StateGraph` when LangGraph is installed, or a local fallback graph when it is not.
4. Fetch a local NORA coverage assessment stub.
5. Analyze the report through `RCAService` and `AzureOpenAIClient` in dual mode (live Azure call when configured, deterministic stub fallback otherwise).
6. Compose the response payload.
7. Return the `RCAAnalysisResult` to the caller.

The workflow exposes a `graph` attribute and a `run_langgraph` entrypoint. In this POC, the graph uses LangGraph when it is available and falls back to the local wrapper when it is not.

## Architecture

- `app/models` - shared contract models such as `CoverageAssessmentReport` and `RCAAnalysisResult`
- `app/services` - NORA client, RCA service, and response composer
- `app/mcp` - MCP tool schema and Azure OpenAI adapter
- `app/orchestrator` - static workflow orchestration
- `tests` - first failing tests for workflow behavior

### Python file mapping

- MCP tool schema: [poc/app/mcp/tool_schema.py](poc/app/mcp/tool_schema.py)
- Azure OpenAI adapter: [poc/app/mcp/azure_openai_client.py](poc/app/mcp/azure_openai_client.py)
- RCA integration update: [poc/app/services/rca_service.py](poc/app/services/rca_service.py)
- OpenAPI contract: [poc/openapi.yaml](poc/openapi.yaml)

## Key integration points

### NORA API
The NORA coverage assessment endpoint is treated as an upstream dependency. In the POC it is implemented as a local client stub, but the contract and payload are shaped to match a real external API contract.

### MCP tool layer
The RCA service does not call Azure OpenAI directly in the POC. It uses an MCP-style tool layer exposed via `CoverageAssessmentInput` and `RCAAnalysisToolResult` contracts.

### Azure OpenAI
The model integration is represented by `AzureOpenAIClient`, which now supports dual mode:

- Live mode: Uses Azure OpenAI chat completions when required environment variables are present and the OpenAI SDK is available.
- Stub mode: Returns deterministic structured RCA output when configuration is missing or if the live call fails.

Required environment variables for live mode:

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_DEPLOYMENT`
- `AZURE_OPENAI_API_VERSION` (optional override, default is `2024-02-01`)

## Run tests

```bash
cd D:\TMobile\py-project
set PYTHONPATH=D:\TMobile\py-project\poc
.\.venv\Scripts\python.exe -m pip install -r .\poc\requirements.txt
.\.venv\Scripts\python.exe -m pytest -q --rootdir="D:\TMobile\py-project\poc" --confcutdir="D:\TMobile\py-project\poc" .\tests
```

Expected baseline result in current environment:
- `4 passed, 1 skipped`

## Verified run modes (from poc folder)

Use these exact commands from `D:\TMobile\py-project\poc`.

### Mode 0: Run tests from repo root (user-verified)

Run this command from `D:\TMobile\py-project`:

```bash
.\.venv\Scripts\python.exe -m pytest -q --rootdir="D:\TMobile\py-project\poc" --confcutdir="D:\TMobile\py-project\poc" .\tests
```

Expected result in current environment:
- `4 passed, 1 skipped`

### Mode 1: Run full workflow tests

```bash
set PYTHONPATH=D:/TMobile/py-project/poc
../.venv/Scripts/python.exe -m pytest -q --rootdir=D:/TMobile/py-project/poc --confcutdir=D:/TMobile/py-project/poc ./tests/test_workflow.py -rs
```

### Mode 2: Run real LangGraph ON-mode test only

```bash
set PYTHONPATH=D:/TMobile/py-project/poc
../.venv/Scripts/python.exe -m pytest -q --rootdir=D:/TMobile/py-project/poc --confcutdir=D:/TMobile/py-project/poc ./tests/test_workflow.py -k test_workflow_runs_with_real_langgraph_mode_on -rs
```

### Optional: quick interpreter and StateGraph check

```bash
set PYTHONPATH=D:/TMobile/py-project/poc
../.venv/Scripts/python.exe -c "import sys, importlib.metadata as m; import app.orchestrator.workflow as w; print('python=', sys.executable); print('langgraph=', m.version('langgraph')); print('StateGraph_is_None=', w.StateGraph is None); print('StateGraph=', w.StateGraph)"
```

## Run with live Azure OpenAI

```bash
cd D:\TMobile\py-project\poc
set PYTHONPATH=D:\TMobile\py-project\poc
set AZURE_OPENAI_ENDPOINT=<your-endpoint>
set AZURE_OPENAI_API_KEY=<your-key>
set AZURE_OPENAI_DEPLOYMENT=<your-deployment>
set AZURE_OPENAI_API_VERSION=2024-02-01
python -m pytest -q tests\test_workflow.py
```

### Azure OpenAI setup checks

Use these commands from `D:\TMobile\py-project\poc` to verify the SDK, environment variables, and client mode before running live calls.

#### 1. Verify OpenAI SDK and AzureOpenAI support

```bash
.\.venv\Scripts\python.exe -c "import sys, openai; print('python=', sys.executable); print('openai=', openai.__file__); print('has_AzureOpenAI=', hasattr(openai, 'AzureOpenAI'))"
```

Expected result:
- `has_AzureOpenAI= True`

#### 2. Set Azure OpenAI environment variables in the current shell

```bash
set AZURE_OPENAI_ENDPOINT=<your-endpoint>
set AZURE_OPENAI_API_KEY=<your-key>
set AZURE_OPENAI_DEPLOYMENT=<your-deployment>
set AZURE_OPENAI_API_VERSION=2024-02-01
```

#### 3. Verify the environment variables are visible to the interpreter

```bash
.\.venv\Scripts\python.exe -c "import os; print('endpoint_set=', bool(os.getenv('AZURE_OPENAI_ENDPOINT'))); print('api_key_set=', bool(os.getenv('AZURE_OPENAI_API_KEY'))); print('deployment=', os.getenv('AZURE_OPENAI_DEPLOYMENT')); print('api_version=', os.getenv('AZURE_OPENAI_API_VERSION'))"
```

#### 4. Verify AzureOpenAIClient switches to live mode

```bash
.\.venv\Scripts\python.exe -c "from app.mcp.azure_openai_client import AzureOpenAIClient; client = AzureOpenAIClient(); print('live_mode=', client._azure_client is not None)"
```

Expected result:
- `live_mode= True`

## Troubleshooting

### 1. Stays in stub mode unexpectedly
Symptoms:
- Output remains deterministic across runs.
- Logs show AzureOpenAIClient initialized in stub mode.

Checks:
- Confirm AZURE_OPENAI_ENDPOINT is set and non-empty.
- Confirm AZURE_OPENAI_API_KEY is set and non-empty.
- Confirm AZURE_OPENAI_DEPLOYMENT is set and matches your deployed model name.
- Confirm the OpenAI SDK is installed in the same virtual environment used for execution.

### 2. Live call fails and falls back to stub
Symptoms:
- Logs show live call failed, then fallback result is returned.

Common causes:
- Endpoint URL is incorrect or uses the wrong Azure resource.
- API key is invalid or expired.
- Deployment name does not exist in the selected Azure OpenAI resource.
- API version is not supported by the deployed model.
- Corporate network or proxy blocks outbound calls.

### 3. LangGraph import or runtime issues
Symptoms:
- Workflow does not build a LangGraph-backed graph.

Checks:
- Install dependencies from requirements.txt.
- Run tests from the poc folder and set PYTHONPATH to the poc path.
- Ensure the same interpreter is used for both install and test commands.

### 4. Import path problems in tests
Symptoms:
- ModuleNotFoundError for app.orchestrator or related app packages.

Fix:
- Run from D:\TMobile\py-project\poc.
- Set PYTHONPATH to D:\TMobile\py-project\poc before running pytest.

### 5. Non-JSON model output in live mode
Symptoms:
- JSON parsing fails in the AzureOpenAIClient response handling.

Fix options:
- Strengthen system prompt constraints for JSON-only output.
- Add a response_format setting when using a model/API version that supports it.
- Add defensive parsing and schema validation with actionable log messages.

## Next steps in POC is to add the MCP Adapter

The next step is to tune prompt/response validation for production quality and expand tests to cover live-mode parsing and fallback behavior.

### Recommended order
1. Install the Python dependencies in requirements.txt
2. Run the first tests in test_workflow.py
3. Confirm workflow tests pass in stub mode
4. Add environment variables for live mode:
   - AZURE_OPENAI_ENDPOINT
   - AZURE_OPENAI_API_KEY
   - AZURE_OPENAI_DEPLOYMENT
   - AZURE_OPENAI_API_VERSION
5. Validate one end-to-end happy path locally in live mode
6. Add tests that intentionally force fallback mode (missing config or live-call error)

### Minimal command sequence
```bash
cd D:\TMobile\py-project\poc
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest -q
```

### Then add the real LLM adapter
The actual integration point is:
- azure_openai_client.py

That is where live-mode request/response handling and stub fallback behavior are implemented.

> The most important next change is expanding live-mode validation and hardening response parsing for production scenarios.

If you want, I can do the next exact step and move the POC from stubbed logic to a real Azure OpenAI integration skeleton with environment config and test coverage.