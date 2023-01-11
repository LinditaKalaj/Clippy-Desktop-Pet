import gtts as gtts
import openai as openai
import os

from playsound import playsound
from PyQt5 import QtCore
from dotenv import load_dotenv
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import *

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
        self.infoSentence.setAlignment(Qt.AlignCenter)
        self.chatBox = QPlainTextEdit(self)
        self.chatBox.setReadOnly(True)
        self.inputTxt = QLineEdit(self)
        self.inputTxt.returnPressed.connect(self.sendToChatGPT)
        self.inputTxt.setPlaceholderText("Ask a question or use the mic")
        self.sendButton = QPushButton('send', self)
        self.sendButton.clicked.connect(self.sendToChatGPT)
        self.thinkLabel = QLabel("Listening ... ", self)


        self.layout.addWidget(self.infoSentence, 0, 0, 1, 2)
        self.layout.addWidget(self.chatBox, 1, 0, 2, 2)
        self.layout.addWidget(self.inputTxt, 4, 0)
        self.layout.addWidget(self.sendButton, 4, 1)
        self.layout.addWidget(self.thinkLabel, 3, 0, 1, 2)
        self.setLayout(self.layout)

    def sendToChatGPT(self):
        print("clicked")
        question = self.inputTxt.text()
        self.worker = Type(question)
        self.worker.gptResult.connect(self.complete)
        self.chatBox.appendHtml("<b>You: </b>" + question)
        self.inputTxt.clear()
        self.inputTxt.setDisabled(True)
        self.sendButton.setDisabled(True)
        self.thinkLabel.setText("Thinking...")
        self.worker.start()
        """""
        if self.workerResponse.isRunning():
            self.chatBox.appendHtml("<b>Please wait until I'm done.</b>")

        else:
            self.chatBox.appendHtml("<b>You: </b>" + question)
            self.inputTxt.clear()
            # calling open ai
            self.workerResponse.start()
        self.workerResponse.finished.connect(self.complete())

        #self.workerResponse.start()
        #self.worker

        #self.talking = True
        #self.worker = Speak(ai_response_msg)
        #self.worker.start()
        #self.worker.finished.connect(self.complete)
        """

    # Updated talking boolean so the talking animation halts
    def complete(self, ai_response_msg):
        self.thinkLabel.setText("Listening...")
        self.inputTxt.setDisabled(False)
        self.sendButton.setDisabled(False)
        self.chatBox.appendHtml("<b>Clippy: </b>" + ai_response_msg)
        self.workerSpeak = Speak(ai_response_msg)
        self.workerSpeak.finished.connect(self.doneTalking)
        self.workerSpeak.start()
        self.talking = True
        print("done")
    
    def doneTalking(self):
        self.talking = False

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
        # self.chatBox.appendHtml("<b>Clippy: </b>" + ai_response_msg)

class Speak(QThread):
    def __init__(self, speech):
        super(QThread, self).__init__()
        self.speech = speech

    def run(self):
        tts = gtts.gTTS(self.speech)
        tts.save("talk.mp3")
        playsound("talk.mp3")
