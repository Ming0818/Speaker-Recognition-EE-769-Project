import os 
from random import shuffle
for root, directories, filenames in os.walk('LibriSpeech/'):
	# for directory in directories:
		# print(os.path.join(root, directory)) 
	i=0
	shuffle(filenames)
	for filename in filenames:
		if ".txt" not in filename and ".TXT" not in filename:
			if i < len(filenames)/10 : 
				# print(filename.split("-")[0])
				os.system("mkdir -p test/"+filename.split("-")[0])
				a = str(os.path.join(root,filename))
				os.system("cp " + a + " " + "test/"+filename.split("-")[0] )
			else :
				# print(filename.split("-")[0])
				os.system("mkdir -p train/"+filename.split("-")[0])
				a = str(os.path.join(root,filename))
				os.system("cp " + a + " " + "train/"+filename.split("-")[0] )
			i += 1