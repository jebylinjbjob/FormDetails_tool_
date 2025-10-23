# JSON 檔案處理工具

這是一個用於處理和合併 JSON 檔案的 Python 工具集，特別針對表單設計的 JSON 結構進行優化。

## 📁 專案結構

```
fromdetil/
├── add/                    # 輸入資料夾 - 放置需要處理的原始JSON檔案
│   └── .json
├── out/                    # 輸出資料夾 - 存放處理後的JSON檔案
│   └── .json
├── append_json.json        # 要合併的JSON資料
├── merge_json.py           # JSON合併腳本
├── optimized_process_json.py  # C#類別結構優化腳本
└── README.md               # 說明文件
```

## 🚀 功能說明

### 1. JSON 合併功能 (`merge_json.py`)

將 `append_json.json` 中的內容自動合併到 `add/` 資料夾中所有 JSON 檔案的 `formFields` 陣列中。

**主要功能：**

- 自動掃描 `add/` 資料夾中的所有 JSON 檔案
- 讀取 `append_json.json` 中的 formFields 資料
- 將新增的 formFields 合併到原有陣列中
- 儲存合併結果到 `out/` 資料夾

**使用方式：**

```bash
python merge_json.py
```

### 2. C#類別結構優化 (`optimized_process_json.py`)

針對 C# FormDetail 類別結構進行 JSON 資料優化處理。

**主要功能：**

- 確保 JSON 結構符合 C#類別定義
- 移除空值欄位，避免序列化錯誤
- 處理擴展資料（ExtensionData）
- 資料類型一致性檢查

**使用方式：**

```bash
python optimized_process_json.py
```

## 📋 支援的 C#類別結構

```csharp
public class FormDetail
{
    public List<Form> Forms { get; set; }
}

public class Form
{
    public string FormId { get; set; }
    public string FormName { get; set; }
    public string Description { get; set; }
    public List<FormField> FormFields { get; set; }
    public List<FieldGroup> FieldGroups { get; set; }
}

public class FormField
{
    public string FormFieldId { get; set; }
    public string FieldName { get; set; }
    public string FieldType { get; set; }
    public JsonElement DefaultValue { get; set; }
    public bool IsReadonly { get; set; }
    public bool IsVisible { get; set; }
    public RelatedSource? RelatedSource { get; set; }
    public List<FieldOptions>? FieldOptions { get; set; }
    public string? FieldGroup { get; set; }
    public string? ParentField { get; set; }
    public JsonElement DisplayCondition { get; set; }
    public bool InfoDisplayCondition { get; set; }
    public string? RelatedFormsExtend { get; set; }
    public Guid? FlowNodeCode { get; set; }
    public int Sort { get; set; }
    public string SpecialFieldCode { get; set; }

    // 用於存儲未知屬性的字典
    [JsonExtensionData] public Dictionary<string, JsonElement>? ExtensionData { get; set; }
}
```

## 🔧 使用流程

### 基本合併流程

1. **準備資料**

   - 將需要處理的 JSON 檔案放入 `add/` 資料夾
   - 準備要合併的 formFields 資料在 `append_json.json` 中

2. **執行合併**

   ```bash
   python merge_json.py
   ```

3. **檢查結果**
   - 處理後的檔案會出現在 `out/` 資料夾中
   - 檔案名稱保持不變

### C#優化流程

1. **執行優化處理**

   ```bash
   python optimized_process_json.py
   ```

2. **驗證結果**
   - 檢查 `out/` 資料夾中的檔案是否符合 C#類別結構
   - 確保可以正常進行 `JsonSerializer.Deserialize<FormDetail>()`

## 📊 處理範例

### 原始資料 (`add/削價單.json`)

```json
{
  "forms": [
    {
      "formFields": [
        {
          "fieldName": "emp",
          "fieldType": "dxTextBox",
          "isReadonly": true,
          "isVisible": false
        }
      ]
    }
  ]
}
```

### 合併資料 (`append_json.json`)

```json
{
  "fieldName": "直、間接人員 (隱藏)",
  "fieldType": "dxTextBox",
  "isReadonly": true,
  "isVisible": false,
  "specialFieldCode": "983"
}
```

### 處理結果 (`out/削價單.json`)

```json
{
  "forms": [
    {
      "formFields": [
        {
          "fieldName": "emp",
          "fieldType": "dxTextBox",
          "isReadonly": true,
          "isVisible": false
        },
        {
          "fieldName": "直、間接人員 (隱藏)",
          "fieldType": "dxTextBox",
          "isReadonly": true,
          "isVisible": false,
          "specialFieldCode": "983"
        }
      ]
    }
  ]
}
```

## ⚙️ 系統需求

- Python 3.6+
- 無需額外套件依賴

## 🛠️ 開發環境設定

### 安裝開發依賴

```bash
# 使用 pip
pip install -e ".[dev]"

# 或使用 requirements-dev.txt
pip install -r requirements-dev.txt

# 或使用 Makefile
make install-dev
```

### 程式碼風格檢查工具

本專案使用以下工具來確保程式碼品質：

- **Ruff**: 快速的 Python linter 和格式化工具
- **Black**: Python 程式碼格式化工具
- **isort**: import 語句排序工具
- **MyPy**: 靜態類型檢查工具
- **Pre-commit**: Git hooks 管理工具

### 使用 Pre-commit Hooks

```bash
# 安裝 pre-commit hooks
pre-commit install

# 手動執行所有檢查
pre-commit run --all-files

# 或使用 Makefile
make pre-commit-install
make pre-commit-run
```

### 手動執行程式碼檢查

```bash
# 檢查程式碼風格
make lint

# 格式化程式碼
make format

# 檢查格式（不修改檔案）
make format-check

# 執行所有檢查
make check

# 執行測試
make test

# 執行安全性檢查
make security

# 執行完整的 CI 檢查
make ci
```

### GitHub Actions CI

專案已設定 GitHub Actions CI 工作流程，會在以下情況自動執行：

- Push 到 `main` 或 `develop` 分支
- 建立 Pull Request 到 `main` 或 `develop` 分支

CI 工作流程包含：

1. **程式碼風格檢查與格式化** - 使用 Ruff、Black、isort、MyPy
2. **測試** - 使用 pytest 執行測試並產生覆蓋率報告
3. **安全性檢查** - 使用 Safety 和 Bandit 檢查安全性問題

### 開發工作流程

1. **Fork 專案並建立分支**
2. **安裝開發依賴**: `make install-dev`
3. **安裝 pre-commit hooks**: `make pre-commit-install`
4. **進行開發並提交變更**
5. **確保所有檢查通過**: `make ci`
6. **建立 Pull Request**

## 📝 日誌記錄

腳本執行時會產生詳細的日誌記錄：

- `merge_json.log` - 合併腳本執行日誌
- `process_json.log` - 處理腳本執行日誌

## 🛡️ 錯誤處理

- JSON 解析錯誤處理
- 檔案不存在檢查
- 資料夾自動創建
- 詳細的錯誤訊息和日誌記錄

## License

MIT License

Copyright (c) 2025 jebylinjbjob

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

---
