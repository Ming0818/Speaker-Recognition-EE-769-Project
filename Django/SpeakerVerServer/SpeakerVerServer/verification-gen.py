import librosa
import numpy as np
import librosa.display
from hmmlearn import hmm
import os
import warnings
import time
import pickle

def mfcc_module(data):
	y , sr = librosa.load(data , sr=None)
	mfcc = librosa.feature.mfcc(y=y, sr=sr,n_mfcc=13,hop_length=int(0.010*sr), n_fft=int(0.025*sr))
	mfcc_delta =  librosa.feature.delta(mfcc,order =1)
	mfcc_double_delta =  librosa.feature.delta(mfcc,order =2)
	array = np.append(mfcc,mfcc_delta,axis=0)
	array = np.append(array,mfcc_double_delta,axis=0)
	return array.T

def get_final_feature(id):
	lens = []
	features = []
	i = 0
	for file in os.listdir("train/"+str(id)):
		if i > num_file_per_speaker :
			break
		i +=1
		curr_feat = mfcc_module("train/"+str(id)+"/"+file)
		curr_feat = list(curr_feat)
		features += curr_feat
		lens.append(len(curr_feat))
	out = np.array(features)
	return out,lens

def identify_speaker(input_file_name):
	id_to_name = {}

	curr_dir = "SpeakerVerServer/"

	print(os.getcwd())

	# with open(curr_dir + 'HMM-Models/id_to_name.pkl', 'rb') as f:
	# 	id_to_name =  pickle.load(f)

	max_score = -float('inf')
	max_id = -1

	score_list = []

	for i in os.listdir(curr_dir + 'HMM-Models/'):
		curr_model = pickle.load(open(curr_dir + 'HMM-Models/' + i, 'rb'))
		sc = curr_model.score(mfcc_module(input_file_name)[:200,:])
		score_list.append([sc, i.split('-')[1]])
		
	score_list.sort()
	
	return id_to_name[score_list[0][1]]


model_name_list = []
for file in os.listdir('HMM-Models/'):
	model_name_list.append(file.split('-')[1])

model_list_with_scores = {}

for model in model_list:

	score_list = [] 

	curr_model = pickle.load(open('HMM-Models/model-' + model, 'rb'))
		
	for test_file in os.listdir( 'OrigData/test/' + model + "/"):
		sc = curr_model.score(mfcc_module(curr_dir + 'OrigData/test/' + model + "/" + test_file)[:200,:])
		score_list.append([sc, i.split('-')[1]])

	model_list_with_scores[model] = score_list.sort()
