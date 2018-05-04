# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import json
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def makemodel_view(request):
	user = request.user
	if request.method == "POST":
		folder='../' 
		fs = FileSystemStorage(location=folder)
		# myfile = request.POST['file']
		print("dummy",request.POST['dummy'])
		print("files",request.FILES['file'])
		# print("file",myfile)
		myfile = request.FILES['file']
		# print('received file:',myfile['file'])
		filename = fs.save(myfile.name, myfile)	
		data = {
			'dummy1' : '1',
			'dummy2' : '2'
		}
		return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		data = {
			'dumm1' : '1'
		}
		print(request.POST)
		return HttpResponse(json.dumps(data), content_type='application/json')


def recogspeaker_view(request):
	if request.method!="POST":
		return HttpResponse(-1)
	else:
		reviewID = request.POST['reviewID']
		review = Review.objects.get(ID=reviewID)
		review.delete()
		return HttpResponse(1)
