import os
import sys
import alibabacloud_oss_v2 as oss

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# 从配置文件获取OSS配置
region = config.OSS_REGION
endpoint = config.OSS_ENDPOINT
bucket_name = config.OSS_BUCKET_NAME
object_key = 'test.png'  # 上传后 OSS 上的文件名
local_file_path = r'tmp\changebg\test.png'  # 本地文件路径

# 初始化 OSS 客户端
cfg = oss.config.load_default()
cfg.region = region
cfg.endpoint = endpoint
cfg.credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
client = oss.Client(cfg)

# 读取并上传文件
with open(local_file_path, 'rb') as f:
    data = f.read()

client.put_object(oss.PutObjectRequest(
    bucket=bucket_name,
    key=object_key,
    body=data
))

# 构造公网 URL（前提：bucket 是公共读或配置了临时授权）
public_url = f"https://{bucket_name}.{endpoint.replace('https://', '')}/{object_key}"
print(f"文件上传成功，公网访问地址：{public_url}")
