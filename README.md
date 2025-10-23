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

## 📝 日誌記錄

腳本執行時會產生詳細的日誌記錄：

- `merge_json.log` - 合併腳本執行日誌
- `process_json.log` - 處理腳本執行日誌

## 🛡️ 錯誤處理

- JSON 解析錯誤處理
- 檔案不存在檢查
- 資料夾自動創建
- 詳細的錯誤訊息和日誌記錄

## 📞 支援

如有問題或建議，請檢查日誌檔案或聯繫開發團隊。

---
