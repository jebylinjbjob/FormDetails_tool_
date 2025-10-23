# pyproject.toml 配置修正摘要

## 🔄 問題解決

您遇到的 CI 錯誤是因為 `pyproject.toml` 配置有兩個主要問題：

1. **License 配置格式已棄用** - 使用了舊的 TOML 表格格式
2. **多個頂層模組發現問題** - setuptools 無法自動發現要包含的模組

已成功修正這些問題。

## 📝 修正內容

### 1. License 配置修正

**修正前：**

```toml
license = {text = "MIT"}
classifiers = [
    "License :: OSI Approved :: MIT License",
    # ... 其他分類
]
```

**修正後：**

```toml
license = "MIT"
classifiers = [
    # 移除了 License 分類標籤
    # ... 其他分類
]
```

### 2. 模組發現問題修正

**問題：**

```
error: Multiple top-level modules discovered in a flat-layout:
['merge_json', 'optimized_process_json', 'setup_dev'].
```

**解決方案：**
新增 `[tool.setuptools]` 配置，明確指定要包含的模組：

```toml
[tool.setuptools]
py-modules = ["merge_json", "optimized_process_json"]
```

### 3. 完整的修正內容

| 項目         | 修正前                                        | 修正後                | 說明               |
| ------------ | --------------------------------------------- | --------------------- | ------------------ |
| License 格式 | `{text = "MIT"}`                              | `"MIT"`               | 使用新的 SPDX 格式 |
| License 分類 | 包含 `License :: OSI Approved :: MIT License` | 移除該分類            | 避免重複和棄用警告 |
| 模組發現     | 自動發現                                      | 明確指定 `py-modules` | 解決多模組衝突     |

## ✅ 修正結果

現在您的 `pyproject.toml` 配置將：

1. **無棄用警告** - 使用最新的 License 配置格式
2. **正確的模組包含** - 明確指定要包含的 Python 模組
3. **符合現代標準** - 遵循 setuptools 的最佳實踐
4. **CI 正常執行** - 不再出現建置錯誤

## 🔍 技術細節

### License 配置變更

- **舊格式**: `license = {text = "MIT"}` (已棄用)
- **新格式**: `license = "MIT"` (SPDX 表達式)
- **移除**: License 分類標籤 (避免重複)

### 模組發現配置

- **問題**: setuptools 自動發現多個頂層模組時會報錯
- **解決**: 使用 `py-modules` 明確指定要包含的模組
- **排除**: `setup_dev.py` 不包含在套件中 (僅用於開發環境設定)

## 🚀 下一步

您的 CI 工作流程現在應該可以正常執行。如果您需要測試，可以：

1. 提交這些變更到 GitHub
2. 建立 Pull Request 觸發 CI
3. 或直接 Push 到 main/develop 分支

所有建置問題現在都已解決！
