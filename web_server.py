import sys
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Proje root'unu Python path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from domain.models import FilterCriteria
from infrastructure.aws_client import S3LogFetcher
from application.summary_service import LogSummaryService
from application.parser_factory import LogParserFactory
from infrastructure.aws_exceptions import S3ResourceNotFoundException

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Web arayüzünü göster"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_logs():
    """Log analizi için API endpoint"""
    data = request.get_json()
    
    bucket_name = data.get('bucket_name')
    prefix = data.get('prefix')
    log_type = data.get('log_type', 'json')
    
    if not bucket_name or not prefix:
        return jsonify({'error': 'Bucket name ve prefix gerekli'}), 400
    
    try:
        # 1. Filtreleri oluştur
        filters = FilterCriteria(bucket_name=bucket_name, prefix=prefix, log_type=log_type)
        
        # 2. AWS S3 istemcisini hazırla
        log_fetcher = S3LogFetcher()
        
        # 3. Parser'ı seç
        parser = LogParserFactory.get_parser(log_type)
        
        # 4. Servisi çalıştır
        summary_service = LogSummaryService(log_fetcher, parser)
        summary_report = summary_service.generate_summary(filters)
        
        # 5. Sonuçları JSON olarak döndür
        return jsonify({
            'success': True,
            'data': {
                'total_logs': summary_report.total_logs,
                'top_errors': summary_report.top_errors,
                'avg_latency': round(summary_report.avg_latency, 2)
            }
        })
    
    except S3ResourceNotFoundException as e:
        return jsonify({'error': f'Kaynak bulunamadı: {str(e)}'}), 404
    except NotImplementedError as e:
        return jsonify({'error': f'Desteklenmeyen log tipi: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Hata: {str(e)}'}), 500

@app.route('/api/log-types', methods=['GET'])
def get_log_types():
    """Desteklenen log tipleri"""
    return jsonify({
        'log_types': ['json', 'txt']
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
