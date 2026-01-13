from django.urls import path

from myapp import views
from myapp.views import login_get

urlpatterns=[
    path('adminhome/',views.admin_home),
    path('add_expertpost',views.add_expertpost),

    path('login_post/', views.loginpost),
    path('add_expert/', views.add_expert),
    path('view_expert/', views.view_expert),
    path('forgot_password/', views.forgot_password),
    path('send_reply/<id>/', views.send_reply),

    path('delete_expert/<id>', views.delete_expert),
    path('edit_expert/<id>', views.edit_expert),
    path('AcceptCompany/<id>/', views.AcceptCompany),
    path('RejectCompany/<id>/', views.RejectCompany),
    path('edit_expertpost/', views.edit_expertpost),


    path('change_password/', views.change_password),
    path('change_passwordpost/', views.change_passwordpost),
    path('view_complaints/', views.view_complaints),
    path('view_companyreview/', views.view_companyreview),
    path('view_user/', views.view_user),
    path('view_appfeedback/', views.view_appfeedback),
    path('verify_company/', views.verify_company),
    path('view_stock/<id>/', views.view_stock),




    ####################################


    path('company_home/', views.company_home),
    path('CompanyRegistration/', views.CompanyRegistration),
    path('CompanyViewStock/', views.CompanyViewStock),
    path('CompanyAddStock/', views.CompanyAddStock),
    path('CompanyEditStock/', views.CompanyEditStock),
    path('CompanyDeleteStock/<id>/', views.CompanyDeleteStock),
    path('CompanyViewTips/', views.CompanyViewTips),
    path('CompanyViewProfile/', views.CompanyViewProfile),
    path('CompanyUpdateProfile/', views.CompanyUpdateProfile),
    path('CompanyChangePassword/', views.CompanyChangePassword),
    path('ViewReviewRatings/', views.ViewReviewRatings),
    path('CompanyDailyUpdateStock/<id>/', views.CompanyDailyUpdateStock),
    path('DeleteDailyStockData/<id>/', views.DeleteDailyStockData),
    path('CompanyDailyUpdateStockPost/', views.CompanyDailyUpdateStockPost),

    #######################################


    path('expert_home/', views.expert_home),
    path('Add_newtip/', views.Add_newtip),
    path('Add_newtippost/',views.Add_newtippost),
    path('expert_change_password/', views.expert_change_password),
    path('expert_change_passwordpost/', views.expert_change_passwordpost),
    path('manage_tips/', views.manage_tips),
    path('delete_tip/<id>/', views.delete_tip),
    path('view_doubt/', views.view_doubt),
    path('expert_send_reply/<id>/', views.expert_send_reply),
    path('view_users/', views.view_users),
    path('view_company/', views.view_company),
    path('ExpertViewStock/<id>/', views.ExpertViewStock),
    path('view_profile/', views.view_profile),
    path('UpdateProfile/', views.UpdateProfile),




    path('FlutterLogin/', views.FlutterLogin),
    path('UserRegistration/', views.UserRegistration),
    path('SendComplaint/', views.SendComplaint),
    path('UserViewComplaints/', views.UserViewComplaints),
    path('UserSendAppFeedback/', views.UserSendAppFeedback),
    path('UserViewAppRating/', views.UserViewAppRating),
    path('UserViewProfile/', views.UserViewProfile),
    path('UserChangePassword/', views.UserChangePassword),
    path('UserViewExperts/', views.UserViewExperts),
    path('UserAskDoubt/', views.UserAskDoubt),
    path('UserViewDoubts/', views.UserViewDoubts),
    path('ViewCompanies/', views.ViewCompanies),
    path('UserViewCompanyStocks/', views.UserViewCompanyStocks),
    path('UserViewCompanyRating/', views.UserViewCompanyRating),
    path('UserSendCompanyRating/', views.UserSendCompanyRating),
    path('UserViewTips/', views.UserViewTips),
    path('ViewAllStocks/', views.ViewAllStocks),

    path('ForgotPassword/', views.ForgotPassword),
    path('forgotpasswordflutter/', views.forgotpasswordflutter),
    path('verifyOtpflutterPost/', views.verifyOtpflutterPost),
    path('changePasswordflutter/', views.changePasswordflutter),
    path('forgotPassword_otp/', views.forgotPassword_otp),
    path('verifyOtp/', views.verifyOtp),
    path('verifyOtpPost/', views.verifyOtpPost),
    path('new_password/', views.new_password),
    path('changePassword/', views.changePassword),


    path('PredictStockData/', views.PredictStockData),
    path('RealStockPrediction/', views.RealStockPrediction),
    path('TopStockPredictions/', views.TopStockPredictions),
    path('ExpertViewTopStock/', views.ExpertViewTopStock),
    path('ExpertStockPrediction/<id>/', views.ExpertStockPrediction),


]