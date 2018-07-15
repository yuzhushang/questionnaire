# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from fangdong.models import Landlord, Visitors, VisitRecords
from django.db import connection


def init_landlord():
    file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(file_dir, 'db/DSS_Revise_Data.csv')

    file_object = open(file_path, 'rb')
    # landlords = []
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
                    Landlord.objects.create(**row_data)
                    # landlords.append(row_data)
            i = i + 1
    except Exception as e:
        print(e)
    finally:
        file_object.close()
    # print(landlords)
    # return landlords


def index(request):
    phone = request.GET.get("phone")
    if phone is None:
        return render(request, 'fangdong/user.html')
    if Landlord.objects.count() == 0:
        init_landlord()

    cur = connection.cursor()
    cur.execute("SELECT count(vl.landlord_id) AS eu, l.listing_id FROM landlord l LEFT JOIN visitor_landlord_relation vl ON l.listing_id=vl.landlord_id LEFT JOIN visitors v ON v.visitor_id=vl.visitor_id AND v.phone !=%s ORDER BY eu ASC LIMIT 1", (phone,))
    landlord_id = cur.fetchone()[1]
    landlord_info = Landlord.objects.get(listing_id=landlord_id)
    count = Visitors.objects.filter(phone=phone).count()
    result_data = landlord_info.__dict__
    result_data['has_record'] = count > 0

    context = {'landlords': result_data}
    return render(request, 'fangdong/index.html', context)


# 房东和访客建立联系
def visit(request):
    phone = request.GET.get("phone")
    data = Visitors.objects.filter(phone=phone).first()
    has_record = data is not None
    # 获取房东id
    if not has_record:
        visitors = Visitors()
        visitors.name = request.GET.get("name")
        visitors.gender = request.GET.get("gender")
        visitors.phone = phone
        visitors.english_level = request.GET.get("english_level")
        visitors.save()
        data = visitors

    listing_id = request.GET.get("listing_id")
    if listing_id is not None:
        landlord = Landlord.objects.get(listing_id=listing_id)
        visit_records = VisitRecords()
        visit_records.visitor_id = visitors.visitor_id
        visit_records.landlord_id = landlord.listing_id
        visit_records.question1_score = request.GET.get("question1_score")
        visit_records.question2_score = request.GET.get("question2_score")
        visit_records.question3_score = request.GET.get("question3_score")
        visit_records.question4_score = request.GET.get("question4_score")
        visit_records.question5_score = request.GET.get("question5_score")
        visit_records.question6_score = request.GET.get("question6_score")
        visit_records.save()

    result_data = data.__dict__
    result_data['has_record'] = has_record
    return HttpResponse(repr(result_data))

