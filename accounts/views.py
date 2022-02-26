from django.shortcuts import render
# from rest_framework import generics, permissions
# from rest_framework.response import Response
# from knox.models import AuthToken
# from .serializers import UserSerializer, RegisterSerializer

# # Create your views here.

# # Register API
# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = RegisterSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#         "user": UserSerializer(user, context=self.get_serializer_context()).data,
#         "token": AuthToken.objects.create(user)[1]
#         })

# from django.contrib.auth import login

# from rest_framework import permissions
# from rest_framework.authtoken.serializers import AuthTokenSerializer
# from knox.views import LoginView as KnoxLoginView

# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return super(LoginAPI, self).post(request, format=None)
#         from django.shortcuts import render
from django.http.response import HttpResponse
import pyrebase
# Create your views here.
from rest_framework.views import APIView
import firebase_admin
from firebase_admin import credentials,firestore,auth
from django.core.files.storage import default_storage
from django.contrib import messages

cred = credentials.Certificate("serviceAccountKey.json")
config={
   'apiKey': "AIzaSyCnqJQ8krxzMk4qcxt-Sg3hsIzTSpQW3ME",

  'authDomain': "fir-9ca93.firebaseapp.com",

  'databaseURL': "https://fir-9ca93-default-rtdb.firebaseio.com",

  'projectId': "fir-9ca93",
  'storageBucket': "fir-9ca93.appspot.com",
  'messagingSenderId': "977749723231",
  'appId': "1:977749723231:web:736317a9255031b6f673ea",
  'measurementId': "G-ZE9T4CZHMT"
}
try:
    firebase_admin.get_app()
except ValueError as e:
    firebase_admin.initialize_app(cred)

firebase=pyrebase.initialize_app(config)
storage = firebase.storage()
authe = firebase.auth()
database = firestore.client()


class RegisterApi(APIView):
    def post(self, request, format=None):
        email = request.POST.get('email')
        pasw = request.POST.get('pasw')
        name = request.POST.get('name')
        phone= request.POST.get('phone')
        sapid= request.POST.get('sapid')
        # file = request.FILES['file']
        # file_save = default_storage.save(file.name, file)
        # storage.child(sapid).put("media/" + file.name)
        # delete = default_storage.delete(file.name)
        # messages.success(request, "File upload in Firebase Storage successful")
        div= request.POST.get('div')
        year= request.POST.get('year')
        
        database.collection('Registration').document(sapid).set({'name':name,'phone':phone,'sapid':sapid,'div':div,'year':year,'email':email})
        try:
            # creating a user with the given email and password
            user=auth.create_user(email=email,email_verified=True,password=pasw,display_name=name)
            uid = user.uid
            # idtoken = request.session['uid']
            print(uid)
        except Exception as e:
            print('Error',e)
            return HttpResponse("error")
            # return render(request, "Registration.html")
        
        return HttpResponse("Created")
        # return render(request,"Login.html")

    def get(self,request):
        return HttpResponse("Well deserved")
        

class LoginAPI(APIView):
   

    def post(self, request, format=None):
        # serializer = AuthTokenSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['user']
        # login(request, user)
        # return super(LoginAPI, self).post(request, format=None)

        email=request.POST.get('email')
        pasw=request.POST.get('pasw')
        
        
        try:
            # if there is no error then signin the user with given email and password
            user = authe.sign_in_with_email_and_password(email,pasw)
            # user = authe.signInWithEmailAndPassword(email,pasw)
        except:
            message="Invalid Credentials!!Please ChecK your Data"
            
        session_id=user['idToken']
        print(session_id)
        request.session['uid']=str(session_id)
        #print(session_id)
        return HttpResponse("You are logged in")


    # def get(self,request):
    #     return HttpResponse("Success")
        #return render(request,"login.html")
#def signUp(request):
    #return render(request,"Registration.html")


class PositionApi(APIView):
    def post(self,request):
        sapid=request.POST.get('sapid')
        pos1=request.POST.get('pos1')
        pos2=request.POST.get('pos2')
        pos3=request.POST.get('pos3')
        github = request.POST.get('github')
        file = request.FILES['file']
        file_save = default_storage.save(file.name, file)
        storage.child(sapid).put("media/" + file.name)
        delete = default_storage.delete(file.name)
        messages.success(request, "File upload in Firebase Storage successful")
        database.collection('Registration').document(sapid).collection('Position').document(sapid).set({'pos1':pos1,'pos2':pos2,'pos3':pos3, 'github':github})
        return HttpResponse("Position added")

    # def __init__(self,name):
    #     self.name=name

class SlotbookApi(APIView):
    def post(self,request):
        sapid=request.POST.get('sapid')
        date=request.POST.get('date')
        timeslot = request.POST.get('timeslot')
        database.collection('Registration').document(sapid).collection('TimeSlot').document(sapid).set({'date':date,'timeslot':timeslot})


