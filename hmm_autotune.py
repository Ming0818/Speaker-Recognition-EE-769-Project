import librosa
import numpy
import librosa.display
from hmmlearn import hmm
import os
import warnings
warnings.filterwarnings("ignore")

#Number of states per HMM
N = 50

#Num of speaker
Num_Speakers = 40

#number of utts to take per speaker
num_utts = 10


