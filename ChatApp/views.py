from django.shortcuts import render, redirect
from django.contrib import messages
from ChatApp.models import Userreg, Systemchat, Contactus
import pymysql
from django.contrib.auth import logout as django_logout
from django.db.models import Q
from django.db import connection
import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import pyotp
import qrcode
import io
import base64

# Create your views here.
def clear_messages(request):
    # Clear any previous messages
    storage = messages.get_messages(request)
    for _ in storage:
        pass

def homepage(request):
    clear_messages(request)
    return render(request,'index.html')

def aboutpage(request):
    return render(request,'about.html')

def register(request):
    clear_messages(request)

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        gender = request.POST['gender']
        phoneno = request.POST['phoneno']
        emailid = request.POST['emailid']
        password = request.POST['password']
        secure_question = request.POST['secure_question']
        answer = request.POST['answer']

        # Check if the phone number or email is already registered
        user_data = Userreg.objects.filter(Q(phoneno=phoneno) | Q(emailid=emailid)).first()

        
        if user_data:
            messages.error(request, 'This phone number or emailid has already registered')
            
        else:
            add_user = Userreg(
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                phoneno=phoneno,
                emailid=emailid,
                password=password,
                secure_question=secure_question,
                answer=answer
            )
            add_user.save()
            db_config = {
                'user': 'root',
                'password': 'root',
                'host': 'localhost',
                'database': 'chatting_system',
                'port': 3306
            }
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()

            # SQL query to create a new table
            table_name = f"ocs{phoneno}"
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                chatid int NOT NULL AUTO_INCREMENT,
                fromuser varchar(15) NOT NULL,
                touser varchar(15) NOT NULL,
                message varchar(500) NOT NULL,
                chat_date varchar(50) NOT NULL,
                PRIMARY KEY (chatid)
            )"""
            cursor.execute(create_table_query)
            cursor.close()
            conn.close()

            messages.success(request, 'You are successfully registered')
            return redirect('/login')
    return render(request,'register.html')

def login(request):
    clear_messages(request)

    if request.method == 'POST':
        uphoneno = request.POST.get('phoneno')
        password = request.POST.get('password')
        
        try:
            user_data = Userreg.objects.get(phoneno=uphoneno)
            if user_data and user_data.password == password:
                has_auth = user_data.is_set_auth

                request.session['uphoneno'] = uphoneno
                if has_auth:
                    return redirect('/verify')
                else:
                    user_data.status = 'Active now'
                    user_data.save()
                    messages.success(request, 'Login successfully')
                    return redirect('/users')
            else:
                messages.error(request, 'Invalid password')
        except Userreg.DoesNotExist:
            messages.error(request, 'User does not exist')
        return render(request, 'login.html')
    return render(request, 'login.html')

def auth_verify(request):
    clear_messages(request)
    
    uphoneno = request.session.get('uphoneno')
    if request.method == 'GET':
        user_data = Userreg.objects.get(phoneno=uphoneno)
        key = user_data.auth_token
        totp = pyotp.TOTP(key)
        check = True
    if request.method == 'POST':
        auth_otp = request.POST.get('auth_otp', '')

        try:
            user_data = Userreg.objects.get(phoneno=uphoneno)
            key = user_data.auth_token
            totp = pyotp.TOTP(key)
            
            check = totp.verify(auth_otp)
            if check:
                user_data.status = 'Active now'
                user_data.save()
                messages.success(request, 'Login successfully')
                return redirect('/users')
        except Exception as e:
            print(e)
    return render(request, 'authentication.html', {"check":check})

def reg_auth(request):
    clear_messages(request)
    
    uphoneno = request.session.get('uphoneno')
    
    if request.method == 'GET':
        try:
            qr_code = None
            has_auth = Userreg.objects.get(phoneno=uphoneno).is_set_auth
            if not has_auth:
                key = pyotp.random_base32()
                request.session['auth_key'] = key
                
                uri = pyotp.totp.TOTP(key).provisioning_uri(name=str(uphoneno), issuer_name="Chatting System")
                qr = qrcode.make(uri)
                buffer = io.BytesIO()
                qr.save(buffer, format="PNG")
                img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
                qr_code = f"data:image/png;base64,{img_str}"
        except Exception as e:
            print(e)
            has_auth = False
        return render(request, 'add_auth.html', {"qr_code":qr_code, "has_auth":has_auth})
    
    if request.method == 'POST':
        try:
            key = request.session.get('auth_key')

            user_data = Userreg.objects.get(phoneno=uphoneno)
            user_data.is_set_auth = True
            user_data.auth_token = key
            user_data.save()
            messages.success(request, 'Added')
            return redirect('/2fa')
        except Exception as e:
            print(e)
    return render(request, 'add_auth.html')

def delete_auth(request):
    clear_messages(request)
    
    uphoneno = request.session.get('uphoneno')
    user_data = Userreg.objects.get(phoneno=uphoneno)
    user_data.is_set_auth = False
    user_data.auth_token = ""
    user_data.save()
    messages.success(request, 'Deleted')
    return redirect('/2fa')

def turnoff_auth(request):
    clear_messages(request)
    
    uphoneno = request.session.get('uphoneno')
    if request.method == 'POST':
        question = request.POST.get('secure_question')
        answer = request.POST.get('answer')
        
        try:
            user_data = Userreg.objects.get(phoneno=uphoneno)
            
            if user_data.secure_question == question and user_data.answer == answer:
                user_data.is_set_auth = False
                user_data.auth_token = ""
                user_data.save()
                messages.success(request, 'Authentication Turned off')
                return redirect('/login')
            else:
                messages.error(request, 'Invalid secure question or answer. Please try again.')
        except Userreg.DoesNotExist:
            messages.error(request, 'User does not exist')

    return render(request, 'turnoff_auth.html', {"uphoneno":uphoneno})

def logout(request):
    clear_messages(request)
    
    uphoneno = request.session.get('uphoneno')
    if uphoneno:
        try:
            user_data = Userreg.objects.get(phoneno=uphoneno)
            user_data.status = 'offline'
            user_data.save()  # Save the updated status
        except Userreg.DoesNotExist:
            pass  # Handle the case where the user doesn't exist
    django_logout(request)
    messages.success(request, 'Logout successfully')
    return redirect('/login')

def contactus(request):
    clear_messages(request)

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        phoneno = request.POST['phoneno']
        emailid = request.POST['emailid']
        message = request.POST['messages']

        contact_us = Contactus(firstname=firstname, lastname=lastname, phoneno=phoneno, emailid=emailid, message=message)
        contact_us.save()
        messages.success(request, 'Successfully Sent')
        return redirect('/contactus')
    return render(request, 'contactus.html')

def pw_recovery(request):
    clear_messages(request)
    
    user_pw = None
    if request.method == 'POST':
        phone_email = request.POST.get('phone_email')
        question = request.POST.get('secure_question')
        answer = request.POST.get('answer')
        
        if phone_email.isnumeric():
            # Handle phone number case
            lookup = Q(phoneno=phone_email)
        else:
            # Handle email case
            lookup = Q(emailid=phone_email)
        
        try:
            # Fetch user data based on the lookup criteria
            user_data = Userreg.objects.get(lookup)
            
            if user_data.secure_question == question and user_data.answer == answer:
                user_pw = user_data.password
                messages.success(request, 'Password recovery successful. Check below 👇')
                # Render the template instead of redirecting to preserve user_pw
                return render(request, 'recovery.html', {'user_pw': user_pw})
            else:
                messages.error(request, 'Invalid secure question or answer. Please try again.')
        except Userreg.DoesNotExist:
            messages.error(request, 'User does not exist')

    return render(request, 'recovery.html',{'user_pw':user_pw})

def user_lists(request):
    clear_messages(request)
    
    # Get the current user's phone number from the session
    uphoneno = request.session.get('uphoneno')

    # Check if the user is logged in
    if not uphoneno:
        messages.error(request, 'Please login first')
        return redirect('/login')
    
    try:
        # Retrieve the current user
        current_user = Userreg.objects.get(phoneno=uphoneno)
        
        # Retrieve other users excluding the current user
        other_users = Userreg.objects.exclude(phoneno=uphoneno)
        
    except Userreg.DoesNotExist:
        messages.error(request, 'Please login first')
        return redirect('/login')
    return render(request, 'user_lists.html',{'current_user':current_user, 'other_users':other_users})

def start_chat(request, phoneno):
    # Check if the user is logged in
    uphoneno = request.session.get('uphoneno')
    if not uphoneno:
        messages.error(request, 'Please login first')
        return redirect('/login')
    
    try:
        # Retrieve the user to chat with
        chat_user = Userreg.objects.get(phoneno=phoneno)
        
        # Set the session for the current user chat
        request.session['chat_user_phoneno'] = chat_user.phoneno
        
        # Redirect to the chat page (assuming you have a chat page at /chat/)
        return redirect('/chat/')
    except Userreg.DoesNotExist:
        messages.error(request, 'User does not exist')
        return redirect('/login')
    
def chat(request):
    uphoneno = request.session.get('uphoneno')
    chat_user_phoneno = request.session.get('chat_user_phoneno')
    
    if not chat_user_phoneno:
        messages.error(request, 'No user selected')
        return redirect('/users')
    
    current_user_table = f"ocs{uphoneno}"
    chat_user_table = f"ocs{chat_user_phoneno}"
    
    if request.method == 'POST':
        if 'sendmessage' in request.POST:
            sendmessage = request.POST.get('sendmessage')
            fromuser = request.POST.get('fromuser')
            touser = request.POST.get('touser')
            chat_date = datetime.datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')
            
            # Save the message to the table
            with connection.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO {current_user_table} (fromuser, touser, message, chat_date) VALUES (%s, %s, %s, %s)", [fromuser, touser, sendmessage, chat_date]
                )
            
            with connection.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO {chat_user_table} (fromuser, touser, message, chat_date) VALUES (%s, %s, %s, %s)", [fromuser, touser, sendmessage, chat_date]
                )
            
            systemchat = Systemchat(fromuser=fromuser, touser=touser, message=sendmessage, chat_date=chat_date)
            systemchat.save()
            
            # Redirect to the same chat page to avoid form resubmission
            return redirect('/chat/')
        elif 'clear_chats' in request.POST:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM {current_user_table} WHERE (fromuser=%s AND touser=%s) OR (fromuser=%s AND touser=%s)", [uphoneno, chat_user_phoneno, chat_user_phoneno, uphoneno]
                )
            return redirect('/chat/')
        
    try:
        current_user = Userreg.objects.get(phoneno=uphoneno)
        chat_user = Userreg.objects.get(phoneno=chat_user_phoneno)
        
        # Fetch chats from the dynamically named table
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM {current_user_table} WHERE (fromuser=%s AND touser=%s) OR (fromuser=%s AND touser=%s) ORDER BY chatid",
                [uphoneno, chat_user_phoneno, chat_user_phoneno, uphoneno]
            )
            chats = cursor.fetchall()
        
        # Process the fetched data into a suitable format for the template
        chat_messages = []
        for chat in chats:
            chat_messages.append({
                'chatid': chat[0],
                'fromuser': chat[1],
                'touser': chat[2],
                'message': chat[3],
                'chat_date': chat[4],
            })
        
    except Userreg.DoesNotExist:
        messages.error(request, 'User does not exist')
        return redirect('/login')
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('/users')
    
    return render(request, 'chat.html', {'chat_user': chat_user, 'current_user': current_user, 'chat_messages': chat_messages, 'uphoneno':uphoneno})

def history(request):
    clear_messages(request)
    
    uphoneno = request.session.get('uphoneno')
    current_user_table = f"ocs{uphoneno}"
    # Check if the user is logged in
    if not uphoneno:
        messages.error(request, 'Please login first')
        return redirect('/login')
    
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {current_user_table}")
        return redirect('/history')

    try:
        # Fetch chats from the dynamically named table
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM {current_user_table} ORDER BY chatid")
            chats = cursor.fetchall()
        
        # Process the fetched data into a suitable format for the template
        chat_messages = []
        for chat in chats:
            chat_messages.append({
                'chatid': chat[0],
                'fromuser': chat[1],
                'touser': chat[2],
                'message': chat[3],
                'chat_date': chat[4],
            })
        
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('/users')
    return render(request, 'history.html', {'chat_messages':chat_messages})

def update_password(request):
    clear_messages(request)
    
    uphoneno = request.session.get('uphoneno')
    # Check if the user is logged in
    if not uphoneno:
        messages.error(request, 'Please login first')
        return redirect('/login')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        try:
            user_data = Userreg.objects.get(phoneno=uphoneno)
            user_data.password = password
            user_data.save()
            messages.success(request, 'Password changed successfully')
        except Userreg.DoesNotExist:
            pass

    return render(request, 'updatepw.html', {'uphoneno':uphoneno})

def change_pic(request):
    clear_messages(request)
    
    # Get the current user's phone number from the session
    uphoneno = request.session.get('uphoneno')

    # Check if the user is logged in
    if not uphoneno:
        messages.error(request, 'Please login first')
        return redirect('/login')
    
    try:
        # Retrieve the current user pic
        current_user = Userreg.objects.get(phoneno=uphoneno)
        user_pic = current_user.images

        if request.method == 'POST' and 'name' in request.FILES:
            image = request.FILES['name']
            root = settings.MEDIA_ROOT
            fs = FileSystemStorage(location=root)
            final_file_name = fs.save(image.name, image)
            current_user.images = final_file_name
            current_user.save()

            messages.success(request, 'Picture changed successfully')
    except Userreg.DoesNotExist:
        pass
    
    return render(request, 'change_pic.html',{'user_pic':user_pic})
