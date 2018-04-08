import librosa
import numpy as np
import librosa.display
# from hmmlearn import hmm
import os


data = "84-121550-0011.flac"
y , sr = librosa.load(data , sr=None)
print(y,len(y),np.shape(y),sr)
print("---------------")
mfcc = librosa.feature.mfcc(y=y, sr=sr,n_mfcc=13,hop_length=int(0.010*sr), n_fft=int(0.025*sr))
print(mfcc,len(mfcc),np.shape(mfcc))
print("+++++++++++++++++++++++")
mfcc_delta =  librosa.feature.delta(mfcc,order =1)
mfcc_double_delta =  librosa.feature.delta(mfcc,order =2)
array = np.append(mfcc,mfcc_delta,axis=0)
array = np.append(array,mfcc_double_delta,axis=0)
print(len(array.T))