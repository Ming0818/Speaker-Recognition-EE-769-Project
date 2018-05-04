import librosa
import numpy as np
import librosa.display
from hmmlearn import hmm
import os
import warnings
import time
import pickle

from .speaker_ident import *

warnings.filterwarnings("ignore")

curr_dir = "SpeakerVerServer/"


def verify_speaker(file, name):

	scores_list = pickle.load(open('SpeakerVerServer/scores_test.pkl', 'rb'))
	print(name)
	print(scores_list)
	if not os.path.exists(curr_dir + 'HMM-Models/model-' + name):
		return "No model Defined", 0

	curr_model = pickle.load(open(curr_dir + 'HMM-Models/model-' + name, 'rb'))
	sc = curr_model.score(mfcc_module(file)[:200,:])

	mean = sum(scores_list[name]) * 1.0 / len(scores_list[name])

	if sc > scores_list[name][-1]:
		return np.exp(sc), 1
	else:
		return np.exp(sc), 0
