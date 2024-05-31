# 使用官方的Python运行时作为父镜像
FROM python:3.9-slim-buster

# 设置工作目录
WORKDIR /app

# 将requirements.txt复制到容器中
COPY requirements.txt .

# 安装任何需要的包
RUN pip install --no-cache-dir -r requirements.txt

# 将项目的所有文件复制到容器中
COPY . .

# 设置环境变量
ENV DJANGO_SETTINGS_MODULE=Litma.settings

# 开放端口
EXPOSE 8000

# 定义运行命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
