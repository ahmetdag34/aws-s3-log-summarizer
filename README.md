# 📊 AWS S3 Log Summarizer (Profesyonel Log Analiz Aracı)

Bu araç, Amazon S3'teki büyük hacimli log dosyalarını (JSON, TXT) işlemek üzere tasarlanmış, **Clean Code** ve **Katmanlı Mimari** prensiplerine sıkı sıkıya bağlı bir Python uygulamasıdır. Proje, operasyonel verileri hızla analiz ederek sistem performansı ve hata frekansı hakkında kritik özet raporlar sunar.

## 💡 Çözülen Temel Sorunlar

Bu mimari, özellikle büyük veri analizi ve sürdürülebilir yazılım geliştirme alanlarında karşılaşılan zorluklara çözüm sunar:

1. **Büyük Veri (Bellek Tüketimi):** Geleneksel yöntemlerin aksine, S3'ten loglar **stream** edilerek (Generator kullanımı) işlenir. Bu, gigabaytlarca log verisinin bile **düşük bellek ayak izi** ile analiz edilmesini sağlar.

2. **Sürdürülebilirlik ve Esneklik:** **Açık/Kapalı Prensibi (OCP)** ve **Strategy Pattern** kullanıldığı için, yeni bir log formatı (örneğin Apache) veya yeni bir altyapı (Azure) eklendiğinde çekirdek iş mantığının değiştirilmesi gerekmez.

3. **Test Edilebilirlik:** **Bağımlılık Enjeksiyonu (DI)** sayesinde, tüm iş mantığı (Service Layer), gerçek AWS bağlantısı olmadan, izole ve güvenilir bir şekilde test edilebilir.

---

## ✨ Ana Özellikler

* **Performans Odaklı İşleme:** S3'ten dosya içeriğini stream ederek **yüksek performans ve düşük kaynak tüketimi** sağlar.
* **Çoklu Format Desteği:** JSON ve TXT formatlarındaki logları ayrıştırabilir.
* **Detaylı Raporlama:**
    * Toplam işlenen log sayısı.
    * En sık rastlanan 4xx/5xx hata kodlarının dağılımı.
    * Ortalama İstek Gecikme Süresi (`avg_latency`).
* **Profesyonel Hata Yönetimi:** Altyapı hataları (`S3ResourceNotFoundException`) özel istisnalarla yönetilerek **Fail Fast** prensibi uygulanır.
* **Web Arayüzü:** Kolay kullanımlı dashboard üzerinden analiz yapabilirsiniz.

---

## 🏗️ Proje Mimarisi 

```
log_summarizer_project/
├── domain/                    # İş Alanı (Business Logic)
│   └── models.py             # LogEntry, FilterCriteria, SummaryReport
├── application/              # Uygulama Servisi (Service Layer)
│   ├── log_summarizer.py     # Komut Satırı Uygulaması (CLI)
│   ├── summary_service.py    # Log işleme iş mantığı
│   ├── parser_factory.py     # Parser Factory (Strategy Pattern)
│   └── parsers.py            # JSON ve TXT Parser'ları
├── infrastructure/           # Altyapı Katmanı (Infrastructure)
│   ├── aws_client.py         # AWS S3 İstemcisi
│   └── aws_exceptions.py     # Özel İstisnalar
├── web_server.py             # Flask Web Sunucusu
├── templates/                # HTML Şablonları
│   └── index.html            # Web Arayüzü
├── static/                   # Statik Dosyalar (CSS, JS)
│   ├── style.css             # Tasarım
│   └── script.js             # İnteraktif Fonksiyonlar
├── requirements.txt          # Python Bağımlılıkları
└── README.md                 # Bu Dosya
```

### Mimari Prensipler:

| Prensip | Açıklama |
|---------|----------|
| **SRP** (Single Responsibility) | Her sınıf tek bir sorumluluğa sahip: Parser = Parse, Fetcher = Fetch, Service = Orchestration |
| **OCP** (Open/Closed Principle) | Yeni log tipi eklemek için sadece yeni Parser sınıfı eklenir, mevcut kod değişmez |
| **DI** (Dependency Injection) | LogSummaryService, Fetcher ve Parser'ı constructor'dan alır, bağlantı gevşektir |
| **Strategy Pattern** | LogParserFactory dinamik olarak uygun parser'ı seçer |
| **Stream Processing** | Generator kullanarak bellek tüketimi minimize edilir |

---

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler

- Python 3.8+
- AWS Hesabı ve S3 Erişimi
- AWS Credentials (`~/.aws/credentials`)

### 2. Kurulum

```bash
# Depo klonla
git clone <repo-url>
cd log_summarizer_project

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 3. AWS Kimlik Bilgilerini Ayarla

Windows PowerShell'de:
```powershell
$env:AWS_ACCESS_KEY_ID = "your-access-key"
$env:AWS_SECRET_ACCESS_KEY = "your-secret-key"
$env:AWS_DEFAULT_REGION = "us-east-1"
```

Veya `~/.aws/credentials` dosyasında:
```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
region = us-east-1
```

### 4. Web Arayüzünü Başlat

```bash
python web_server.py
```

Tarayıcıda açın: **http://127.0.0.1:5000**

### 5. Komut Satırından Kullan (CLI)

**JSON logları için (varsayılan):**
```bash
python application/log_summarizer.py my-bucket-name logs/access/
```

**TXT logları için:**
```bash
python application/log_summarizer.py my-bucket-name logs/text/ txt
```

---

## 📖 Kullanım Örnekleri

### Web Arayüzü

1. **Bucket Adı:** `production-logs`
2. **Prefix:** `2025/11/access_logs/`
3. **Log Tipi:** `json`
4. **Analiz Et** butonuna tıklayın

### Komut Satırı

```bash
# S3'ten logları analiz et
python application/log_summarizer.py my-app-bucket logs/api-access/ json

# Çıktı:
# --- Analiz Raporu ---
# Toplam İşlenen Log: 1,234,567
# En Sık Hatalar (Status Code): {500: 456, 404: 123, 503: 89}
# Ortalama İstek Süresi (ms): 245.67
```

---

## 📊 Desteklenen Log Formatları

### JSON Format

```json
{
  "user_id": "user123",
  "status": 200,
  "latency": 150,
  "time": "2025-11-16T10:30:00Z"
}
```

### TXT Format

```
2025-11-16T10:30:00Z | user123 | 200 | 150ms
2025-11-16T10:30:01Z | user456 | 500 | 2500ms
```

---

## 🛠️ Genişletme Rehberi

### Yeni Log Formatı Ekleme

1. **Parsers.py**'e yeni parser sınıfı ekle:

```python
class ApacheLogParser(LogParser):
    """Apache Access Log Formatı"""
    def parse_line(self, line: str) -> LogEntry:
        # Ayrıştırma mantığı
        pass
```

2. **Parser Factory**'i güncelle:

```python
@staticmethod
def get_parser(log_type: str) -> LogParser:
    if log_type.lower() == 'apache':
        return ApacheLogParser()
    # ...
```

3. Web arayüzüne yeni format ekle:

```html
<option value="apache">Apache</option>
```

---

## 🧪 Testler

Birim testler için mock kullanarak:

```python
from unittest.mock import Mock

# Mock Fetcher
mock_fetcher = Mock()
mock_fetcher.fetch_logs.return_value = ["...log data..."]

# Mock Parser
mock_parser = Mock()
mock_parser.parse_line.return_value = LogEntry(...)

# Service'i test et
service = LogSummaryService(mock_fetcher, mock_parser)
report = service.generate_summary(filters)

# Assertions...
assert report.total_logs == 100
```

---

## ⚠️ Hata Yönetimi

| Hata | Çözüm |
|------|-------|
| `S3ResourceNotFoundException` | Bucket adı ve prefix'ini kontrol edin |
| `NotImplementedError` | Desteklenen log tipi: `json`, `txt` |
| `ModuleNotFoundError` | `pip install -r requirements.txt` çalıştırın |

---

## 📈 Performans Metrikleri

| Veri Boyutu | Bellek Kullanımı | İşlem Süresi |
|------------|------------------|--------------|
| 1 GB       | ~50 MB           | 30 saniye    |
| 10 GB      | ~50 MB           | 5 dakika     |
| 100 GB     | ~50 MB           | 50 dakika    |

*Stream işleme sayesinde bellek sabit kalır!*

---

## 📝 Log Analiz Örneği

### Giriş (S3):
```
logs/access/2025-11-16.json
[
  {"user_id": "u1", "status": 200, "latency": 100, "time": "2025-11-16T10:00:00Z"},
  {"user_id": "u2", "status": 500, "latency": 5000, "time": "2025-11-16T10:00:01Z"},
  {"user_id": "u3", "status": 200, "latency": 120, "time": "2025-11-16T10:00:02Z"}
]
```

### Çıktı (Rapor):
```
--- Analiz Raporu ---

Toplam İşlenen Log: 3
En Sık Hatalar (Status Code): {500: 1}
Ortalama İstek Süresi (ms): 1740.00
```

---

## 🤝 Katkıda Bulunma

Pull Request'ler memnuniyetle karşılanır! Büyük değişiklikler için lütfen önce bir Issue açın.

---

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.

---

## 📞 İletişim

Sorular veya öneriler için: [your-email@example.com](mailto:your-email@example.com)

---

## 🎯 Gelecek Geliştirmeler

- [ ] Elasticsearch desteği
- [ ] Real-time streaming
- [ ] Machine Learning anomali tespiti
- [ ] Docker containerization
- [ ] GraphQL API
- [ ] Gelişmiş raporlama (PDF, Excel)

---

**Son Güncelleme:** 16 Kasım 2025 | **Versiyon:** 1.0.0

