#!/bin/bash
# 恢复脚本：在新 VPS 上从备份包快速恢复服务
# 用法：bash restore.sh <备份文件路径>
# 示例：bash restore.sh saveany_backup_20260416_120000.tar.gz

set -e

BACKUP_FILE="$1"

if [ -z "$BACKUP_FILE" ]; then
  echo "用法：bash restore.sh <备份文件路径>"
  exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
  echo "错误：备份文件不存在：$BACKUP_FILE"
  exit 1
fi

echo "=== SaveAny 恢复开始 ==="

# 1. 安装系统依赖
echo "[1/5] 安装系统依赖..."
apt update -qq
apt install -y python3 python3-pip python3-venv git ffmpeg nginx certbot python3-certbot-nginx

# 2. 解压备份
echo "[2/5] 解压备份文件..."
mkdir -p /opt
tar -xzf "$BACKUP_FILE" -C /opt
echo "解压完成"

# 3. 重建虚拟环境
echo "[3/5] 安装 Python 依赖..."
python3 -m venv /opt/saveany/venv
/opt/saveany/venv/bin/pip install -q --upgrade pip
/opt/saveany/venv/bin/pip install -q -r /opt/saveany/backend/requirements.txt
echo "依赖安装完成"

# 4. 注册 systemd 服务
echo "[4/5] 注册系统服务..."
cp /opt/saveany/backend/saveany.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable saveany
systemctl start saveany
sleep 2
systemctl status saveany --no-pager

# 5. 恢复 Nginx 配置（如果存在）
echo "[5/5] 检查 Nginx 配置..."
if [ -f "/opt/saveany/backend/scripts/nginx.conf" ]; then
  cp /opt/saveany/backend/scripts/nginx.conf /etc/nginx/sites-available/saveany
  ln -sf /etc/nginx/sites-available/saveany /etc/nginx/sites-enabled/saveany
  nginx -t && systemctl reload nginx
  echo "Nginx 配置已恢复"
else
  echo "未找到 Nginx 配置，请手动配置（见 README）"
fi

echo ""
echo "=== 恢复完成 ==="
echo "请检查 /opt/saveany/backend/.env 中的配置是否正确"
echo "如需更新 ALLOWED_ORIGINS，修改后执行：systemctl restart saveany"
