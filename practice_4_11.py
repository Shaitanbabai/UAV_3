from  flask import Flask, Response, render_template
import cv2
"""
Запуск:
Запускаем 4.10
Запускаем 4.11
Открываем браузер, вводим в адресную строку http://127.0.0.1:5000/video_feed
"""

app = Flask(__name__)

# Создаем функцию для захвата видеопотока
def video_sttream():
    camera = cv2.VideoCapture("udp://127.0.0.1:1234", cv2.CAP_FFMPEG)  # перехватываем порт и добавляем обработчик
    while True:
        ret, frame = camera.read()
        if not ret:  # если не удалось получить кадр, то выходим
            break
        ret, buffer = cv2.imencode('.jpg', frame)  # перекодирует картинку в байты
        frame = buffer.tobytes()
        # Генерация потока кадра
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

  # Возвращение ответа с типом MIME multipart/x-mixed-replace и границей frame
@app.route('/video_feed')
def video_feed():  # Создаем функцию для выдачи видеопотока в веб-интерфейс
    return Response(video_sttream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video')
def feed_2():
    return render_template('stream_4_11.html')

if __name__ == '__main__':
    app.run(debug=True)  # by default 127:0/0/1/5000