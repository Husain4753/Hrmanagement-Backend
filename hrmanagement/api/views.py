from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import UserRegistrationSerializer,UserLoginSerializer,GetUserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserUpdateSerializer,NewLeaveSerializer,GetLeaveSerializer,ChangeLeaveSerializer,NewApplicantRequestSerializer,ApplicantSerializer,GetResumeDetailSerializer,UserProfileUpdateSerializer,NewAnnouncementSerializer,GetAllAnnouncementsSerializer,UserPasswordResetSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import uuid
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth import authenticate
from .models import User,Leave,Resume,Announcement
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.

# For Getting a token for user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['is_admin'] = user.is_admin
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
# Authentication Views
class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAdminUser]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({'msg':'New User created successfully'},status=status.HTTP_201_CREATED) 
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username=serializer.data.get('username')
            password=serializer.data.get('password')
            user=authenticate(username=username,password=password)
            # print(user)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'login Success'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)

class GetLoggedUserProfile(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=GetUserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class GetSingleProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAdminUser]
    def get(self,request,pk,format=None):
        user=User.objects.get(id=pk)
        serializer=GetUserProfileSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
class GetAllUserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAdminUser]
    def get(self,request,format=None):
        data=User.objects.all()
        serializer=GetUserProfileSerializer(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ChangeUserPasswordView(APIView):
    renderer_classes=[UserRenderer]  
    permission_classes=[IsAuthenticated]       
    def put(self,request,format=None,pk=None):
        if pk is not None:
            user=User.objects.get(id=pk)
            serializer=UserChangePasswordSerializer(data=request.data,context={'user':user})
            if serializer.is_valid(raise_exception=True):
                return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)
        serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)
          

class SendPasswordResetEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Link Send'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Successfully'},status=status.HTTP_200_OK)

class UserUpdateView(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]
    def put(self,request,pk=None,format=None):
        id=pk
        if pk is not None:
            user=User.objects.get(pk=id)
            serializer=UserUpdateSerializer(user,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'msg':'Data has been updated successfully'})
        user=User.objects.get(username=request.user)
        serializer=UserUpdateSerializer(request.user,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':'Data has been updated successfully'})
       

class UserProifleUpdateView(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]
    def put(self,request,pk=None,format=None):
        if pk is not None:
            user=User.objects.get(pk=pk)
            serializer=UserProfileUpdateSerializer(user,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'msg':'Profile has been updated successfully'},status=status.HTTP_200_OK)  
        serializer=UserProfileUpdateSerializer(request.user,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':'Profile has been updated successfully'})
       


class UserDeleteData(APIView):
    permission_classes=[IsAdminUser]
    renderer_classes=[UserRenderer]
    def delete(self,request,pk,format=None):
        user=User.objects.get(pk=pk)
        user.delete()
        return Response({'msg':'User has been deleted successfully'})

# Leave Views

class NewLeaveView(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        data=request.data | {"user":request.user.username}
        serializer=NewLeaveSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            leave=serializer.save()
            return Response({'msg':'Leave application has been sent successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   
        
class GetLoggedUserLeaveView(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]
    def get(self,request,format=None):
        data=Leave.objects.filter(user=request.user)
        serializer=GetLeaveSerializer(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class GetAllUserLeaveView(APIView):
    permission_classes=[IsAdminUser]
    renderer_classes=[UserRenderer]
    def get(self,request,format=None):
        data=Leave.objects.all()
        serializer=GetLeaveSerializer(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ChangeLeaveView(APIView):
    permission_classes=[IsAdminUser]
    renderer_classes=[UserRenderer]
    def put(self,request,pk,format=None):
        leave=Leave.objects.get(pk=pk)
        serializer=ChangeLeaveSerializer(leave,data=request.data)
        if serializer.is_valid():
            leave=serializer.save()
            return Response({'msg':'Leave Has been successfully updated'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# Resume View 

class NewApplicantRequestView(APIView):
    permission_classes=[IsAdminUser]
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        unique_id=uuid.uuid4().hex
        print(unique_id)
        data=request.data|{"created_by":request.user.id,"unique_id":unique_id}
        serializer=NewApplicantRequestSerializer(data=data)
        if serializer.is_valid():
            resume=serializer.save()
            return Response("New application has been created successfully",status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class PutApplicantDetailview(APIView):
    renderer_classes=[UserRenderer]
    def put(self,request,pk,format=None):
        resume=Resume.objects.get(unique_id=pk)
        serializer=ApplicantSerializer(resume,data=request.data)
        if serializer.is_valid():
            resume=serializer.save()
            return Response({'msg':'Resume has been filled completely'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class GetResumeDetailView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAdminUser]
    def get(self,request,format=None):
        resume=Resume.objects.all()
        serializer=GetResumeDetailSerializer(resume,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

#Announcement Views

class GetAllAnnouncementsView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        announcement=Announcement.objects.all()
        serializer=GetAllAnnouncementsSerializer(announcement,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class NewAnnouncementView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        data=request.data|{"user":request.user.username}
        serializer=NewAnnouncementSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            announcement=serializer.save()
            return Response({'msg':'New Announcement has been made successfully'},status=status.HTTP_200_OK)

class GetDashboardDataview(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAdminUser]
    def get(self,request,format=None):
        staff_count=User.objects.count()
        leave_count=Leave.objects.filter(status='Unseen').count()
        resume_count=Resume.objects.count()
        return Response({'staff_count':staff_count,'leave_count':leave_count,'resume_count':resume_count},status=status.HTTP_200_OK)
