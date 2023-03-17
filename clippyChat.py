import gtts as gtts
import openai as openai
import os
from PyQt6 import QtCore
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import *
from dotenv import load_dotenv
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QPlainTextEdit, \
    QLineEdit
from playsound import playsound

chat_log: None


# Chatbox class/gui for Clippy
class ClippyChat(QWidget):
    def __init__(self):
        super(ClippyChat, self).__init__()
        # Load dot env file and pass API key to open.ai
        self.layout = None
        self.info_sentence = None
        self.chat_box = None
        self.input_txt = None
        self.send_button = None
        self.sound_button = None
        self.think_label = None
        self.worker = None
        self.worker_speak = None
        self.d = None
        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.player.mediaStatusChanged.connect(self.player_status_callback)

        # self._player.errorOccurred.connect(self._player_error)
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Clippy's chat log
        global chat_log
        chat_log = [{"role": "system", "content": "You are a helpful and sassy assistant, "
                                                  "specifically you are reincarnated Clippy from Microsoft Word. "
                                                  "Also, try to be funny, entertaining, and show some of that rizz you "
                                                  "got pleasseeee"}]

        # Bool for Clippy's talking animation
        self.talking = False

        # Initialize the UI
        self.init_ui()

    def init_ui(self):
        self.layout = QGridLayout(self)
        self.info_sentence = QLabel("Let's Have a chat!", self)
        self.chat_box = QPlainTextEdit(self)
        self.chat_box.setReadOnly(True)
        self.input_txt = QLineEdit(self)
        self.input_txt.setFocus()
        self.input_txt.returnPressed.connect(self.send_to_gpt)
        self.input_txt.setPlaceholderText("Ask a question!")
        self.send_button = QPushButton('send', self)
        # Mute Button
        self.sound_button = QPushButton('', self)
        self.sound_button.setStyleSheet("border-image: url(img/sound.png);")
        self.sound_button.setFixedSize(30, 30)
        self.sound_button.setCheckable(True)
        self.sound_button.clicked.connect(self.change_sound_style)

        # Send Question to chat GPT
        self.send_button.clicked.connect(self.send_to_gpt)
        self.think_label = QLabel("Listening ... ", self)

        # Add widgets to grid
        self.layout.addWidget(self.sound_button, 0, 1)
        self.layout.addWidget(self.info_sentence, 0, 0)
        self.layout.addWidget(self.chat_box, 1, 0, 2, 2)
        self.layout.addWidget(self.input_txt, 4, 0)
        self.layout.addWidget(self.send_button, 4, 1)
        self.layout.addWidget(self.think_label, 3, 0, 1, 1)
        self.setLayout(self.layout)

    # Changes the sound button styling to match the state
    def change_sound_style(self):
        if self.sound_button.isChecked():
            self.sound_button.setStyleSheet("border-image: url(img/silent.png);")
            self.audio_output.setVolume(0)
        else:
            self.sound_button.setStyleSheet("border-image: url(img/sound.png);")
            self.audio_output.setVolume(50)

    # Sends text from input to Chat GPT
    def send_to_gpt(self):
        question = self.input_txt.text()
        chat_log.append({"role": "user", "content": question})
        # Thread to allow gui to function while it queries chatGPT
        self.worker = Type()
        self.worker.gpt_result.connect(self.complete)
        self.chat_box.appendHtml("<b>You: </b>" + question)
        self.input_txt.clear()
        # Disable buttons to user doesn't overwhelm chatGPT
        self.input_txt.setDisabled(True)
        self.send_button.setDisabled(True)
        self.think_label.setText("Thinking ...")
        self.worker.start()

    """
    Callback function for worker thread that's sending and receiving data from chatgpt api
    Re enables the buttons
    Appends ChatGPT text to chat box
    Starts another thread for speaking
    Set talking boolean for chatting animation
    """

    def complete(self, ai_response_msg):
        self.input_txt.setFocus()
        self.chat_box.appendHtml("<b>Clippy: </b>" + ai_response_msg)

        # check if mute button is active
        if not self.sound_button.isChecked():
            self.worker_speak = LoadReply(ai_response_msg)
            self.worker_speak.done_loading_reply.connect(self.done_loading_sound)
            self.worker_speak.start()
        else:
            self.think_label.setText("Talking (telepathically)...")
            self.input_txt.setDisabled(False)
            self.send_button.setDisabled(False)

    # Callback for speech worker
    def done_loading_sound(self):
        self.think_label.setText("Listening ...")
        self.player.setSource(QUrl.fromLocalFile("talk.mp3"))
        self.player.play()
        self.input_txt.setDisabled(False)
        self.send_button.setDisabled(False)

    def player_status_callback(self, status):
        if status == QMediaPlayer.MediaStatus.BufferedMedia:
            self.talking = True
            self.think_label.setText("Talking ...")
        else:
            self.talking = False
            self.think_label.setText("Listening ...")


# Thread for ChatGPT inquiries
class Type(QThread):
    gpt_result = QtCore.pyqtSignal(object)

    def __init__(self):
        super(QThread, self).__init__()

    def run(self):
        ai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_log,
            temperature=.9
        )
        # parse for the response text
        ai_response_msg = ai_response['choices'][0]['message']['content']
        chat_log.append({"role": "assistant", "content": ai_response_msg})
        self.gpt_result.emit(ai_response_msg)


# Thread for speaking
class LoadReply(QThread):
    done_loading_reply = QtCore.pyqtSignal()

    def __init__(self, reply):
        super(QThread, self).__init__()
        QtCore.pyqtSignal()
        self.reply = reply

    # Plays Audio received from gTTS
    def run(self):
        tts = gtts.gTTS(self.reply)
        tts.save("talk.mp3")
        self.done_loading_reply.emit()
