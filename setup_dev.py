# 開發環境快速設定腳本
# 使用方式：python setup_dev.py

import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """執行命令並顯示結果"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 完成")
        if result.stdout:
            print(f"輸出: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失敗")
        print(f"錯誤: {e.stderr}")
        return False
    return True


def main():
    """主函數"""
    print("🚀 開始設定 FormDetails Tool 開發環境...")
    print("=" * 60)

    # 檢查 Python 版本
    python_version = sys.version_info
    print(f"Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")

    if python_version < (3, 8):
        print("❌ 需要 Python 3.8 或更高版本")
        sys.exit(1)

    # 安裝開發依賴
    commands = [
        ("pip install --upgrade pip", "升級 pip"),
        ("pip install -e .", "安裝專案依賴"),
        ("pip install -r requirements-dev.txt", "安裝開發依賴"),
        ("pre-commit install", "安裝 pre-commit hooks"),
    ]

    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1

    print("\n" + "=" * 60)
    print(f"設定完成！成功執行 {success_count}/{len(commands)} 個步驟")

    if success_count == len(commands):
        print("\n🎉 開發環境設定完成！")
        print("\n可用的命令：")
        print("  make help          - 顯示所有可用命令")
        print("  make lint          - 執行程式碼檢查")
        print("  make format        - 格式化程式碼")
        print("  make test          - 執行測試")
        print("  make ci            - 執行完整 CI 檢查")
        print("  pre-commit run --all-files  - 執行所有 pre-commit 檢查")
    else:
        print("\n⚠️  部分步驟失敗，請檢查錯誤訊息並手動執行失敗的命令")


if __name__ == "__main__":
    main()
