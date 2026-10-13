from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Server Medsos Checker Aktif, Wak! 🚀"}

@app.post("/check")
def check_video(data: dict):
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="Mana URL-nya, Wak?")
    
    ydl_opts = {
        'extract_flat': False,
        'skip_download': True, # Cuma ekstrak data/metadata, aman dari jebol kuota server
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Ambil data penting buat dikirim ke HP
            result = {
                "title": info.get("title"),
                "uploader": info.get("uploader"),
                "platform": info.get("extractor"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "formats": []
            }
            
            # Saring pilihan format video/resolusi yang tersedia
            for f in info.get("formats", []):
                if f.get("vcodec") != "none": # Pastikan ini jalur video aktif
                    result["formats"].append({
                        "resolution": f.get("format_note") or f.get("resolution"),
                        "ext": f.get("ext"),
                        "fps": f.get("fps"),
                        "url": f.get("url")
                    })
                    
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
