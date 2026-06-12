#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 API بسيط لمنصة آمِن
يعرض قائمة الفيديوهات من R2
"""

import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from botocore.client import Config
from datetime import datetime

app = Flask(__name__)
CORS(app)  # السماح بـ CORS للموقع

# ═══════════════════════════════════════════════════════════
# ⚙️ الإعدادات
# ═══════════════════════════════════════════════════════════

R2_ACCESS_KEY = os.getenv('R2_ACCESS_KEY')
R2_SECRET_KEY = os.getenv('R2_SECRET_KEY')
R2_ENDPOINT = os.getenv('R2_ENDPOINT')
R2_BUCKET = os.getenv('R2_BUCKET', 'amen-videos')
R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')

# إنشاء عميل R2
s3 = boto3.client(
    's3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    config=Config(signature_version='s3v4')
)

# ═══════════════════════════════════════════════════════════
# 📡 API Endpoints
# ═══════════════════════════════════════════════════════════

@app.route('/')
def home():
    """الصفحة الرئيسية"""
    return jsonify({
        'status': 'active',
        'message': 'مرحباً بك في API منصة آمِن 🌟',
        'endpoints': {
            '/api/videos': 'GET - قائمة جميع الفيديوهات',
            '/api/videos/<category>': 'GET - فيديوهات حسب القسم',
            '/api/stats': 'GET - إحصائيات المنصة'
        }
    })

@app.route('/api/videos')
def get_videos():
    """جلب جميع الفيديوهات من R2"""
    try:
        # جلب جميع الملفات من R2
        response = s3.list_objects_v2(Bucket=R2_BUCKET)
        
        videos = []
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                
                # تجاهل الملفات غير الفيديو
                if not key.endswith(('.mp4', '.webm', '.mov')):
                    continue
                
                # استخراج المعلومات من اسم الملف
                # مثال: quran_video_001_1234567890.mp4
                parts = key.replace('.mp4', '').split('_')
                category = parts[0] if len(parts) > 0 else 'other'
                
                # بناء الرابط العام
                video_url = f"{R2_PUBLIC_URL}/{key}"
                
                videos.append({
                    'id': key,
                    'title': key.replace('_', ' ').replace('.mp4', ''),
                    'category': category,
                    'url': video_url,
                    'thumbnail': f"{video_url}?poster",  # R2 يولّد thumbnail تلقائياً
                    'size': obj['Size'],
                    'uploaded_at': obj['LastModified'].isoformat()
                })
        
        return jsonify({
            'success': True,
            'count': len(videos),
            'videos': videos
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/videos/<category>')
def get_videos_by_category(category):
    """جلب فيديوهات حسب القسم"""
    try:
        # جلب جميع الفيديوهات
        response = s3.list_objects_v2(
            Bucket=R2_BUCKET,
            Prefix=f"{category}_"  # فلترة حسب القسم
        )
        
        videos = []
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                
                if not key.endswith(('.mp4', '.webm', '.mov')):
                    continue
                
                video_url = f"{R2_PUBLIC_URL}/{key}"
                
                videos.append({
                    'id': key,
                    'title': key.replace('_', ' ').replace('.mp4', ''),
                    'category': category,
                    'url': video_url,
                    'thumbnail': f"{video_url}?poster",
                    'size': obj['Size'],
                    'uploaded_at': obj['LastModified'].isoformat()
                })
        
        return jsonify({
            'success': True,
            'category': category,
            'count': len(videos),
            'videos': videos
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats')
def get_stats():
    """إحصائيات المنصة"""
    try:
        response = s3.list_objects_v2(Bucket=R2_BUCKET)
        
        total_videos = 0
        total_size = 0
        categories = {}
        
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                
                if not key.endswith(('.mp4', '.webm', '.mov')):
                    continue
                
                total_videos += 1
                total_size += obj['Size']
                
                # حساب عدد الفيديوهات لكل قسم
                category = key.split('_')[0]
                categories[category] = categories.get(category, 0) + 1
        
        return jsonify({
            'success': True,
            'stats': {
                'total_videos': total_videos,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'categories': categories,
                'last_updated': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ═══════════════════════════════════════════════════════════
# 🚀 تشغيل السيرفر
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
