# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from fangdong.models import Landlord, Visitors


def init_landlord():
    file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(file_dir, 'db/DSS_Revise_Data.csv')

    file_object = open(file_path, 'rb')
    landlords = []
    try:
        i = 0
        titles = []
        for line in file_object:
            if i == 0:
                titles = str(line).replace("\\r\\n'", "").replace("b'", "").strip().split(",")
                print(titles)
            else:
                if line is not None:
                    row = str(line).replace("\\r\\n'", "").replace("b'", "").strip().split(",")
                    row_data = {}
                    for cel_num in range(len(titles)):
                        key = str(titles[cel_num])
                        if row[cel_num] != 'N/A':
                            row_data[key] = row[cel_num]
                        else:
                            row_data[key] = None
                    landlords.append(row_data)
            i = i + 1
    except Exception as e:
        print(e)
    finally:
        file_object.close()
    # print(landlords)
    return landlords


def index(request):
    landlords = Landlord.objects.all()
    if len(landlords) == 0:
        landlords = init_landlord()
        for landlord_info in landlords:
            landlord = Landlord()
            landlord.listing_id = landlord_info['listing_id']
            Landlord.objects.create(**landlord_info)
    print(landlords)
    context = {'landlords': landlords[0:2]}
    return render(request, 'fangdong/index.html', context)


def visit(request):
    phone = request.GET.get("phone")
    data = Visitors.objects.filter(phone=phone).first()
    if data is not None:
        return HttpResponse(repr(data.__dict__))
    visitors = Visitors()
    visitors.name = request.GET.get("name")
    visitors.gender = request.GET.get("gender")
    visitors.phone = phone
    visitors.english_level = request.GET.get("english_level")
    visitors.save()

    return HttpResponse(repr(data.__dict__))

