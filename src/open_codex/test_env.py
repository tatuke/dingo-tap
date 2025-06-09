from dotenv import load_dotenv
import os

# 1. 获取脚本目录
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, "resources", ".env") 

# 2. 调试路径
print(f"Script directory: {script_dir}")
print(f"Dotenv path: {dotenv_path}")
print(f"File exists? {os.path.exists(dotenv_path)}")

# 3. 加载环境变量
load_dotenv(dotenv_path=dotenv_path)

# 4. 验证环境变量
print("Environment variables after loading:")
print(os.environ)

# 5. 使用环境变量
try:
    model_name = os.environ['MODEL_NAME']
    print(f"MODEL_NAME: {model_name}")
except KeyError as e:
    print(f"Missing environment variable: {e}")