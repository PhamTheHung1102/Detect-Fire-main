from ultralytics import YOLO
import cv2
import requests
import datetime
import time

# Load mô hình YOLO đã train
model = YOLO('model.pt')

# Khởi tạo camera
cam = cv2.VideoCapture(0)

# Thông tin bot Telegram
api_key = '7924496422:AAG_ytGhrQmgPiEea57mHaR8Yn3oyvZJ4F8'
chat_id = '6805428031'

# Biến kiểm soát gửi ảnh (chỉ gửi sau mỗi 30s)
fire_detected = False
last_sent_time = 0  # Lưu thời gian gửi ảnh cuối cùng


# Hàm gửi ảnh qua Telegram
def send_telegram_photo(photo_path):
    chat = f'🔥 Phát hiện cháy lúc {datetime.datetime.now().strftime("%H:%M:%S")}'
    url_message = f'https://api.telegram.org/bot{api_key}/sendMessage'
    requests.post(url_message, data={'chat_id': chat_id, 'text': chat})

    # Gửi ảnh
    url_photo = f'https://api.telegram.org/bot{api_key}/sendPhoto'
    with open(photo_path, 'rb') as file:
        response = requests.post(url_photo, files={'photo': file}, data={'chat_id': chat_id, 'caption': chat})

    if response.status_code == 200:
        print("✅ Đã gửi ảnh thành công")
    else:
        print(f"❌ Lỗi gửi ảnh: {response.text}")


# Vòng lặp chính
while True:
    # Đọc hình ảnh từ camera
    ret, frame = cam.read()
    if not ret:
        print("❌ Không thể đọc từ camera.")
        break

    # Dự đoán với YOLOv8
    results = model.predict(frame, conf=0.4, verbose=False)
    boxes = results[0].boxes.xyxy
    confs = results[0].boxes.conf

    # Hiển thị box và độ tin cậy
    fire_count = 0
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box)
        confidence = float(confs[i])
        if confidence > 0.4:
            fire_count += 1
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, f'Fire: {confidence:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Xử lý phát hiện cháy
    if fire_count > 0:
        cv2.putText(frame, f'{fire_count} fire detected', (30, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        current_time = time.time()
        if not fire_detected or (current_time - last_sent_time > 30):
            fire_detected = True
            last_sent_time = current_time
            photo_path = 'fire_detected.jpg'

            # Lưu ảnh & gửi Telegram
            cv2.imwrite(photo_path, frame)
            send_telegram_photo(photo_path)
    else:
        cv2.putText(frame, f'No fire visible', (30, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        fire_detected = False  # Reset cờ nếu không còn phát hiện cháy

    # Hiển thị khung hình
    cv2.imshow('Fire Detection', frame)

    # Thoát khi nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng camera
cam.release()
cv2.destroyAllWindows()
