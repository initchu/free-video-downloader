#!/bin/bash
# 备份脚本：打包应用数据和配置，上传到 Google Cloud Storage（可选）
# 用法：bash backup.sh

set -e

APP_DIR="/opt/saveany"
BACKUP_DIR="/opt/saveany-backups"
LOG_FILE="${BACKUP_DIR}/backup.log"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="saveany_backup_${TIMESTAMP}.tar.gz"

echo "=== SaveAny 备份开始 ==="

mkdir -p "$BACKUP_DIR"
exec >> "$LOG_FILE" 2>&1

# 打包：代码 + .env + 数据库
tar -czf "${BACKUP_DIR}/${BACKUP_FILE}" \
  -C /opt \
  --exclude="saveany/venv" \
  --exclude="saveany/backend/downloads" \
  --exclude="saveany/.git" \
  saveany

echo "备份文件：${BACKUP_DIR}/${BACKUP_FILE}"
echo "文件大小：$(du -sh ${BACKUP_DIR}/${BACKUP_FILE} | cut -f1)"

# 可选：上传到 GCS（需要 gcloud 已登录）
# GCS_BUCKET="gs://your-bucket-name/saveany-backups"
# gcloud storage cp "${BACKUP_DIR}/${BACKUP_FILE}" "${GCS_BUCKET}/"
# echo "已上传到 ${GCS_BUCKET}"

# 保留最近 7 个备份，删除旧的
cd "$BACKUP_DIR"
ls -t saveany_backup_*.tar.gz | tail -n +8 | xargs -r rm --
echo "旧备份已清理，当前保留："
ls -lh saveany_backup_*.tar.gz

echo "=== 备份完成 ==="
