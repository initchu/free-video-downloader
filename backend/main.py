import os
import asyncio
from contextlib import asynccontextmanager
from urllib.parse import unquote

from dotenv import load_dotenv
load_dotenv()

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

from downloader import VideoDownloader
from douyin import DouyinParser, is_douyin_url
from database import init_db


downloader = VideoDownloader()
douyin_parser = DouyinParser(download_dir=downloader.DOWNLOAD_DIR)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    download_dir = downloader.DOWNLOAD_DIR
    if os.path.exists(download_dir):
        for f in os.listdir(download_dir):
            try:
                os.remove(os.path.join(download_dir, f))
            except OSError:
                pass


app = FastAPI(
    title="万能视频下载器 API",
    description="基于 yt-dlp 的万能视频下载服务，支持 1800+ 平台",
    version="1.0.0",
    lifespan=lifespan,
)

# 生产环境通过 ALLOWED_ORIGINS 环境变量指定前端域名（逗号分隔）
# 例如：ALLOWED_ORIGINS=https://yourapp.pages.dev,https://yourdomain.com
# 未配置时默认允许所有来源（仅适合本地开发）
import re

# Production: set ALLOWED_ORIGINS env var (comma-separated exact origins)
# Set ALLOWED_ORIGIN_PATTERNS for wildcard subdomain patterns (comma-separated regex)
# e.g. ALLOWED_ORIGIN_PATTERNS=https://.*\.free-video-downloader-v5i\.pages\.dev
_raw_origins = os.getenv("ALLOWED_ORIGINS", "")
_exact_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

_raw_patterns = os.getenv("ALLOWED_ORIGIN_PATTERNS", "")
_origin_patterns = [re.compile(p.strip()) for p in _raw_patterns.split(",") if p.strip()]

def is_origin_allowed(origin: str) -> bool:
    if not _exact_origins and not _origin_patterns:
        return True  # allow all when nothing configured (local dev)
    if origin in _exact_origins:
        return True
    return any(p.fullmatch(origin) for p in _origin_patterns)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_exact_origins if _exact_origins else ["*"],
    allow_origin_regex=_raw_patterns.strip() or None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ParseRequest(BaseModel):
    url: str


class DownloadRequest(BaseModel):
    url: str
    format_id: str = "bestvideo+bestaudio/best"


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "万能视频下载器服务运行中"}


@app.post("/api/parse")
async def parse_video(req: ParseRequest):
    """解析视频信息（抖音走专用模块，其他走 yt-dlp）"""
    try:
        loop = asyncio.get_event_loop()
        if is_douyin_url(req.url):
            result = await loop.run_in_executor(None, douyin_parser.parse, req.url)
        else:
            result = await loop.run_in_executor(None, downloader.parse_video, req.url)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "success": False,
            "error": f"解析失败: {str(e)}"
        })


@app.post("/api/download")
async def download_video(req: DownloadRequest):
    """服务端下载视频后提供文件下载（抖音走专用模块）"""
    try:
        # debug logging
        print(f"[download] URL: {req.url}, Format ID: {req.format_id}")
        
        loop = asyncio.get_event_loop()
        if is_douyin_url(req.url):
            result = await loop.run_in_executor(None, douyin_parser.download, req.url)
        else:
            result = await loop.run_in_executor(
                None, downloader.download_video, req.url, req.format_id
            )
        filepath = result["filepath"]
        if not os.path.exists(filepath):
            raise HTTPException(status_code=500, detail="下载的文件不存在")

        return FileResponse(
            path=filepath,
            filename=result["filename"],
            media_type="application/octet-stream",
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[download error] {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=400, detail={
            "success": False,
            "error": f"下载失败: {str(e)}"
        })


@app.post("/api/direct-url")
async def get_direct_url(req: DownloadRequest):
    """获取视频直链"""
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, downloader.get_direct_url, req.url, req.format_id
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "success": False,
            "error": f"获取直链失败: {str(e)}"
        })


@app.get("/api/proxy/thumbnail")
async def proxy_thumbnail(url: str = Query(..., description="缩略图URL")):
    """代理获取视频缩略图，绕过防盗链"""
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            resp = await client.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": url,
            })
            resp.raise_for_status()
            content_type = resp.headers.get("content-type", "image/jpeg")
            return StreamingResponse(
                iter([resp.content]),
                media_type=content_type,
                headers={"Cache-Control": "public, max-age=86400"},
            )
    except Exception:
        raise HTTPException(status_code=502, detail="缩略图加载失败")


# 挂载功能模块路由
from api_summarize import router as summarize_router
from api_auth import router as auth_router
from api_payment import router as payment_router

app.include_router(summarize_router)
app.include_router(auth_router)
app.include_router(payment_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
