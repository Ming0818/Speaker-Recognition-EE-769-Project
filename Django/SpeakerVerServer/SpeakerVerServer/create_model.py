import librosa
import numpy as np
import librosa.display
from hmmlearn import hmm
import os
import warnings
import time
import pickle

warnings.filterwarnings("ignore")

#Number of states per HMM
N = 50

#Num of speaker
Num_Speakers = 40

#number of utts to take per speaker
num_file_per_speaker = 10

#Number off iterations of HMM
num_iter_hmm = 10


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
	for file in os.listdir("SpeakerVerServer/train/" + id):
		
		if i > num_file_per_speaker :
			break
		i +=1
		curr_feat = mfcc_module("SpeakerVerServer/train/" + id +"/" + file)
		curr_feat = list(curr_feat)
		features += curr_feat
		lens.append(len(curr_feat))

	out = np.array(features)
	return out,lens

def create_model(my_id):
	print(my_id)	
	if ("model-" + str(my_id)) in os.listdir("SpeakerVerServer/HMM-Models/"):
		my_model_file = open('SpeakerVerServer/HMM-Models/model-'+str(my_id) ,'rb')
		model =  pickle.load(my_model_file)
		return model

	features , lens = get_final_feature(my_id)
	print("Started Training Model ", my_id)
	start_time = time.time()
	model = hmm.GaussianHMM(n_components=N, covariance_type="diag", init_params='mcs', params='mcs', n_iter=num_iter_hmm, 
							tol=1e-7, verbose=True)
	model.transmat_ = np.ones((N, N), dtype='float') / N
	model.fit(features,lens)
	pickle.dump(model,open('SpeakerVerServer/HMM-Models/model-'+str(my_id) ,'wb'))
	print("training time for ",my_id," : ", time.time() -start_time)

	names_scores_list = pickle.load(open('SpeakerVerServer/scores_test.pkl', 'rb'))
	score_list = [] 
	for file in os.listdir("SpeakerVerServer/train/" + id):
		sc = curr_model.score(mfcc_module("SpeakerVerServer/train/" + id + file)[:200,:])
		score_list.append([sc])
		names_scores_list[str(my_id)] = score_list

	pickle.dump(names_scores_list, open('SpeakerVerServer/scores_test.pkl', 'wb'))
	return model

np.random.seed(42)
