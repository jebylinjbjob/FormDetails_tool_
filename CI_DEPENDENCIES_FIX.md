# CI 依賴安裝問題修正摘要

## 🔄 問題解決

您遇到的 CI 錯誤是因為 pytest 模組沒有被正確安裝。問題出現在 `pyproject.toml` 的 `dev` 依賴配置不完整，以及 CI 工作流程中安全性檢查任務的依賴安裝方式不一致。

已成功修正這些問題。

## 📝 修正內容

### 1. pyproject.toml 依賴更新

**修正前：**

```toml
[project.optional-dependencies]
dev = [
    "ruff>=0.1.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
]
```

**修正後：**

```toml
[project.optional-dependencies]
dev = [
    "ruff>=0.1.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.10.0",
    "safety>=2.0.0",
    "bandit>=1.7.0",
]
```

### 2. CI 工作流程一致性修正

**修正前 (安全性檢查任務)：**

```yaml
- name: 安裝依賴
  run: |
    python -m pip install --upgrade pip
    pip install safety bandit
```

**修正後：**

```yaml
- name: 安裝依賴
  run: |
    python -m pip install --upgrade pip
    pip install -e ".[dev]"
```

### 3. 新增的測試依賴

| 套件          | 版本     | 用途             |
| ------------- | -------- | ---------------- |
| `pytest`      | >=7.0.0  | 測試框架         |
| `pytest-cov`  | >=4.0.0  | 覆蓋率報告       |
| `pytest-mock` | >=3.10.0 | Mock 支援        |
| `safety`      | >=2.0.0  | 依賴安全性檢查   |
| `bandit`      | >=1.7.0  | 程式碼安全性檢查 |

## ✅ 修正結果

現在您的 CI 工作流程將：

1. **正確安裝測試依賴** - pytest 和相關套件會被正確安裝
2. **統一的依賴管理** - 所有任務都使用 `pip install -e ".[dev]"`
3. **完整的測試環境** - 包含覆蓋率報告和 Mock 支援
4. **一致的安全性檢查** - 使用相同的依賴安裝方式

## 🔍 技術細節

### 依賴管理策略

- **統一安裝**: 所有 CI 任務都使用 `pip install -e ".[dev]"`
- **版本控制**: 明確指定最低版本要求
- **功能完整**: 包含測試、覆蓋率、安全性檢查所需的所有套件

### CI 任務依賴對應

| CI 任務         | 所需依賴                        | 安裝方式                  |
| --------------- | ------------------------------- | ------------------------- |
| lint-and-format | ruff, black, isort, mypy        | `pip install -e ".[dev]"` |
| test            | pytest, pytest-cov, pytest-mock | `pip install -e ".[dev]"` |
| security        | safety, bandit                  | `pip install -e ".[dev]"` |

## 🚀 下一步

您的 CI 工作流程現在應該可以正常執行。如果您需要測試，可以：

1. 提交這些變更到 GitHub
2. 建立 Pull Request 觸發 CI
3. 或直接 Push 到 main/develop 分支

所有依賴安裝問題現在都已解決！
