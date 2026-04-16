# SaveAny 部署指南

后端部署在谷歌云 VPS，前端部署在 Cloudflare Pages。

---

## 前置要求

- VPS：Python >= 3.10，ffmpeg 已安装
- 本地：Node.js >= 18，Git

---

## 一、后端部署（谷歌云 VPS）

**1. 克隆代码**

```bash
git clone <your-repo> /opt/saveany
cd /opt/saveany/backend
```

**2. 创建虚拟环境并安装依赖**

```bash
python3 -m venv /opt/saveany/venv
/opt/saveany/venv/bin/pip install -r requirements.txt
```

**3. 配置环境变量**

```bash
cp .env.example .env
vim .env
```

填入以下内容：

```env
DEEPSEEK_API_KEY=sk-你的key
JWT_SECRET=随机强密码字符串

# Stripe 支付（可选）
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_PRICE_ID_MONTHLY=price_xxx

# 前端域名（Cloudflare Pages 部署完成后填入）
FRONTEND_URL=https://yourapp.pages.dev
ALLOWED_ORIGINS=https://yourapp.pages.dev
```

**4. 注册 systemd 服务**

```bash
sudo cp saveany.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable saveany
sudo systemctl start saveany

# 查看运行状态
sudo systemctl status saveany
```

**5. 配置防火墙**

在 GCP 控制台 → VPC 网络 → 防火墙规则，放行 TCP 8000 端口。

推荐在 8000 前加一层 Nginx 反代并配置 HTTPS，将 `https://api.yourdomain.com` 代理到 `localhost:8000`。

---

## 二、前端部署（Cloudflare Pages）

**1. 在 Cloudflare Pages 控制台新建项目**

连接你的 Git 仓库，配置构建参数：

| 配置项 | 值 |
|---|---|
| 根目录 | `frontend` |
| 构建命令 | `npm run build` |
| 输出目录 | `dist` |

**2. 添加环境变量**

在 Pages 项目 → 设置 → 环境变量中添加：

| 变量名 | 值 | 说明 |
|---|---|---|
| `VITE_API_BASE_URL` | `https://你的VPS域名或IP:8000` | 后端地址 |
| `VITE_SITE_PASSWORD` | `自定义密码` | 网站访问密码，留空则不启用 |

**3. 触发部署**

保存后 Cloudflare 会自动构建并部署，完成后获得 `yourapp.pages.dev` 域名。

---

## 三、收尾

将 Cloudflare Pages 域名填回 VPS 的 `.env`：

```env
FRONTEND_URL=https://yourapp.pages.dev
ALLOWED_ORIGINS=https://yourapp.pages.dev
```

重启后端：

```bash
sudo systemctl restart saveany
```

---

## 本地开发

```bash
# 后端
cd backend
cp .env.example .env
pip install -r requirements.txt
python main.py

# 前端（新终端）
cd frontend
npm install
npm run dev
```

本地开发无需设置 `VITE_API_BASE_URL`，Vite 会自动将 `/api` 请求代理到 `localhost:8000`。

---

## 四、更新线上代码

本地改动推送到远程后，在 VPS 上执行以下命令同步最新代码并重启服务：

```bash
cd /opt/saveany
git pull

# 如果 requirements.txt 有变动，重新安装依赖
/opt/saveany/venv/bin/pip install -r backend/requirements.txt

# 重启服务
sudo systemctl restart saveany
sudo systemctl status saveany
```

---

## 五、后端迁移方案

VPS 到期或需要换机器时，按以下步骤操作。

### 备份（旧 VPS 上执行）

```bash
bash /opt/saveany/backend/scripts/backup.sh
```

备份文件保存在 `/opt/saveany-backups/`，包含代码、`.env` 配置、SQLite 数据库。

将备份文件下载到本地：

```bash
# 在本地执行，将备份文件拉到本地
gcloud compute scp saveany-backend:/opt/saveany-backups/saveany_backup_xxx.tar.gz ./ --zone=us-west1-b
```

### 恢复（新 VPS 上执行）

**1. 将备份文件上传到新 VPS**

```bash
gcloud compute scp saveany_backup_xxx.tar.gz 新机器名:/root/ --zone=新机器zone
```

**2. 执行恢复脚本**

```bash
sudo bash restore.sh /root/saveany_backup_xxx.tar.gz
```

脚本会自动完成：安装依赖 → 解压备份 → 重建虚拟环境 → 注册服务 → 恢复 Nginx 配置。

**3. 重新申请 SSL 证书**

新机器 IP 变了，需要先把域名 DNS 指向新 IP，再申请证书：

```bash
sudo certbot --nginx -d saveany.initchu.asia
```

**4. 更新前端配置**

如果后端域名/IP 变了，去 Cloudflare Pages → 环境变量，更新 `VITE_API_BASE_URL`，重新部署前端。

### 定时自动备份（可选）

**1. 准备备份目录，将所有权赋给当前用户**

```bash
sudo mkdir -p /opt/saveany-backups
sudo chown $(whoami):$(whoami) /opt/saveany-backups
```

**2. 设置每天凌晨 3 点自动备份（普通用户 crontab，无需 sudo）**

```bash
crontab -e
```

添加：

```
0 3 * * * bash /opt/saveany/backend/scripts/backup.sh
```

备份文件和日志均保存在 `/opt/saveany-backups/`，查看日志：

```bash
tail -50 /opt/saveany-backups/backup.log
```

**3. 手动触发一次测试**

```bash
bash /opt/saveany/backend/scripts/backup.sh
```
