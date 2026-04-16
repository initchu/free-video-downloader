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

| 变量名 | 值 |
|---|---|
| `VITE_API_BASE_URL` | `https://你的VPS域名或IP:8000` |

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
