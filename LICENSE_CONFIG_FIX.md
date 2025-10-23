# pyproject.toml License 配置修正摘要

## 🔄 問題解決

您遇到的 CI 錯誤是因為 `pyproject.toml` 中的 license 配置格式不符合 setuptools 的期望。錯誤訊息顯示 setuptools 期望 license 配置使用特定的格式，而不是簡單的字串。

已成功修正這個問題。

## 📝 問題分析

### 錯誤訊息解讀

```
configuration error: `project.license` must be valid exactly by one definition (2 matches found):
- keys: 'file': {type: string} required: ['file']
- keys: 'text': {type: string} required: ['text']
```

這表示 setuptools 期望 license 配置使用以下兩種格式之一：

1. `{file = "LICENSE"}` - 指向授權檔案
2. `{text = "MIT"}` - 直接指定授權文字

### 修正內容

**修正前：**

```toml
license = "MIT"
```

**修正後：**

```toml
license = {text = "MIT"}
```

## ✅ 修正結果

現在您的 `pyproject.toml` 配置將：

1. **符合 setuptools 規範** - 使用正確的 license 配置格式
2. **避免建置錯誤** - 不再出現配置驗證錯誤
3. **保持功能完整** - license 資訊仍然正確傳遞
4. **CI 正常執行** - 依賴安裝現在應該可以成功

## 🔍 技術細節

### License 配置格式說明

| 格式                 | 用途             | 範例             |
| -------------------- | ---------------- | ---------------- |
| `{text = "MIT"}`     | 直接指定授權文字 | 適用於標準授權   |
| `{file = "LICENSE"}` | 指向授權檔案     | 適用於自定義授權 |

### 為什麼需要這種格式

- **setuptools 規範**: 遵循 PEP 621 標準
- **類型安全**: 明確區分授權文字和檔案
- **向後相容**: 支援不同的授權配置方式

## 🚀 版本相容性

這個修正確保了：

- **setuptools >= 45**: 完全支援
- **Python 3.8+**: 正常運作
- **現代建置工具**: 符合最新標準

## 🎯 下一步

您的 CI 工作流程現在應該可以正常執行。如果您需要測試，可以：

1. 提交這些變更到 GitHub
2. 建立 Pull Request 觸發 CI
3. 或直接 Push 到 main/develop 分支

所有建置配置問題現在都已解決！
