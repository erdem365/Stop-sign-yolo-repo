# STOP Tabelası Tespiti — YOLOv8

Bu depo, **Destek Ekip - Ödev 3** kapsamında geliştirilen, derin öğrenme tabanlı
(YOLOv8n) STOP tabelası nesne tespit modelinin kodlarını, veri seti hazırlama
betiklerini ve test sonuçlarını içerir.

## İçerik

```
├── dataset_prep/
│   └── prepare_dataset.py     # Kaynak veri setinden tek sınıflı (STOP) alt veri seti üretir
├── training/
│   ├── train.py                # Model eğitim betiği
│   └── test_inference.py       # Test görüntüleri üzerinde çıkarım (inference) betiği
├── stop_sign_yolo_dataset/     # Eğitimde kullanılan hazır veri seti (train/valid + data.yaml)
├── results/
│   ├── results.png             # Eğitim/doğrulama metrik grafikleri
│   ├── confusion_matrix.png
│   ├── BoxPR_curve.png         # Precision-Recall eğrisi
│   └── metrics_summary.md      # Sayısal sonuçların özeti ve yorumu
├── test_images/                # Ödevdeki stop_sign_data_set üzerinde model çıktıları (kutulu görseller)
├── weights/
│   └── best.pt                 # Eğitilmiş model ağırlıkları
└── requirements.txt
```

## Kurulum

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` içeriği:
```
ultralytics>=8.3.0
```

## Veri Seti

Model, [Traffic-sign-detection-using-yolo](https://github.com/AsadiAhmad/Traffic-sign-detection-using-yolo)
(RoboFlow ile etiketlenmiş, MIT lisanslı, YOLO formatlı) açık veri setinden yalnızca
**STOP tabelası** etiketi içeren görüntüler filtrelenerek oluşturulan alt veri setiyle
eğitilmiştir (115 train + 32 valid görüntü, tek sınıf: `stop_sign`). Bu hazır veri
seti `stop_sign_yolo_dataset/` klasöründe zaten mevcuttur; aşağıdaki adım yalnızca
sıfırdan yeniden üretmek isterseniz gereklidir.

Veri setini kendiniz yeniden oluşturmak isterseniz, önce kaynak depoyu klonlayın:
```bash
git clone https://github.com/AsadiAhmad/Traffic-sign-detection-using-yolo.git
python dataset_prep/prepare_dataset.py \
    --src Traffic-sign-detection-using-yolo/Dataset \
    --out stop_sign_yolo_dataset
```

## Eğitim

Repo kök dizininden çalıştırın:
```bash
python training/train.py
```

Kullanılan parametreler ve gerekçeleri için ödev raporunun 3.b bölümüne bakınız.
Özet: `model=yolov8n.pt`, `epochs=50`, `imgsz=640`, `batch=8`, `optimizer=auto`
(AdamW olarak otomatik seçildi), `patience=20`. Eğitim çıktıları `runs/stop_sign_yolov8n/`
altına kaydedilir; en iyi ağırlıklar `runs/stop_sign_yolov8n/weights/best.pt` olarak
oluşur (bu depoda paylaşılan `weights/best.pt` ile aynı ağırlıklardır).

## Test (Çıkarım)

Ödev kapsamında paylaşılan `stop_sign_data_set` görüntüleri üzerinde modeli test
etmek için (repo kök dizininden):
```bash
python training/test_inference.py --source path/to/stop_sign_data_set --conf 0.25
```
Çıktılar, tespit kutuları çizilmiş olarak `test_images_output/predictions/` klasörüne
kaydedilir. Bu depoda zaten paylaşılan `test_images/` klasörü, bu betiğin önceden
üretilmiş çıktılarını (5 test görüntüsü, kutulu) içerir.

## Sonuçlar

Eğitim/doğrulama metrikleri (box loss, class loss, mAP50, precision, recall) ve
bunların yorumu için `results/metrics_summary.md` dosyasına bakınız. Özet:
Precision 0.997, Recall 0.976, mAP50 0.988, mAP50-95 0.922 (epoch 50, best.pt).

## Lisans

Kod MIT lisansı ile paylaşılmıştır. Kullanılan üçüncü taraf veri seti kendi
lisansına (MIT) tabidir.
