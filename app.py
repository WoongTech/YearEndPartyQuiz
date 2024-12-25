from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time
import threading
import queue
import json
import random

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "allow_headers": ["Content-Type"],
        "methods": ["GET", "POST", "OPTIONS"]
    }
})

socketio = SocketIO(app, 
    cors_allowed_origins="*",
    ping_timeout=60,
    ping_interval=25,
    async_mode='eventlet'  # eventlet 모드 사용
)

class TextDisplay:
    def __init__(self, category: str, text: str, answer: str):
        self.category = category
        self.text = text
        self.answer = answer
        self.current_position = 0
        self.displayed_text = ""
        self.is_playing = False
        self.display_thread = None
        self.lock = threading.Lock()
        self.event_queue = queue.Queue()
        self.showing_category = True
        self.stop_thread = False

    def display_character(self):
        while self.is_playing and not self.stop_thread:
            with self.lock:
                if self.current_position < len(self.text):
                    self.displayed_text += self.text[self.current_position]
                    self.current_position += 1
                    self.event_queue.put(('update_text', {'text': self.displayed_text}))
                    time.sleep(0.1)
                else:
                    self.is_playing = False
                    break

    def toggle_play(self):
        with self.lock:
            if self.showing_category:
                self.showing_category = False
                self.is_playing = True
                if self.display_thread is None or not self.display_thread.is_alive():
                    self.display_thread = threading.Thread(target=self.display_character)
                    self.display_thread.start()
            else:
                self.is_playing = not self.is_playing
                if self.is_playing:
                    if self.display_thread is None or not self.display_thread.is_alive():
                        self.display_thread = threading.Thread(target=self.display_character)
                        self.display_thread.start()

    def clear_text(self):
        with self.lock:
            self.displayed_text = ""
            self.event_queue.put(('update_text', {'text': self.displayed_text}))

    def show_all(self):
        with self.lock:
            self.is_playing = False
            self.showing_category = False
            self.event_queue.put(('show_all', {'full_text': self.text, 'answer': self.answer}))

    def stop(self):
        with self.lock:
            self.stop_thread = True
            self.is_playing = False
            if self.display_thread and self.display_thread.is_alive():
                self.display_thread.join(timeout=0.1)

class TextDisplayManager:
    def __init__(self):
        try:
            with open('quiz_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.original_texts = data['questions']
                # Create a shuffled copy of the questions
                self.texts = self.original_texts.copy()
                random.shuffle(self.texts)
        except Exception as e:
            print(f"Error loading quiz data: {e}")
            self.original_texts = []
            self.texts = []
        
        self.current_index = 0
        self.current_display = None

    def get_current_text(self):
        return self.texts[self.current_index]

    def next_text(self):
        self.current_index = (self.current_index + 1) % len(self.texts)
        # If we've gone through all questions, reshuffle
        if self.current_index == 0:
            random.shuffle(self.texts)
        return self.get_current_text()

    def previous_text(self):
        self.current_index = (self.current_index - 1 + len(self.texts)) % len(self.texts)
        return self.get_current_text()

    def shuffle_questions(self):
        """Manually shuffle the questions and reset index"""
        random.shuffle(self.texts)
        self.current_index = 0
        return self.get_current_text()

# 전역 텍스트 디스플레이 관리자
text_display_manager = TextDisplayManager()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    current_text = text_display_manager.get_current_text()
    text_display = TextDisplay(current_text['category'], current_text['text'], current_text['answer'])
    text_display_manager.current_display = text_display
    
    # 이벤트 처리 스레드 시작
    def process_events():
        while True:
            try:
                event_type, data = text_display.event_queue.get(timeout=1)
                socketio.emit(event_type, data)
            except queue.Empty:
                pass

    threading.Thread(target=process_events, daemon=True).start()
    
    emit('init', {
        'text': f"[카테고리: {current_text['category']}]",
        'current_index': text_display_manager.current_index,
        'total_texts': len(text_display_manager.texts)
    })

@socketio.on('toggle_play')
def handle_toggle_play():
    if text_display_manager.current_display:
        text_display_manager.current_display.toggle_play()

@socketio.on('clear_text')
def handle_clear_text():
    if text_display_manager.current_display:
        text_display_manager.current_display.clear_text()

@socketio.on('show_all')
def handle_show_all():
    if text_display_manager.current_display:
        text_display_manager.current_display.show_all()

@socketio.on('next_text')
def handle_next_text():
    if text_display_manager.current_display:
        text_display_manager.current_display.stop()
    
    next_text = text_display_manager.next_text()
    text_display = TextDisplay(next_text['category'], next_text['text'], next_text['answer'])
    text_display_manager.current_display = text_display
    
    # 새로운 텍스트로 변경할 때 초기 설정
    text_display.showing_category = True
    
    # 이벤트 처리 스레드 시작
    threading.Thread(target=process_events, args=(text_display,), daemon=True).start()
    
    emit('text_changed', {
        'text': f"[카테고리: {next_text['category']}]",
        'current_index': text_display_manager.current_index,
        'total_texts': len(text_display_manager.texts)
    })

@socketio.on('previous_text')
def handle_previous_text():
    if text_display_manager.current_display:
        text_display_manager.current_display.stop()
    
    previous_text = text_display_manager.previous_text()
    text_display = TextDisplay(previous_text['category'], previous_text['text'], previous_text['answer'])
    text_display_manager.current_display = text_display
    
    # 새로운 텍스트로 변경할 때 초기 설정
    text_display.showing_category = True
    
    # 이벤트 처리 스레드 시작
    threading.Thread(target=process_events, args=(text_display,), daemon=True).start()
    
    emit('text_changed', {
        'text': f"[카테고리: {previous_text['category']}]",
        'current_index': text_display_manager.current_index,
        'total_texts': len(text_display_manager.texts)
    })

# 공통으로 사용되는 process_events 함수를 전역으로 이동
def process_events(text_display):
    while True:
        try:
            event_type, data = text_display.event_queue.get(timeout=1)
            socketio.emit(event_type, data)
        except queue.Empty:
            pass

if __name__ == '__main__':
    import eventlet
    eventlet.monkey_patch()
    
    port = 5000
    host = '0.0.0.0'
    
    print(f"\n🎮 Quiz Game Server Starting...")
    print(f"📝 Loading questions from quiz_data.json")
    print(f"🌐 Server will be available at:")
    print(f"   - Local: http://localhost:{port}")
    print(f"   - Network: http://{host}:{port}")
    print(f"🎯 Press Ctrl+C to stop the server\n")
    
    socketio.run(app, 
                host=host, 
                port=port, 
                debug=False,
                allow_unsafe_werkzeug=True)
