# Eğitim ve Test Sonuçları — Özet

## Eğitim Ayarları
- Model: YOLOv8n (pre-trained, COCO)
- Epoch: 50 (patience=20, early stopping tetiklenmedi)
- Görüntü boyutu: 640x640
- Batch size: 8
- Optimizer: AdamW (otomatik seçildi, lr≈0.002, momentum=0.9)
- Veri seti: 115 train + 32 valid (tek sınıf: stop_sign)

## Nihai Doğrulama Metrikleri (Epoch 50)

| Metrik | Değer |
|---|---|
| Precision | 0.997 |
| Recall | 0.976 |
| mAP50 | 0.988 |
| mAP50-95 | 0.922 |
| Box loss (val) | 0.410 |
| Cls loss (val) | 0.494 |
| DFL loss (val) | 0.844 |

En yüksek mAP50 değeri (0.995), epoch 21'de elde edilmiş; sonraki epoch'larda model
bu seviyenin etrafında dalgalanarak kararlı kalmıştır (bkz. results.png).

## Confusion Matrix (bkz. confusion_matrix.png)

Ham sayılar: 32 doğrulama görüntüsündeki toplam 41 STOP tabelasından 40'ı doğru
tespit edilmiş (TP), 1'i kaçırılmış (FN); ayrıca 1 adet yanlış alarm (FP) —
gerçekte STOP tabelası olmayan bir bölgenin STOP tabelası olarak işaretlenmesi —
görülmüştür. Normalize edilmiş grafikte bu tek FP, veri setinde başka "background"
örneği bulunmadığından background sütununda %100 olarak görünür; bu, modelin genel
olarak çok sayıda yanlış alarm ürettiği anlamına gelmez, yalnızca payda küçük
olduğu için oluşan bir görsel etkidir.

## Test Veri Seti Sonuçları (stop_sign_data_set, 5 görüntü, confidence=0.25)

| Görüntü | Tespit | Confidence |
|---|---|---|
| photo-1518749031467-bb37f48aee10.jpg (alacakaranlık) | 1 stop_sign | 0.97 |
| photo-1558626219-fa0c107b5613.jpg (koni + araçlar arasında) | 1 stop_sign | 0.90 |
| photo-1635481585588-2440d43b6747.jpg (Endonezce "BERHENTI" tabelası) | 1 stop_sign | 0.97 |
| photo-1727156275339-aad186798856.jpg (diğer tabelaların yanında) | 1 stop_sign | 0.98 |
| premium_photo-1731192705955-f10a8e7174d2.jpg | 1 stop_sign | 0.98 |

**Sonuç: 5/5 görüntüde doğru tespit, ortalama confidence ≈ 0.96.**

Özellikle dikkat çekici iki örnek:
1. Farklı dilde ("BERHENTI") yazan bir STOP tabelasının doğru tespit edilmesi, modelin
   metni değil tabelanın geometrik şeklini ve renk desenini öğrendiğini göstermektedir.
2. Turuncu trafik konileri ve çok sayıda araç içeren, kırmızı/turuncu renklerin bol
   olduğu bir sahnede modelin yalnızca gerçek STOP tabelasını işaretlemesi, önceki
   ödevdeki saf renk tabanlı yöntemin aksine, yapay zeka tabanlı yaklaşımın
   sağlamlığını doğrulamaktadır.
