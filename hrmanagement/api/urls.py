from api import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # auth api
    path('loginuser/',views.UserLoginView.as_view(),name='loginuser'),
    path('alluserprofile/',views.GetAllUserProfileView.as_view(),name='alluserprofile'),
    path('getuserprofile/<int:pk>/',views.GetSingleProfileView().as_view(),name='getuserprofile'),
    path('loggeduserprofile/',views.GetLoggedUserProfile.as_view(),name='loggeduserprofile'),
    path('userprofileupdate/',views.UserProifleUpdateView.as_view(),name='userprofileupdate'),
    path('userprofileupdate/<int:pk>/',views.UserProifleUpdateView.as_view(),name='userprofileupdate'),
    path('updateuser/',views.UserUpdateView.as_view(),name='updateuser'),
    path('updateuser/<int:pk>/',views.UserUpdateView.as_view(),name='updateuser'),
    path('changeuserpassword/',views.ChangeUserPasswordView.as_view(),name='changeuserpassword'),
    path('changeuserpassword/<int:pk>/',views.ChangeUserPasswordView.as_view(),name='changeuserpassword'),
    path('deleteuser/<int:pk>/',views.UserDeleteData.as_view(),name='deleteuser'),
    path('registeruser/',views.UserRegistrationView.as_view(),name='registeruser'),
    path('sendresetpasswordemail/',views.SendPasswordResetEmailView.as_view(),name='sendresetpasswordemail'),
    path('resetpassword/<str:uid>/<str:token>/',views.UserPasswordResetView.as_view(),name='resetpassword'),
    path('refreshtoken/',TokenRefreshView.as_view(),name='refeshtoken'),
    path('getdashboarddata/',views.GetDashboardDataview.as_view(),name='getdashboarddata'),

    # # Leave Urls
    path('getalluserleave/',views.GetAllUserLeaveView.as_view(),name='getalluserleave'),
    path('changeuserleave/<int:pk>/',views.ChangeLeaveView.as_view(),name='changeuserleave'),
    path('getloggeduserleave/',views.GetLoggedUserLeaveView.as_view(),name='getloggeduserleave'),
    path('applynewleave/',views.NewLeaveView.as_view(),name='applynewleave'),
    # # Applicant Urls
    path('createnewapplication/',views.NewApplicantRequestView.as_view(),name='createnewapplication'),
    path('getresumedetail/',views.GetResumeDetailView.as_view(),name='getresumedetail'),
    path('putapplicantdetail/<str:pk>/',views.PutApplicantDetailview.as_view(),name='putapplicantdetail'),
    # Announcement Urls
    path('getallannouncement/',views.GetAllAnnouncementsView.as_view(),name='getallannouncement'),
    path('newannouncement/',views.NewAnnouncementView.as_view(),name='newannouncement'),
]
