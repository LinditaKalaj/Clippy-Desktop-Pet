import platform
import gtts as gtts
import openai as openai
import os

from PyQt5 import QtCore
from dotenv import load_dotenv
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import *
from playsound import playsound

# Chatbox class/gui for Clippy
class ClippyChat(QWidget):
    def __init__(self):
        super(ClippyChat, self).__init__()
        # Load dot env file and pass API key to open.ai
        self.d = None
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Bool for clippy's talking animation
        self.talking = False

        # Initialize the UI
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.infoSentence = QLabel("Let's Have a chat!", self)
        self.infoSentence.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.infoSentence.setAlignment(Qt.AlignRight)
        self.chatBox = QPlainTextEdit(self)
        self.chatBox.setReadOnly(True)
        self.inputTxt = QLineEdit(self)
        self.inputTxt.setFocus(True)
        self.inputTxt.returnPressed.connect(self.sendToChatGPT)
        self.inputTxt.setPlaceholderText("Ask a question!")
        self.sendButton = QPushButton('send', self)
        # Mute Button
        self.soundButton = QPushButton('', self)
        self.soundButton.setStyleSheet("border-image: url(img/sound.png);")
        self.soundButton.setFixedSize(30, 30)
        self.soundButton.setCheckable(True)
        self.soundButton.clicked.connect(self.changeSoundButton)

        # Send Question to chat GPT
        self.sendButton.clicked.connect(self.sendToChatGPT)
        self.thinkLabel = QLabel("Listening ... ", self)

        # Add widgets to grid
        self.layout.addWidget(self.soundButton, 0, 1, alignment=QtCore.Qt.AlignRight)
        self.layout.addWidget(self.infoSentence, 0, 0)
        self.layout.addWidget(self.chatBox, 1, 0, 2, 2)
        self.layout.addWidget(self.inputTxt, 4, 0)
        self.layout.addWidget(self.sendButton, 4, 1)
        self.layout.addWidget(self.thinkLabel, 3, 0, 1, 2)
        self.setLayout(self.layout)

    # Changes the sound button styling to match the state
    def changeSoundButton(self):
        if self.soundButton.isChecked():
            self.soundButton.setStyleSheet("border-image: url(img/silent.png);")
        else:
            self.soundButton.setStyleSheet("border-image: url(img/sound.png);")

    # Sends text from input to Chat GPT
    def sendToChatGPT(self):
        question = self.inputTxt.text()
        # Thread to allow gui to function while it queries chatGPT
        self.worker = Type(question)
        self.worker.gptResult.connect(self.complete)
        self.chatBox.appendHtml("<b>You: </b>" + question)
        self.inputTxt.clear()
        # Disable buttons to user doesnt overwhelm chatGPT
        self.inputTxt.setDisabled(True)
        self.sendButton.setDisabled(True)
        self.thinkLabel.setText("Thinking ...")
        self.worker.start()

    """
    Callback function for worker thread thats sending and receiving data from chatgpt api
    Re enables the buttons
    Appends ChatGPT text to chatbox
    Starts another thread for speaking
    Set talking boolean for chatting animation
    """ 
    def complete(self, ai_response_msg):
        self.thinkLabel.setText("Talking ...")
        self.inputTxt.setDisabled(False)
        self.sendButton.setDisabled(False)
        self.inputTxt.setFocus(True)
        self.chatBox.appendHtml("<b>Clippy: </b>" + ai_response_msg)

        # check if mute button is active
        if not self.soundButton.isChecked():
            self.workerSpeak = Speak(ai_response_msg)
            self.workerSpeak.talkingEnded.connect(self.doneTalking)
            self.workerSpeak.start()
            self.talking = True
    
    #Callback for speech worker
    def doneTalking(self):
        self.thinkLabel.setText("Listening ...")
        self.talking = False

#Thread for ChatGPT inquiries
class Type(QThread):
    gptResult = QtCore.pyqtSignal(object)
    def __init__(self, text):
        super(QThread, self).__init__()
        self.text = text

    def run(self):
        ai_response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.text,
            temperature=1,
            max_tokens=2000,
        )
        # parse for the response text
        ai_response_msg = ai_response.choices[0].text
        print(ai_response_msg)
        self.gptResult.emit(ai_response_msg)
#Thread for speaking
class Speak(QThread):
    talkingEnded = QtCore.pyqtSignal()
    def __init__(self, speech):
        super(QThread, self).__init__()
        endPlay = QtCore.pyqtSignal()
        self.speech = speech
    # Plays Audio received from gTTS
    def run(self):
        tts = gtts.gTTS(self.speech)
        tts.save("talk.mp3")
        playsound("talk.mp3")
        os.remove("talk.mp3")
        self.talkingEnded.emit()
