from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import UniAR, Profile, User, UserType, UniType, UniFileType, UniCategory, LoginType
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.db.models import Q
from functools import reduce
from operator import or_
from django.core.files import File
from _datetime import datetime

@csrf_exempt
def request_server(request):
    print(1)
    if request.method == 'POST':
        print(2)
        print(request.POST)
        if request.POST.get('ACTION') == "Login":
            print("Login")
            data = Login(request)
        elif request.POST.get('ACTION') == "Register":
            data = print("Register")
            data = Register(request)
        elif request.POST.get('ACTION') == "FBLogin":
            print("FBLogin")
            FBLogin(request)
        elif request.POST.get('ACTION') == "RecuperarContrasena":
            print("RecuperarContrasena")
            RecuperarContrasena(request)
        elif request.POST.get('ACTION') == "GetGlobalUnis":
            print("GetGlobalUnis")
            data = GetGlobalUnis(request)
        elif request.POST.get('ACTION') == "GetGlobalUnisCategory":
            print("GetGlobalUnisCategory")
            data = GetGlobalUnisCategory(request)
        elif request.POST.get('ACTION') == "GetSerchedUsers":
            print("GetSerchedUsers")
            data = GetSerchedUsers(request)
        elif request.POST.get('ACTION') == "GetUserProfile":
            print("GetUserProfile")
            data = GetUserProfile(request)
        elif request.POST.get('ACTION') == "GetProfile":
            print("GetProfile")
            data = GetProfile(request)
        elif request.POST.get('ACTION') == "ChangeProfileData":
            print("ChangeProfileData")
            data = ChangeProfileData(request)
        elif request.POST.get('ACTION') == "UploadUni":
            print("UploadUni")
            data = UploadUni(request)
    print(data)
    return JsonResponse(data, safe = False)




def handle_uploaded_file(f, path):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def UploadUni(request):
    name = request.POST.get('NAME')
    unihyperlink = request.POST.get('UNIHYPERLINK')
    fileSize = request.POST.get('FILESIZE')
    isPrivate = request.POST.get('ISPRIVATE')
    ownerid = request.POST.get('OWNER')
    position_x = request.POST.get('POSITION_X')
    position_y = request.POST.get('POSITION_Y')
    position_z = request.POST.get('POSITION_Z')
    rotation_x = request.POST.get('ROTATION_X')
    rotation_y = request.POST.get('ROTATION_Y')
    rotation_z = request.POST.get('ROTATION_Z')
    scale_x = request.POST.get('SCALE_X')
    scale_y = request.POST.get('SCALE_Y')
    scale_z = request.POST.get('SCALE_Z')
    uniCategory = request.POST.get('UNICATEGORY')
    uniType = request.POST.get('UNITYPE')
    uniFileType = request.POST.get('UNIFILETYPE')
    
    path_img = settings.MEDIA_ROOT + '\\tmps\\' + request.FILES['IMAGE'].name
    path_file = settings.MEDIA_ROOT + '\\tmps\\' + request.FILES['FILE'].name

    image = handle_uploaded_file(request.FILES['IMAGE'], path_img)
    file = handle_uploaded_file(request.FILES['FILE'], path_file)
    
    uniAR = UniAR();
    
    user = User.objects.get(id = ownerid)
    uniAR.owner = Profile.objects.get(user = user)
    
    
    uniAR.name = name
    uniAR.pub_date = datetime.now(tz=None)
    uniAR.uniHyperLink = unihyperlink
    uniAR.fileSize = fileSize
    uniAR.isPrivate = isPrivate
    uniAR.position_x = position_x
    uniAR.position_y = position_y
    uniAR.position_z = position_z
    uniAR.rotation_x = rotation_x
    uniAR.rotation_y = rotation_y
    uniAR.rotation_z = rotation_z
    uniAR.scale_x = scale_x
    uniAR.scale_y = scale_y
    uniAR.scale_z = scale_z
    uniAR.uniCategory = UniCategory(int(uniCategory))
    uniAR.uniType = UniType(int(uniType))
    uniAR.uniFileType = UniFileType(int(uniFileType))
    
    local_file = open(path_img, 'rb')
    djangofile = File(local_file)
    uniAR.image.save(request.FILES['IMAGE'].name, djangofile, save=True)
    #uniAR.image = djangofile
    local_file.close()
    djangofile.close()
    
    local_file = open(path_file, 'rb')
    djangofile = File(local_file)
    uniAR.file.save(request.FILES['FILE'].name, djangofile, save=True)
    #uniAR.file = djangofile
    local_file.close()
    djangofile.close()
    
    uniAR.save();
    print(uniAR.id)
    
    data = {"STATUS": 0}
    
    return data




def GetUserProfile(request):
    searchId = request.POST.get('USERID')
    user = User.objects.get(id = searchId)
    data = {"STATUS" : 0}
    newProfile = Profile.objects.filter(user = user);
    if newProfile is not None and len(newProfile) > 0:
        data["ID"] = user.id
        data["USERNAME"] = user.username
        data["FOLLOWERS"] = newProfile[0].followers
        data["FOLLOWING"] = newProfile[0].following
        data["UNISAMOUNT"] = newProfile[0].unisAmount
        try:
            data["IMAGE"] = newProfile[0].image.url
        except:
            data["IMAGE"] = ""
            
        data["UNIS"] = {}
        uniars = UniAR.objects.filter(owner = newProfile[0]);
        i = 0
        for element in uniars:
            print(element)
            print("-------")
            data["UNIS"][i] = {}
            data["UNIS"][i]["ID"] = element.id
            data["UNIS"][i]["UNICATEGORY"] = element.uniCategory
            data["UNIS"][i]["UNITYPE"] = element.uniType
            data["UNIS"][i]["UNIFILETYPE"] = element.uniFileType
            data["UNIS"][i]["IMAGE"] = element.image.url
            data["UNIS"][i]["FILE"] = element.file.url
            data["UNIS"][i]["UNIHYPERLINK"] = element.uniHyperLink
            data["UNIS"][i]["FILESIZE"] = element.fileSize
            data["UNIS"][i]["POSITIONX"] = element.position_x
            data["UNIS"][i]["POSITIONY"] = element.position_y
            data["UNIS"][i]["POSITIONZ"] = element.position_z
            data["UNIS"][i]["ROTATIONX"] = element.rotation_x
            data["UNIS"][i]["ROTATIONY"] = element.rotation_y
            data["UNIS"][i]["ROTATIONZ"] = element.rotation_z
            data["UNIS"][i]["SCALEX"] = element.scale_x
            data["UNIS"][i]["SCALEY"] = element.scale_y
            data["UNIS"][i]["SCALEZ"] = element.scale_z
            i+=1
            
    print(data)
    return data


def GetSerchedUsers(request):
    searchQuery = request.POST.get('SEARCHEDUSER')
    q = Q()
    for user in User.objects.all():
        q |= Q(username__icontains = searchQuery)
    posibleUsers = User.objects.filter(q)
    posibleUsers = posibleUsers.order_by('-id')[:6]
    data = {"STATUS" : 0}
    data["USERS"] = {}
    for element in posibleUsers:
        newProfile = Profile.objects.filter(user = element);
        if newProfile is not None and len(newProfile) > 0:
            data["USERS"][element.id] = {}
            data["USERS"][element.id]["ID"] = element.id
            data["USERS"][element.id]["USERNAME"] = element.username
            data["USERS"][element.id]["FOLLOWERS"] = newProfile[0].followers
            try:
                data["USERS"][element.id]["IMAGE"] = newProfile[0].image.url
            except:
                data["USERS"][element.id]["IMAGE"] = "";
    return data

def GetGlobalUnisCategory(request):
    UniCat = request.POST.get('UNICATEGORY')
    categorySelect = UniAR.objects.all().filter(uniCategory = UniCat)
    last_nine = categorySelect.order_by('-id')[:9]
    data = {"STATUS" : 0}
    data["UNIS"] = {}
    for element in last_nine:
        data["UNIS"][element.id] = {}
        data["UNIS"][element.id]["ID"] = element.id
        data["UNIS"][element.id]["UNICATEGORY"] = element.uniCategory
        data["UNIS"][element.id]["UNITYPE"] = element.uniType
        data["UNIS"][element.id]["UNIFILETYPE"] = element.uniFileType
        data["UNIS"][element.id]["IMAGE"] = element.image.url
        data["UNIS"][element.id]["FILE"] = element.file.url
        data["UNIS"][element.id]["UNIHYPERLINK"] = element.uniHyperLink
        data["UNIS"][element.id]["FILESIZE"] = element.fileSize
        data["UNIS"][element.id]["POSITIONX"] = element.position_x
        data["UNIS"][element.id]["POSITIONY"] = element.position_y
        data["UNIS"][element.id]["POSITIONZ"] = element.position_z
        data["UNIS"][element.id]["ROTATIONX"] = element.rotation_x
        data["UNIS"][element.id]["ROTATIONY"] = element.rotation_y
        data["UNIS"][element.id]["ROTATIONZ"] = element.rotation_z
        data["UNIS"][element.id]["SCALEX"] = element.scale_x
        data["UNIS"][element.id]["SCALEY"] = element.scale_y
        data["UNIS"][element.id]["SCALEZ"] = element.scale_z
    return data

def GetGlobalUnis(request):
    last_nine = UniAR.objects.all().order_by('-id')[:9]
    data = {"STATUS" : 0}
    data["UNIS"] = {}
    for element in last_nine:
        data["UNIS"][element.id] = {}
        data["UNIS"][element.id]["ID"] = element.id
        data["UNIS"][element.id]["UNICATEGORY"] = element.uniCategory
        data["UNIS"][element.id]["UNITYPE"] = element.uniType
        data["UNIS"][element.id]["UNIFILETYPE"] = element.uniFileType
        data["UNIS"][element.id]["IMAGE"] = element.image.url
        data["UNIS"][element.id]["FILE"] = element.file.url
        data["UNIS"][element.id]["UNIHYPERLINK"] = element.uniHyperLink
        data["UNIS"][element.id]["FILESIZE"] = element.fileSize
        data["UNIS"][element.id]["POSITIONX"] = element.position_x
        data["UNIS"][element.id]["POSITIONY"] = element.position_y
        data["UNIS"][element.id]["POSITIONZ"] = element.position_z
        data["UNIS"][element.id]["ROTATIONX"] = element.rotation_x
        data["UNIS"][element.id]["ROTATIONY"] = element.rotation_y
        data["UNIS"][element.id]["ROTATIONZ"] = element.rotation_z
        data["UNIS"][element.id]["SCALEX"] = element.scale_x
        data["UNIS"][element.id]["SCALEY"] = element.scale_y
        data["UNIS"][element.id]["SCALEZ"] = element.scale_z
    return data

def Login(request):
    login_type = request.POST.get('LOGINTYPE')
    if login_type == '2':
        name = request.POST.get('USERNAME')
        password = request.POST.get('PASSWORD')
    else:
        name = request.POST.get('USERNAME')
        password = request.POST.get('PASSWORD')
    user = authenticate(username=name, password=password)
    if user is not None:
        newProfile = Profile.objects.filter(user = user);
        if newProfile is not None:
            data = {
                'STATUS': 0,
                'ID': user.id,
                'FOLLOWERS': newProfile[0].followers,
                'FOLLOWING': newProfile[0].following,
                'UNISAMOUNT': newProfile[0].unisAmount,
                'USERTYPE': newProfile[0].userType,
                'LOGINTYPE': newProfile[0].loginType
            }
    else:
        data = {
            'STATUS': 1,
            'ERROR': 'USER NOT FOUND OR WRONG PASSWORD'
        }
    return data
    
def Register(request):
    data = {}
    try:
        login_type = request.POST.get('LOGINTYPE')
        if login_type == '2':
            name = request.POST.get('USERNAME')
            password = request.POST.get('PASSWORD')
            email = request.POST.get('EMAIL')
            user = User.objects.create_user(name, email, password)
        else:
            print(5)
            print(request.POST.get('USERNAME'))
            print(request.POST.get('PASSWORD'))
            print(request.POST.get('EMAIL'))
            name = request.POST.get('USERNAME')
            password = request.POST.get('PASSWORD')
            email = request.POST.get('EMAIL')
            user = User.objects.create_user(name, email, password)
        newProfile = Profile.objects.filter(user = user); 
        print(9)
        newProfile.update(followers = 0)
        newProfile.update(following = 0)
        newProfile.update(unisAmount = 0)
        newProfile.update(userType = UserType.FREE)
        newProfile.update(loginType = LoginType.EMAIL)
        data = {
            'STATUS': 0,
            'ID': user.id
        }
    except:
        data = {
            'STATUS': 1,
            'ERROR': 'THE USER ALREADY EXIST'
        }
    return data
    
def ChangePassword(request):
    name = request.POST.get('USERNAME')
    password = request.POST.get('PASSWORD')
    newpassword = request.POST.get('NEWPASSWORD')
    
    user = authenticate(username=name, password=password)
    if user is not None:
        user.set_password(newpassword)
        user.save()
        
        
        
        
        
        
# def request_server(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
#         return render(request, 'core/simple_upload.html', {
#             'uploaded_file_url': uploaded_file_url
#         })
#     return render(request, 'hola mundo')