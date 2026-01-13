import random
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import yfinance as yf


# Create your views here.
from myapp.models import *
from django.contrib.auth.models import User,Group

from stock_riskanalysis import settings


def admin_home(request):
    return render(request,'admin_module/index.html')

def login_get(request):
    return render(request,'admin_module/loginn.html')

def loginpost(request):
    uname=request.POST['uname']
    password=request.POST['pwrd']
    user = authenticate(request, username=uname, password=password)
    if user is not None:
        if user.groups.filter(name="admin").exists():
            login(request,user)
            return redirect('/myapp/adminhome/')
        elif user.groups.filter(name="expert").exists():
            login(request,user)
            return redirect('/myapp/expert_home/')
        elif user.groups.filter(name="company").exists():
            ob=company_table.objects.get(LOGIN=user)
            if ob.status == 'Accepted':
                login(request, user)
                return redirect('/myapp/company_home/')
            else:
                print('brrr')
                messages.warning(request,'You are not Approved yet.')
                return redirect('/')
        else:
            messages.warning(request,"invalid username or password")
            return redirect('/')
    else:
        messages.warning(request, "invalid username or password")
        return redirect('/')

def add_expert(request):
    return render(request,'admin_module/expert.html')
def add_expertpost(request):
    name=request.POST['Name']
    email=request.POST['E-mail']
    phone=request.POST['Phone']
    place=request.POST['Place']
    pincode=request.POST['Pincode']
    district=request.POST['District']
    uname=request.POST['Username']
    password=request.POST['Password']
    photo=request.FILES["photo"]
    user=User.objects.create(username=uname,password=make_password(password),email=email,first_name=name)
    user.save()
    user.groups.add(Group.objects.get(name="expert"))

    obj=expert_table()
    obj.name=name
    obj.email=email
    obj.phone=phone
    obj.place=place
    obj.pincode=pincode
    obj.district=district
    obj.photo=photo
    obj.LOGIN=user


    obj.save()
    return redirect('/myapp/view_expert/')


def edit_expert(request,id):
    request.session['eid']=id
    obj=expert_table.objects.get(id=request.session['eid'])

    return render(request,'admin_module/editexpert.html',{"data":obj})

def edit_expertpost(request):
    name=request.POST['Name']
    # email=request.POST['E-mail']
    phone=request.POST['Phone']
    place=request.POST['Place']
    pincode=request.POST['Pincode']
    district=request.POST['District']
    photo=request.FILES.get("photo")

    obj=expert_table.objects.get(id=request.session['eid'])
    obj.name=name
    # obj.email=email
    obj.phone=phone
    obj.place=place
    obj.pincode=pincode
    obj.district=district
    if photo:
        obj.photo=photo
    obj.save()
    return redirect('/myapp/view_expert/')

def delete_expert(request,id):
    obj=User.objects.get(id=id)
    obj.delete()
    return redirect('/myapp/view_expert/')


def view_expert(request):
    data=expert_table.objects.all()
    return render(request,'admin_module/viewexpert.html',{"data":data})


def forgot_password(request):
    return render(request,'admin_module/frgtpass.html')
def send_reply(request,id):
    reply=request.POST['reply']
    ob=complaint.objects.get(id=id)
    ob.reply=reply
    ob.save()
    return redirect('/myapp/view_complaints/#about')

def change_password(request):
    return render(request,'admin_module/chngpass.html')

def change_passwordpost(request):
    current_password = request.POST['Current Password']
    new_password = request.POST['New Password']
    confirm_password = request.POST['Confirm Password']

    if new_password == confirm_password:
        print(request.user)
        f=check_password(current_password,request.user.password)
        if f:
            user=request.user
            user.set_password(new_password)
            user.save()

            logout(request)
            messages.success(request,'password changes successfully.')
            return redirect('/myapp/')
        else:
            messages.warning(request, 'Invalid Current Password.')
            return redirect('/myapp/change_password/#about')
    else:
        messages.warning(request, 'new password and confirm password are not equal')
        return redirect('/myapp/change_password/#about')



def view_complaints(request):
    data=complaint.objects.all()
    return render(request,'admin_module/viewcomplaints.html',{"data":data})


def view_companyreview(request):
    ob = company_review.objects.all()
    return render(request,'admin_module/cmpnyreview.html',{'data':ob})

def view_user(request):
    ob = user_table.objects.all()
    return render(request,'admin_module/viewuser.html',{'data':ob})

def view_appfeedback(request):
    ob = feedback.objects.all()
    return render(request,'admin_module/appfeedbck.html',{'data':ob})

def verify_company(request):
    data = company_table.objects.all()
    return render(request,'admin_module/verifycmpny.html',{'data':data})

def AcceptCompany(request,id):
    ob = company_table.objects.get(id=id)
    ob.status='Accepted'
    ob.save()
    return redirect('/myapp/verify_company/')

def RejectCompany(request,id):
    ob = company_table.objects.get(id=id)
    ob.status='Rejected'
    ob.save()
    return redirect('/myapp/verify_company/')

def view_stock(request,id):
    ob=stock_table.objects.filter(COMPANY__id=id)
    return render(request,'admin_module/viewstock.html',{'data':ob})








##############expert#####################

def expert_home(request):
    return render(request,'expert/expert_index.html')


def Add_newtip(request):
    return render(request,'expert/Addnewtip.html')

def Add_newtippost(request):
    tip = request.POST['tip']
    details = request.POST['details']


    ob=tips()
    ob.EXPERT = expert_table.objects.get(LOGIN_id=request.user.id)
    ob.tiptitle=tip
    ob.description=details
    ob.date=datetime.now().today()
    ob.save()
    return redirect('/myapp/manage_tips/')


def expert_change_password(request):
    return render(request,'expert/change_password.html')


def expert_change_passwordpost(request):
    current_password = request.POST['Current Password']
    new_password = request.POST['New Password']
    confirm_password = request.POST['Confirm Password']

    if new_password == confirm_password:
        print(request.user)
        f = check_password(current_password, request.user.password)
        if f:
            user = request.user
            user.set_password(new_password)
            user.save()

            logout(request)
            messages.success(request, 'password updated successfully.')
            return redirect('/myapp/')
        else:
            messages.warning(request, 'Incorrect current password.')
            return redirect('/myapp/expert_change_password/#about')
    else:
        messages.warning(request, 'current password and new password are not equal')
        return redirect('/myapp/expert_change_password/#about')

def manage_tips(request):
    ab=tips.objects.all()
    return render(request,'expert/managetips.html',{'data':ab})


def delete_tip(request,id):
    ab=tips.objects.get(id=id)
    ab.delete()

    return redirect('/myapp/manage_tips/')

def expert_send_reply(request,id):
    ob=doubt.objects.get(id=id)
    ob.reply=request.POST['reply']
    ob.save()
    return redirect('/myapp/view_doubt/')
def view_doubt(request):
    ob=doubt.objects.filter(EXPERT__LOGIN__id=request.user.id)
    return render(request,'expert/view_doubt.html',{'data':ob})
def view_users(request):
    return render(request,'expert/view_users.html')
def view_company(request):
    ob=company_table.objects.all()
    return render(request,'expert/viewcompany.html',{'data':ob})

def ExpertViewStock(request,id):
    ob=stock_table.objects.filter(COMPANY__id=id)
    return render(request,'expert/viewstocks.html',{'data':ob})

def view_profile(request):
    ob=expert_table.objects.get(LOGIN_id=request.user.id)
    return render(request,'expert/viewprofile.html',{"data":ob})


def UpdateProfile(request):
    name=request.POST['Name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['Place']
    pincode=request.POST['Pincode']
    district=request.POST['District']
    photo=request.FILES.get("photo")

    obj=expert_table.objects.get(LOGIN__id=request.user.id)
    obj.name=name
    # obj.email=email
    obj.phone=phone
    obj.place=place
    obj.pincode=pincode
    obj.district=district
    if photo:
        obj.photo=photo
    obj.save()
    return redirect('/myapp/view_profile/')



##############################Company#######################



def company_home(request):
    return render(request,'company/company_index.html')

def CompanyRegistration(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        sinceyear=request.POST['sinceyear']
        proof=request.FILES['proof']
        photo=request.FILES['photo']
        place=request.POST['place']
        pincode=request.POST['pincode']
        state=request.POST['state']
        district=request.POST['district']
        longitude=request.POST['longitude']
        latitude=request.POST['latitude']
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.success(request,'User with this username already exists.')
            return redirect('/myapp/')
        if User.objects.filter(email=email).exists():
            messages.success(request,'User with this email already exists.')
            return redirect('/myapp/')
        user=User.objects.create(username=username,password=make_password(password),email=email,first_name=name)
        user.save()
        user.groups.add(Group.objects.get(name='company'))
        obj=company_table()
        obj.name=name
        obj.email=email
        obj.phone=phone
        obj.place=place
        obj.pincode=pincode
        obj.district=district
        obj.longtitude=longitude
        obj.latitude=latitude
        obj.sinceyear=sinceyear
        obj.proof=proof
        obj.state=state
        obj.photo=photo
        obj.status='pending'
        obj.LOGIN=user
        obj.save()
        messages.success(request, 'Registration Successful Wait to be verified .')
        return redirect('/myapp/')
    return render(request,'company/registrations.html')

def CompanyViewStock(request):
    ob=stock_table.objects.filter(COMPANY__LOGIN__id=request.user.id)
    return render(request,'company/managestock.html',{"data":ob})

def CompanyAddStock(request):
    name=request.POST['name']
    price=request.POST['price']
    details=request.POST['details']
    company=company_table.objects.get(LOGIN__id=request.user.id)
    obj=stock_table()
    obj.name=name
    obj.price=price
    obj.details=details
    obj.photo=company.photo
    obj.COMPANY_id=company.id
    obj.save()
    return redirect('/myapp/CompanyViewStock/')

def CompanyEditStock(request):
    name=request.POST['name']
    price=request.POST['price']
    details=request.POST['details']
    obj=stock_table.objects.get(id=request.POST['id'])
    obj.name=name
    obj.price=price
    obj.details=details
    obj.save()
    return redirect('/myapp/CompanyViewStock/')

def CompanyDeleteStock(request,id):
    obj=stock_table.objects.get(id=id)
    obj.delete()
    return redirect('/myapp/CompanyViewStock/')

def CompanyViewTips(request):
    ob=tips.objects.all()
    return render(request,'company/viewtips.html',{"data":ob})

def CompanyViewProfile(request):
    ob=company_table.objects.get(LOGIN__id=request.user.id)
    return render(request,'company/manageprofile.html',{"company":ob})

def CompanyUpdateProfile(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    sinceyear = request.POST['sinceyear']
    place = request.POST['place']
    pincode = request.POST['pincode']
    state = request.POST['state']
    district = request.POST['district']
    obj = company_table.objects.get(LOGIN__id=request.user.id)
    obj.name = name
    obj.email = email
    obj.phone = phone
    obj.place = place
    obj.pincode = pincode
    obj.district = district
    obj.sinceyear = sinceyear
    if 'proof' in request.FILES:
        proof = request.FILES['proof']
        obj.proof = proof
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        obj.photo = photo
    obj.state = state
    obj.save()
    return redirect('/myapp/CompanyViewProfile/')


def CompanyChangePassword(request):
    if request.method == 'POST':
        current_password = request.POST['Current Password']
        new_password = request.POST['New Password']
        confirm_password = request.POST['Confirm Password']

        if new_password == confirm_password:
            print(request.user)
            f = check_password(current_password, request.user.password)
            if f:
                user = request.user
                user.set_password(new_password)
                user.save()

                logout(request)
                messages.success(request, 'password updated successfully.')
                return redirect('/myapp/')
            else:
                messages.warning(request, 'Invalid Current Password.')
                return redirect('/myapp/CompanyChangePassword/#about')
        else:
            messages.warning(request, 'new password and confirm password are not equal')
            return redirect('/myapp/CompanyChangePassword/#about')
    else:
        return render(request,'company/changepassword.html')

def ViewReviewRatings(request):
    ob=company_review.objects.filter(COMPANY__LOGIN__id=request.user.id)
    return render(request,'company/view_reviews.html',{"data":ob})

def CompanyDailyUpdateStock(request,id):
    obj=StockDailyHistory.objects.filter(STOCK__id=id).order_by('date')
    request.session['sid']=id
    return render(request,'company/view_daily_update.html',{"data":obj})

def CompanyDailyUpdateStockPost(request):
    starting=request.POST['starting']
    ending=request.POST['ending']
    sid = request.session['sid']
    obj=StockDailyHistory()
    obj.STOCK_id=sid
    obj.starting=starting
    obj.ending=ending
    obj.date=datetime.today()
    obj.save()
    ob=stock_table.objects.get(id=sid)
    ob.price=starting
    ob.save()
    return redirect(f'/myapp/CompanyDailyUpdateStock/{sid}')

def DeleteDailyStockData(request,id):
    sid = request.session['sid']
    StockDailyHistory.objects.get(id=id).delete()
    return redirect(f'/myapp/CompanyDailyUpdateStock/{sid}')






####################User###########################

def FlutterLogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.groups.filter(name='user').exists():
            login(request, user)
            return JsonResponse({'status':'ok','lid':user.id,'username':user.username})
        else:
            return JsonResponse({'status':'fail'})
    else:
        return JsonResponse({'status':'fail'})

def UserRegistration(request):
    name=request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    place = request.POST['place']
    pincode = request.POST['pincode']
    district = request.POST['district']
    photo = request.FILES['photo']
    username = request.POST['username']
    password = request.POST['password']
    ob=user_table()
    ob.name=name
    ob.email=email
    ob.phone=phone
    ob.place=place
    ob.pincode=pincode
    ob.district=district
    ob.photo=photo
    if User.objects.filter(username=username).exists():
        return JsonResponse({'status':'exists'})
    if User.objects.filter(email=email).exists():
        return JsonResponse({'status':'email'})
    user=User.objects.create(username=username,password=make_password(password),email=email,first_name=name,last_name=name)
    user.save()
    user.groups.add(Group.objects.get(name='user'))
    ob.LOGIN=user
    ob.save()
    return JsonResponse({'status':'ok'})

def SendComplaint(request):
    lid=request.POST['lid']
    complaints=request.POST['complaint']
    ob=complaint()
    ob.complaint=complaints
    ob.reply='pending'
    ob.date=datetime.today()
    ob.USER=user_table.objects.get(LOGIN__id=lid)
    ob.save()
    return JsonResponse({'status':'ok'})

def UserViewComplaints(request):
    lid=request.POST['lid']
    ob=complaint.objects.filter(USER__LOGIN__id=lid)
    mdata=[]
    for i in ob:
        data={
            'complaint':i.complaint,
            'reply':i.reply,
            'date':str(i.date),
        }
        mdata.append(data)
    return JsonResponse({'status':'ok','data':mdata})

def UserSendAppFeedback(request):
    lid=request.POST['lid']
    feedbacks=request.POST['feedback']
    rating=request.POST['rating']
    ob=feedback()
    ob.feedback=feedbacks
    ob.rating=rating
    ob.date=datetime.today()
    ob.USER=user_table.objects.get(LOGIN__id=lid)
    ob.save()
    return JsonResponse({'status':'ok'})

def UserViewAppRating(request):
    ob=feedback.objects.all()
    mdata=[]
    for i in ob:
        data={
            'user':i.USER.name,
            'photo':i.USER.photo.url,
            'feedback':i.feedback,
            'rating':str(i.rating),
            'date':str(i.date),

        }
        mdata.append(data)
    return JsonResponse({'status':'ok','data':mdata})

def UserViewProfile(request):
    lid=request.POST['lid']
    ob=user_table.objects.get(LOGIN__id=lid)
    data={
        'name':ob.name,
        'email':ob.email,
        'phone':ob.phone,
        'place':ob.place,
        'pincode':ob.pincode,
        'district':ob.district,
        'photo':ob.photo.url,
    }
    return JsonResponse({'status':'ok','data':data})

def UserChangePassword(request):
    lid=request.POST['lid']
    current_password = request.POST['current_password']
    new_password = request.POST['new_password']
    user = User.objects.get(id=lid)
    f = check_password(current_password, user.password)
    if f:
        user = user
        user.set_password(new_password)
        user.save()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'fail'})

def UserViewExperts(request):
    ob=expert_table.objects.all()
    mdata=[]
    for i in ob:
        data={
            'eid':i.id,
            'expert':i.name,
            'email':i.email,
            'phone':i.phone,
            'district':i.district,
            'photo':i.photo.url,
        }
        mdata.append(data)
    return JsonResponse({'status':'ok','data':mdata})

def UserAskDoubt(request):
    lid=request.POST['lid']
    eid=request.POST['eid']
    doubts=request.POST['doubt']
    ob=doubt()
    ob.doubt=doubts
    ob.reply='pending'
    ob.USER=user_table.objects.get(LOGIN__id=lid)
    ob.EXPERT=expert_table.objects.get(id=eid)
    ob.date=datetime.today()
    ob.save()
    return JsonResponse({'status':'ok'})

def UserViewDoubts(request):
    lid=request.POST['lid']
    eid=request.POST['eid']
    print(lid,eid)
    ob=doubt.objects.filter(USER__LOGIN__id=lid,EXPERT__id=eid)
    mdata=[]
    for i in ob:
        data={
            'doubt':i.doubt,
            'reply':i.reply,
            'date':str(i.date),
        }
        mdata.append(data)
    print(mdata)
    return JsonResponse({'status':'ok','data':mdata})

def ViewCompanies(request):
    ob=company_table.objects.filter(status='Accepted')
    mdata=[]
    for i in ob:
        data={
            'cid':i.id,
            'name':i.name,
            'email':i.email,
            'phone':i.phone,
            'district':i.district,
            'photo':i.photo.url,
        }
        mdata.append(data)
    return JsonResponse({'status':'ok','data':mdata})

def UserViewCompanyStocks(request):
    cid = request.POST['cid']
    ob=stock_table.objects.filter(COMPANY__id=cid)
    mdata=[]
    for i in ob:
        data={
            'name':i.name,
            'photo':i.photo.url,
            'price':i.price,
            'details':i.details,
        }
        mdata.append(data)
    return JsonResponse({'status':'ok','data':mdata})

def UserViewCompanyRating(request):
    cid = request.POST['cid']
    ob=company_review.objects.filter(COMPANY__id=cid)
    mdata=[]
    for i in ob:
        data={
            'user':i.USER.name,
            'photo':i.USER.photo.url,
            'review':i.review,
            'rating':str(i.rating),
            'date':str(i.date),
        }
        mdata.append(data)
    return JsonResponse({'status':'ok','data':mdata})

def UserSendCompanyRating(request):
    cid = request.POST['cid']
    lid=request.POST['lid']
    review=request.POST['review']
    rating=request.POST['rating']
    ob=company_review()
    ob.review=review
    ob.rating=rating
    ob.date=datetime.today()
    ob.COMPANY=company_table.objects.get(id=cid)
    ob.USER=user_table.objects.get(LOGIN__id=lid)
    ob.save()
    return JsonResponse({'status':'ok'})

def UserViewTips(request):
    ob=tips.objects.all()
    mdata=[]
    for i in ob:
        data={
            'expert':i.EXPERT.name,
            'photo':i.EXPERT.photo.url,
            'tip':i.tiptitle,
            'description':i.description,
            'date':str(i.date),
        }
        mdata.append(data)
    return JsonResponse({'status':'ok','data':mdata})

def ViewAllStocks(request):
    ob=stock_table.objects.all()
    mdata=[]
    for i in ob:
        data={
            'company':i.COMPANY.name,
            'sid':i.id,
            'photo':i.photo.url,
            'stock':i.name,
            'price':i.price,
            'details':i.details,
        }
        mdata.append(data)
    return JsonResponse({'status':'ok','data':mdata})





#######################forgotpassword###########################
def ForgotPassword(request):
    return render(request,'forgot_password.html')

def forgotPassword_otp(request):
    if 'email' in request.POST:
        request.session['email'] = request.POST['email']
    email=request.session['email']
    try:
        user=User.objects.get(email=email)
    except User.DoesNotExist:
        messages.warning(request,'Email doesnt match')
        return redirect('/myapp/')
    otp=random.randint(100000,999999)
    request.session['otp']=str(otp)
    request.session['email'] = email

    send_mail('Your Verification Code',
    f'Your verification code is {otp}',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False)
    messages.success(request,'OTP sent To your Mail')
    return redirect('/myapp/verifyOtp/')

def verifyOtp(request):
    return render(request,'otpverification.html')

def verifyOtpPost(request):
    entered_otp=request.POST['entered_otp']
    if request.session.get('otp') == entered_otp:
        messages.success(request,'otp verified')
        return redirect('/myapp/new_password/')
    else:
        messages.warning(request,'Invalid OTP!!')
        return redirect('/myapp/')

def new_password(request):
    return render(request,'new_password.html')

def changePassword(request):
    newpassword=request.POST['newPassword']
    confirmPassword=request.POST['confirmPassword']
    if newpassword == confirmPassword:
        email=request.session.get('email')
        user = User.objects.get(email=email)
        user.set_password(confirmPassword)
        user.save()
        messages.success(request, 'Password Updated Successfully')
        return redirect('/myapp/')
    else:
        messages.warning(request, 'The password doesnt match!!')
        return redirect('/myapp/new_password/')





def forgotpasswordflutter(request):
    email = request.POST['email']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Email not found'})

    otp = random.randint(100000, 999999)
    PasswordResetOTP.objects.create(email=email, otp=otp)

    send_mail('Your Verification Code',
              f'Your verification code is {otp}',
              settings.EMAIL_HOST_USER,
              [email],
              fail_silently=False)
    return JsonResponse({'status': 'ok', 'message': 'OTP sent'})


def verifyOtpflutterPost(request):
    email = request.POST['email']
    entered_otp = request.POST['entered_otp']
    otp_obj = PasswordResetOTP.objects.filter(email=email).latest('created_at')
    if otp_obj.otp == entered_otp:
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error'})


def changePasswordflutter(request):
    email = request.POST['email']
    newpassword = request.POST['newPassword']
    confirmPassword = request.POST['confirmPassword']
    if newpassword == confirmPassword:
        try:
            user = User.objects.get(email=email)
            user.set_password(confirmPassword)
            user.save()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})








##########################Main#################

def PredictStockData(request):
    try:
        stock_id = request.POST.get('stock_id')

        # 1️⃣ Fetch history
        history = StockDailyHistory.objects.filter(STOCK_id=stock_id).order_by('date')

        if not history.exists() or history.count() < 3:
            return JsonResponse({'status': 'error', 'message': 'Not enough data'})

        # 2️⃣ Convert to DataFrame
        df = pd.DataFrame(list(history.values('date', 'starting', 'ending')))
        df['date'] = pd.to_datetime(df['date'])
        df['days'] = (df['date'] - df['date'].min()).dt.days

        X = df[['days']]
        y = df['ending']

        # 3️⃣ Train regression
        model = LinearRegression()
        model.fit(X, y)

        # 4️⃣ Predict next day
        next_day = np.array([[df['days'].max() + 1]])
        predicted_price = model.predict(next_day)[0]

        trend = "up" if predicted_price > y.iloc[-1] else "down"

        # 5️⃣ Format response
        history_data = [
            {'date': str(i['date']), 'ending': i['ending']}
            for i in list(history.values('date', 'ending'))
        ]

        return JsonResponse({
            'status': 'ok',
            'history': history_data,
            'predicted_price': round(predicted_price, 2),
            'trend': trend
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def RealStockPrediction(request):
    symbol = request.GET.get('symbol', 'AAPL')

    try:
        # 1️⃣ Fetch last 1 month data safely
        data = yf.download(symbol, period="1mo", interval="1d", auto_adjust=False)

        if data.empty:
            return JsonResponse({'status': 'error', 'message': 'No data found for this symbol'})

        # Ensure 'Close' column is 1D
        close_prices = np.ravel(data['Close'].values)

        # 2️⃣ Create DataFrame properly
        df = pd.DataFrame({
            'date': data.index,
            'ending': close_prices
        })

        # 3️⃣ Add 'days' column (0, 1, 2, ...)
        df['date'] = pd.to_datetime(df['date'])
        df['days'] = np.arange(len(df))  # simpler and guaranteed 1D

        # 4️⃣ Prepare X and y (both 1D)
        X = df[['days']]  # shape (n, 1)
        y = df['ending'].values  # shape (n,)

        # 5️⃣ Train regression model
        model = LinearRegression()
        model.fit(X, y)

        # 6️⃣ Predict next day's price
        next_day = np.array([[df['days'].max() + 1]])
        predicted_price = float(model.predict(next_day)[0])

        # 7️⃣ Determine trend
        trend = "up" if predicted_price > y[-1] else "down"

        # 8️⃣ Prepare response data
        history = [
            {'date': str(date.date()), 'ending': float(price)}
            for date, price in zip(df['date'], df['ending'])
        ]

        return JsonResponse({
            'status': 'ok',
            'symbol': symbol,
            'predicted_price': round(predicted_price, 2),
            'trend': trend,
            'history': history
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})



def TopStockPredictions(request):
    # List of top stock symbols with company names
    top_companies = {
        'RELIANCE.NS': 'Reliance Industries',
        'TCS.NS': 'Tata Consultancy Services',
        'INFY.NS': 'Infosys',
        'HDFCBANK.NS': 'HDFC Bank',
        'ICICIBANK.NS': 'ICICI Bank',
        'SBIN.NS': 'State Bank of India',
        'BHARTIARTL.NS': 'Bharti Airtel',
    }

    results = []

    try:
        for symbol, name in top_companies.items():
            data = yf.download(symbol, period="1mo", interval="1d", auto_adjust=False)

            if data.empty:
                continue

            close_prices = np.ravel(data['Close'].values)
            df = pd.DataFrame({
                'date': data.index,
                'ending': close_prices
            })
            df['days'] = np.arange(len(df))

            X = df[['days']]
            y = df['ending'].values

            model = LinearRegression()
            model.fit(X, y)

            next_day = np.array([[df['days'].max() + 1]])
            predicted = float(model.predict(next_day)[0])
            trend = "up" if predicted > y[-1] else "down"

            results.append({
                'symbol': symbol,
                'name': name,
                'current_price': round(float(y[-1]), 2),
                'predicted_price': round(predicted, 2),
                'trend': trend,
            })

        return JsonResponse({'status': 'ok', 'data': results})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def ExpertViewTopStock(request):
    return render(request, 'expert/top_stock_data.html')

def ExpertStockPrediction(request,id):
    request.session['stock_id'] = id
    return render(request, 'expert/stock_prediction.html')

