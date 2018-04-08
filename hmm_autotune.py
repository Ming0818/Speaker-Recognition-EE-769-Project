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
Num_Speakers =40

#number of utts to take per speaker
num_file_per_speaker = 10

#Number off iterations of HMM
num_iter_hmm = 10


#Number of test audios per user to be tested
test_limit = 10


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

def create_model(n_states,my_id):
	print(my_id)
	dir_name = "Tr_" + str(N) + "_" + str(Num_Speakers) + "_" + str(num_file_per_speaker) + "_"+str(num_iter_hmm)
	if ("model-" + str(my_id)) in os.listdir("Models/"+ dir_name):
		my_model_file = open('Models/'+dir_name + '/model-'+str(my_id) ,'rb')
		model =  pickle.load(my_model_file)
		return model

	features , lens = get_final_feature(my_id)
	print("Started Training Model ", my_id)
	start_time = time.time()
	model = hmm.GaussianHMM(n_components=N, covariance_type="diag", init_params='mcs', params='mcs', n_iter=num_iter_hmm, 
							tol=1e-7, verbose=True)
	model.transmat_ = np.ones((N, N), dtype='float') / N
	model.fit(features,lens)
	pickle.dump(model,open('Models/'+dir_name+'/model-'+str(my_id) ,'wb'))
	print("training time for ",my_id," : ", time.time() -start_time)
	return model

np.random.seed(42)
id_list = os.listdir("./train")
speaker_list = []
model_list = []
num = 0
print("id list :",id_list)

directory_name = "Tr_" + str(N) + "_" + str(Num_Speakers) + "_" + str(num_file_per_speaker) + "_"+str(num_iter_hmm)
if not directory_name in os.listdir('Models'):
	os.system('mkdir -p Models/'+directory_name)
for i in id_list :
	if num > Num_Speakers:
		break
	num +=1
	my_id = int(i)
	model_list.append([create_model(N,my_id),my_id])
	speaker_list.append(my_id)

print("speaker :",speaker_list)
actual_list = []
pred_list = []


for i in id_list:
	if int(i) in speaker_list:
		test_num =0
		for j in os.listdir("./test/"+i):
			if test_num >= test_limit :
				break
			test_num += 1
			my_start_time = time.time()
			max_score = -float('inf')
			index = 0
			for k in range(len(model_list)):
				score = model_list[k][0].score(mfcc_module("test/"+i+"/"+j)[:200,:])
				if max_score < score:
					index = k
					max_score = score
			# print("i is :",i)
			pred_list.append(model_list[index][1])
			actual_list.append(int(i))
			print("testing time for ",i,j," : ",time.time() - my_start_time)

print("pred list :",pred_list)
print("actual list :",actual_list)

count = 0.0
for i in range(0,len(actual_list)):
    if actual_list[i] == pred_list[i]:
    	count += 1

print(((count*1.0)/len(actual_list))*100)
	

