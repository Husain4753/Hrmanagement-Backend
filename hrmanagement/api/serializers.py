from rest_framework import serializers
from .models import User,Leave,Resume,Announcement
from django.utils.encoding import smart_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from .utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['username','email','contact','department','profile_image','password','password2','is_admin']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def validate_password(self, value):
        validate_password(value)  # Django's password validation
        return value    
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password!=password2:
            raise serializers.ValidationError("Password and Confirm Password does not match")
        return attrs

    def create(self,validate_data):
        return User.objects.create_user(**validate_data)    

class UserLoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=255)
    class Meta:
        model=User
        fields=['username','password']

class GetUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','contact','department','profile_image','is_admin','created_at','updated_at']
    
class UserChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password','password2']
        
    def validate_password(self, value):
        validate_password(value)  # Django's password validation
        return value

    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password!=password2:
            raise serializers.ValidationError("Password and Confirm Password does not match")   
        user.set_password(password)
        user.save()
        return attrs
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    
    def validate(self, attrs):
        email=attrs.get("email")
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID',uid)
            token=PasswordResetTokenGenerator().make_token(user)
            link='http://localhost:3000/api/user/reset/'+uid+'/'+token
            print ("password Reset link",link)
            body='Click the following link to reset password \n'+link
            data={
                "subject":"Reset Your Password",
                'body':body,
                'to_email':user.email
            }
            # Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a registered user')



class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password','password2']
    
    def validate_password(self, value):
        validate_password(value)  # Django's password validation
        return value    
        
    def validate(self, attrs):
        try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            if password!=password2:
                raise serializers.ValidationError("Password and Confirm Password does not match") 
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError("Token is not Valid or Expired") 
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('Token is not Valid or Epired')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','contact','department','is_admin']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['profile_image']

# Leave Serializers

class NewLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=Leave
        fields=['user','date_from','date_to','reason']
    def validate(self,attrs):
        user=attrs.get('user')
        date_from=attrs.get('date_from')
        if (Leave.objects.filter(date_from=date_from,user=user)):
            raise serializers.ValidationError('Request for leave on this date has already been sent ')
        return attrs

class GetLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=Leave
        fields=['id','user','date_from','date_to','status','reason','remarks','app_date']

class ChangeLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=Leave
        fields=['status','remarks']
        

# Resume Serializer

class NewApplicantRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Resume
        fields=['created_by','email','unique_id']
    
    def validate(self, attrs):
        email=attrs.get('email')
        created_by=attrs.get('created_by')
        unique_id=attrs.get('unique_id')
        if Resume.objects.filter(email=email).exists():
            raise serializers.ValidationError("Application already generated by this id")
        link="http://localhost:3000/putapplicantdetail/"+str(unique_id)
        print('New Application link send successfully')
        body="Kindly fill your info for new application. The link is given below \n \n"+link
        data={
                "subject":"Fill your info here",
                'body':body,
                'to_email':email
            }
        print(link)
        # Util.send_email(data)
        return attrs

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model=Resume
        fields=['name','email','dob','address','gender','pimage','rdocs']

class GetResumeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Resume
        fields=['name','email','dob','address','gender','pimage','rdocs','unique_id','created_by']

# Announcement Serializers

class GetAllAnnouncementsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Announcement
        fields=['id','user','announcement','date']

class NewAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Announcement
        fields=['user','announcement']