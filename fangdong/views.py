# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import csv
import traceback

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from fangdong.models import Landlord, Visitors, VisitRecords
from django.db import connection


def init_landlord():
    file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(file_dir, 'db/DSS_Revise_Data.csv')

    with open(file_path, encoding='utf-8') as csvfile:
        try:
            readCSV = csv.reader(csvfile, delimiter=',')
            i = 0
            titles = []
            for row in readCSV:
                if i == 0:
                    titles = row
                    print(titles)
                else:
                    if row is not None:
                        row_data = {}
                        for cel_num in range(len(titles)):
                            key = str(titles[cel_num])
                            if row[cel_num] != 'N/A' and row[cel_num] != '':
                                row_data[key] = row[cel_num]
                            else:
                                row_data[key] = None
                        print(row_data)
                        Landlord.objects.create(**row_data)
                i = i + 1
                print(i)
        except:
            traceback.print_exc()
        finally:
            csvfile.close()
    # print(landlords)
    # return landlords


def index(request):
    phone = request.GET.get("phone")
    if phone is None:
        return render(request, 'fangdong/user.html')
    if Landlord.objects.count() == 0:
        init_landlord()

    cur = connection.cursor()
    # cur.execute("SELECT count(vl.visitor_id) AS eu, l.listing_id FROM landlord l LEFT JOIN visitor_landlord_relation vl ON l.listing_id=vl.landlord_id LEFT JOIN visitors v ON v.visitor_id=vl.visitor_id AND v.phone !=%s group by l.listing_id ORDER BY eu ASC LIMIT 1", (phone,))
    cur.execute("SELECT CASE WHEN 6-count(vl.visitor_id) >0 THEN 6-count(vl.visitor_id) ELSE 7 END AS eu, l.listing_id FROM landlord l LEFT JOIN visitor_landlord_relation vl ON l.listing_id=vl.landlord_id WHERE l.listing_id NOT IN (SELECT DISTINCT landlord_id FROM visitor_landlord_relation vl JOIN visitors v ON v.visitor_id=vl.visitor_id WHERE v.phone =%s) GROUP BY l.listing_id ORDER BY eu ASC LIMIT 1", (phone,))
    landlord_tuple = cur.fetchone()
    if landlord_tuple is None:
        return render(request, 'fangdong/index.html', {})
    landlord_id = landlord_tuple[1]
    landlord_info = Landlord.objects.get(listing_id=landlord_id)
    count = Visitors.objects.filter(phone=phone).count()
    result_data = landlord_info.__dict__
    result_data['has_record'] = count > 0
    if result_data['host_verifications']:
        result_data['host_verifications'] = json.loads(result_data['host_verifications'].replace("'", "\""))
    num_range = []
    for i in range(1, 8):
        num_range.append(i)
        # if i == 0:
        #     num_range.append('{i}'.format(i=i))
        # else:
        #     num_range.append('{i}-{j}'.format(i=i*10+1, j=(i+1)*10))
    percentage_range = []
    for i in range(10):
        if i == 0:
            percentage_range.append('{i}-{j}'.format(i=i, j=(i+1)*10))
        else:
            percentage_range.append('{i}-{j}'.format(i=i*10+1, j=(i+1)*10))
    result_data['num_range'] = num_range
    result_data['percentage_range'] = percentage_range
    context = {'landlords': result_data}
    return render(request, 'fangdong/index.html', context)


# 房东和访客建立联系
def visit(request):
    phone = request.GET.get("phone")
    listing_id = request.GET.get("listing_id")
    if request.method == 'GET':
        data = Visitors.objects.filter(phone=phone).first()
        has_record = data is not None
        # 获取房东id
        if not has_record:
            visitors = Visitors()
            visitors.name = request.GET.get("name")
            visitors.gender = request.GET.get("gender")
            visitors.phone = phone
            visitors.english_level = request.GET.get("english_level")
            visitors.degree = request.GET.get("degree")
            visitors.age = request.GET.get("age")
            visitors.credulity_question1 = request.GET.get("credulity_question1")
            visitors.credulity_question2 = request.GET.get("credulity_question2")
            visitors.credulity_question3 = request.GET.get("credulity_question3")
            visitors.save()
            data = Visitors.objects.filter(phone=phone).first()

        # listing_id = request.GET.get("listing_id")
        if listing_id is not None:
            landlord = Landlord.objects.get(listing_id=listing_id)
            visit_records = VisitRecords()
            visit_records.visitor_id = data.visitor_id
            visit_records.landlord_id = landlord.listing_id
            visit_records.question1_score = request.GET.get("question1_score")
            visit_records.question2_score = request.GET.get("question2_score")
            visit_records.question3_score = request.GET.get("question3_score")
            visit_records.question4_score = request.GET.get("question4_score")
            visit_records.question5_score = request.GET.get("question5_score")
            visit_records.question6_score = request.GET.get("question6_score")
            visit_records.question7_score = request.GET.get("question7_score")
            visit_records.question8_score = request.GET.get("question8_score")
            visit_records.save()
    elif request.method == 'POST':
        data = Visitors.objects.filter(phone=phone).first()
        has_record = data is not None
        # 获取房东id
        if not has_record:
            visitors = Visitors()
            visitors.name = request.POST.get("name")
            visitors.gender = request.POST.get("gender")
            visitors.phone = phone
            visitors.english_level = request.POST.get("english_level")
            visitors.degree = request.POST.get("degree")
            visitors.age = request.GET.get("age")
            visitors.save()
            data = visitors

        # listing_id = request.POST.get("listing_id")
        if listing_id is not None:
            landlord = Landlord.objects.get(listing_id=listing_id)
            visit_records = VisitRecords()
            visit_records.visitor_id = visitors.visitor_id
            visit_records.landlord_id = landlord.listing_id
            visit_records.question1_score = request.POST.get("question1_score")
            visit_records.question2_score = request.POST.get("question2_score")
            visit_records.question3_score = request.POST.get("question3_score")
            visit_records.question4_score = request.POST.get("question4_score")
            visit_records.question5_score = request.POST.get("question5_score")
            visit_records.question6_score = request.POST.get("question6_score")
            visit_records.question7_score = request.POST.get("question7_score")
            visit_records.question8_score = request.POST.get("question8_score")
            visit_records.save()

    # result_data = data.__dict__
    # result_data['has_record'] = has_record

    return HttpResponseRedirect("/?phone=" + phone)


def logout(request):
    phone = request.GET.get("phone")
    cur = connection.cursor()
    cur.execute("SELECT count(distinct landlord_id) as ev FROM visitor_landlord_relation vl JOIN visitors v ON v.visitor_id=vl.visitor_id WHERE v.phone =%s", (phone,))
    mark_count = cur.fetchone()[0]
    context = {'mark_count': mark_count}
    return render(request, 'fangdong/logout.html', context)

