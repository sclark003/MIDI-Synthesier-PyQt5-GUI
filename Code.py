from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, \
    QSlider, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
import sys
import mido
import sounddevice as sd
import oscillator as o

#Create QObject to listen for MIDI messages
class MidiPortReader(QObject):
    #Create signal for when a MIDI note_on message arrives
    newNoteFrequency = pyqtSignal(float)
    #Initialise Object
    def __init__(self):
        QObject.__init__(self)
        #Open MIDI input port to recieve MIDI messages
		self.port = mido.open_input('pipes',virtual=True)
    
    #Create function to recieve MIDI messages, calculate note
	#Frequency, and to emit the new frequency as a PyQt5 signal
    def listener(self):
        for msg in self.port:
            m = str(msg)
            #Select the relevant parts of the recieved MIDI message
			#Here this is the note number
			a = m[23]
            b = m[24]
			#Select the part of the MIDI message to distinguish if
			#this is a 'note_on' or 'note_off'
            z = m[6]
			#If the message is 'note_on', emit the note frequency
            if (z=="n"):
                note = int(a+b)
                f = 27.5*2**((note-21)/12)
                self.newNoteFrequency.emit(f)
    


#Create QWidget to produce GUI (main thread)
class Control(QWidget):
    
	#Set-up signals and variables
    fs = 44100
    v = 0
    wave = 0
    s = o.Oscillate()

	#Initialise object
    def __init__(self, parent = None):
        super().__init__(parent)
        
        #Create worker(MidiPortReader) thread inside QWidget
        self.obj = MidiPortReader()
        self.thread = QThread()
        #Connect worker's signal to GUI slot
        self.obj.newNoteFrequency.connect(self.noteplay)
        #Move the worker object to the thread object
        self.obj.moveToThread(self.thread)
        #Start thread
        self.thread.start()    
        #Start GUI
        self.create_UI()

    #Create GUI
    def create_UI(self):
        #Create slider/buttons
        self.Slider1 = QSlider(Qt.Horizontal)
        self.label = QLabel("Volume")
        self.sib = QPushButton(self.tr('Sine Wave'))
        self.sqb = QPushButton(self.tr('Square Wave'))
        self.exb = QPushButton(self.tr('Exit'))
        
		#Set button colours
        self.sib.setStyleSheet("background-color: red")
        self.sqb.setStyleSheet("background-color: red")

        #Build horizontal layout
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.sib)
        hLayout.addStretch(1)
        hLayout.addWidget(self.sqb)

        #Build vertical layout
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(self.label)
        vLayout.addWidget(self.Slider1)
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.exb)
        
		#Connect buttons to slots
        self.Slider1.valueChanged[int].connect(self.sliderClicked)
        self.showb.clicked.connect(self.sliderClicked)
        #If exit button pressed, exit application
		self.exb.clicked.connect(app.exit)        
        self.sib.clicked.connect(self.sineClicked)
        self.sqb.clicked.connect(self.squareClicked)
        self.obj.newNoteFrequency.connect(self.noteplay)
    
    #Create slots
	
	#If sine wave is selected, set 'wave' variable to '0'
    @pyqtSlot()
    def sineClicked(self):
        self.wave = 0

	#If square wave is selected, set 'wave' variable to '1'   
    @pyqtSlot()
    def squareClicked(self):
        self.wave = 1
     
	#If slider is moved, set 'v' variable to new slider value
    @pyqtSlot()
    def sliderClicked(self):
        self.v = self.Slider1.value()
       #Do not accept slider value of zero as volume of zero
	   #means zero output
	   if (self.v==0):
            self.v = 1

    #Create function to play note using C++ oscillator class
    @pyqtSlot(float)
	#Slot receieves frequency value from listener thread
    def noteplay(self,f):
       #print("frequency:",f)
       #print("volume:",self.v)
       #print("wave:",self.wave)
       #If 'wave' variable is set to 0, use sine wave oscillator
	   if (self.wave==0):
           #print("sine")
            b = self.s.wavesine(self.fs,f)
			#adjust note volume based on 'v' variable value
            note = (1/1000000*f)*b*self.v
			#play array to generate sound
            sd.play(note, self.fs)
       #If 'wave' variable is set to 1, use square wave oscillator
        if (self.wave==1):
           #print("square")
            b = self.s.wavesquare(self.fs,f,0.7)
			#adjust note volume based on 'v' variable value
            note = 0.001*b*self.v
			#play array to generate sound
            sd.play(note, self.fs)



app = QApplication(sys.argv)
window = Control()
window.show()
sys.exit(app.exec_())