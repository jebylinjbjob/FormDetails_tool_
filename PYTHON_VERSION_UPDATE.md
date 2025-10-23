# Python 版本更新摘要

## 🔄 問題解決

您遇到的 GitHub Actions 錯誤是因為 Ubuntu 24.04 不再支援 Python 3.6。已成功修正所有相關配置檔案。

## 📝 更新內容

### 1. GitHub Actions CI 工作流程 (`.github/workflows/ci.yml`)

- **移除**: Python 3.6
- **保留**: Python 3.7, 3.8, 3.9, 3.10, 3.11, 3.12
- **影響**: `lint-and-format` 和 `test` 任務的 matrix 策略

### 2. 專案配置檔案 (`pyproject.toml`)

- **最低版本要求**: `>=3.6` → `>=3.7`
- **Ruff 目標版本**: `py36` → `py37`
- **Black 目標版本**: `['py36']` → `['py37']`
- **MyPy Python 版本**: `3.6` → `3.7`
- **分類標籤**: 移除 Python 3.6 相關標籤

### 3. 文檔更新

- **README.md**: 系統需求從 "Python 3.6+" 改為 "Python 3.7+"
- **README.md**: 新增支援的 Python 版本清單
- **setup_dev.py**: 版本檢查從 3.6 改為 3.7
- **CODE_QUALITY_SETUP.md**: 更新支援版本清單並新增說明

### 4. Markdown 格式修正

- **README.md**: 修正程式碼區塊語言標記，解決 MD040 警告

## ✅ 修正結果

現在您的 CI 工作流程將：

1. **成功執行** - 不再出現 Python 3.6 找不到的錯誤
2. **支援現代版本** - 測試 Python 3.7-3.12 版本
3. **保持相容性** - 專案仍可在 Python 3.7+ 環境中正常運行
4. **符合最佳實踐** - 使用目前 GitHub Actions 支援的 Python 版本

## 🚀 下一步

您的 CI 工作流程現在應該可以正常執行。如果您需要測試，可以：

1. 提交這些變更到 GitHub
2. 建立 Pull Request 觸發 CI
3. 或直接 Push 到 main/develop 分支

所有程式碼風格檢查工具現在都配置為支援 Python 3.7+ 版本！
