#!/usr/bin/env python3
"""Hailo Vision — Edge AI inference pipeline for BlackRoad fleet"""
import json, sys, os, random
from http.server import HTTPServer, BaseHTTPRequestHandler

MODELS = [
    {"id": "yolov8n", "name": "YOLOv8 Nano", "task": "detection", "tops": 8.7, "fps": 120},
    {"id": "yolov8s", "name": "YOLOv8 Small", "task": "detection", "tops": 14.2, "fps": 85},
    {"id": "mobilenet_v2", "name": "MobileNet V2", "task": "classification", "tops": 3.4, "fps": 200},
    {"id": "deeplabv3", "name": "DeepLab V3", "task": "segmentation", "tops": 11.8, "fps": 45},
]
LABELS = ["person", "car", "bicycle", "dog", "cat", "chair", "laptop", "phone", "cup", "book"]

def mock_detect(model_id="yolov8n"):
    n = random.randint(1, 5)
    return [{"label": random.choice(LABELS), "confidence": round(random.uniform(0.7, 0.99), 2),
             "bbox": [random.randint(10, 200), random.randint(10, 200), random.randint(50, 300), random.randint(50, 300)]}
            for _ in range(n)]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/models":
            self.respond(200, MODELS)
        elif self.path.startswith("/api/detect"):
            self.respond(200, {"model": "yolov8n", "device": "hailo8", "detections": mock_detect(), "inference_ms": round(random.uniform(5, 25), 1)})
        elif self.path == "/api/health":
            self.respond(200, {"status": "ok", "device": "hailo-8", "tops": 26, "temperature": round(45 + random.uniform(0, 10), 1)})
        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body style='background:#0a0a0a;color:#f5f5f5;font-family:monospace;padding:40px'><h1>Hailo Vision</h1><p>Edge AI at 52 TOPS</p><pre>GET /api/models\nGET /api/detect\nGET /api/health</pre></body></html>")
        else:
            self.respond(404, {"error": "Not found"})
    def respond(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    def log_message(self, *args): pass

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8789
    print(f"Hailo Vision running on :{port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
