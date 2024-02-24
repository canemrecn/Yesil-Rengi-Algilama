import cv2
import numpy as np
#Gerekli kütüphaneleri import et
altRenk = np.array([30, 60, 60])
ustRenk = np.array([64, 255, 255])
# Alttaki ve üstteki renk sınırlarını tanımla
RENK = 'YESIL'
# Tespit edilecek rengi belirle
kamera = cv2.VideoCapture(0)
# Kamera bağlantısını başlat
cember = True
# Konturları çember olarak çizme durumunu belirle
while True:
    if not kamera.isOpened(): break
# Kamera açık değilse döngüyü sonlandır
    _,kare = kamera.read()
# Bir kareyi oku
    hsv = cv2.cvtColor(kare, cv2.COLOR_BGR2HSV)
# Kareyi HSV renk uzayına dönüştür
    maske = cv2.inRange(hsv,altRenk,ustRenk)
# HSV görüntüsündeki renk aralığını maskele
    kernel = np.ones((5,5),'int')
    maske = cv2.dilate(maske,kernel)
# Maskeyi genişlet
    res = cv2.bitwise_and(kare,kare,mask=maske)
# Orijinal kare üzerinde maskeyi uygula
    konturlar = cv2.findContours(maske.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
# Maske üzerindeki konturları bul
    say = 0
    for kontur in konturlar:
        alan = cv2.contourArea(kontur)
        if alan > 600:
            say+=1
            (x,y,w,h)=cv2.boundingRect(kontur)
            cv2.rectangle(kare, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if cember:
                (x, y), ycap = cv2.minEnclosingCircle(kontur)
                merkez = (int(x), int(y))
                ycap = int(ycap)
                img = cv2.circle(kare, merkez, ycap, (255, 0, 0), 2)
# Konturları çiz
    if say > 0:
        cv2.putText(kare, f'{say} {RENK} nesne bulundu', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
# Tespit edilen nesne sayısını ekrana yazdır
    cv2.imshow('kare', kare)
# Kareyi göster
    k = cv2.waitKey(4) & 0xFF
# Klavyeden bir tuşa basılmasını bekle
    if k == 27: break
# ESC tuşuna basıldığında döngüyü sonlandır
if kamera.isOpened():
    kamera.release()
# Kamera bağlantısını serbest bırak
cv2.destroyAllWindows()
# Tüm pencereleri kapat