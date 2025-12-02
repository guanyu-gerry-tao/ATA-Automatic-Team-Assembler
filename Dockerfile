FROM python:3.13

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# 确保脚本有执行权限并修复可能的行尾符问题
RUN chmod +x /app/docker-entrypoint.sh && \
    sed -i 's/\r$//' /app/docker-entrypoint.sh 2>/dev/null || true

EXPOSE 8000

# 使用 sh 来执行脚本，避免权限问题
ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]