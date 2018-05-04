# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import json
from django.views.decorators.csrf import csrf_exempt
from .speaker_ident import identify_speaker
from .create_model import create_model
import os
# from .speaker_ver import verify_speaker

@csrf_exempt
def makemodel_view_api(request):
	user = request.user
	if request.method == "POST":
		name = request.POST['name']

		folder='SpeakerVerServer/train/' + name 
		fs = FileSystemStorage(location=folder)

		# myfile = request.POST['file']
		# print("dummy",request.POST['dummy'])
		# print("body", request.body)
		# print("files",request.FILES['file'])
		# print("file",myfile)
		# print('received file:',myfile['file'])
		# for file in request.FILES.keys():

		index = find_max_index(folder)
		for i, file in enumerate(request.FILES.keys()):
			myfile = request.FILES[file]
			filename = fs.save("train-" + str(index), myfile)	
			index += 1 
		
		create_model(name)

		#test the data
		data = {
			'status' : True
		}
		return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		data = {
			'status' : False
		}
		return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def identifySpeaker_view_api(request):
	user = request.user
	if request.method == "POST":
		folder='SpeakerVerServer/test/' 
		fs = FileSystemStorage(location=folder)
		# print("files",request.FILES['file'])
		# print("file",myfile)
		myfile = request.FILES['file']
		# print('received file:',myfile['file'])
		filename = fs.save(myfile.name, myfile)
		name = identify_speaker(folder + filename)	
		print(name)

		os.remove(folder + filename)

		#test the data
		data = {
			'status' : True,
			'data' : name
		}
		return HttpResponse(json.dumps(data), content_type='application/json')	
	else:
		return HttpResponse(1)

@csrf_exempt
def verifySpeaker_view_api(request):
	user = request.user

	if request.method == "POST":
		folder='SpeakerVerServer/test' 
		fs = FileSystemStorage(location=folder)
		# print("files",request.FILES['file'])
		# print("file",myfile)
		myfile = request.FILES['file']
		# print('received file:',myfile['file'])
		filename = fs.save(myfile.name, myfile)
		#test the data

		os.remove(filename)

		data = {
			'status' : True,
			'data' : name
		}

		return HttpResponse(json.dumps(data), content_type='application/json')	
	else:
		return HttpResponse(1)


def find_max_index(dir):
	max_index = 0
	
	if not os.path.exists(dir):
		return 0

	for file in os.listdir(dir):
		index = int(file.split("-")[1])
		if index > max_index:
			max_index = index
	if max_index == 0:
		return 1
	return max_index + 1