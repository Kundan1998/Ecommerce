from django.shortcuts import render, HttpResponse
from datetime import datetime, timedelta
from home import serializers
from home.models import *
from django.contrib import messages
from rest_framework import status
from rest_framework import authentication
from django.contrib.auth.hashers import make_password, check_password
# import rest_framework
import jwt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
# Create your views here.


################################################################ API ###############################################################################
@api_view(['POST'])
def store_register(request):
    if request.data['name'] == "" :
        return Response({"success":False, "message": "Name is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
    if request.data['email'] == "":
        return Response({"success":False, "message": "Email id is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
    if request.data['phone_no'] == "":
        return Response({"success":False, "message": "Phone Number is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
    if request.data['password'] == "":
        return Response({"success":False, "message": "Password is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
    if request.data['confirm_password'] == "":
        return Response({"success":False, "message": "Confirm Password is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
    if request.data['store_name'] == "":
        return Response({"success":False, "message": "Store Name is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
    email = request.data['email']
    print(request.data['email'])
    name = request.data['name']
    phone_no = request.data['phone_no']
    password = request.data['password']
    confirm_password = request.data['confirm_password']
    store_name = request.data['store_name']
    if password != confirm_password:
        return Response({"success":False, "message": "Password and Confirm Password Does not match"}, status=status.HTTP_400_BAD_REQUEST)
    if Store.objects.filter(email=email).first():
        return Response({"success":False, "message": "Email id already exist"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        password = make_password(password)
        store = Store.objects.create(name=name,email=email,phone_no=phone_no,password=password,store_name=store_name)
        serializer = StoreSerializer(store)
        payload = {
            'id':store.store_id,
            'exp': datetime.utcnow() + timedelta(days=365),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret' , algorithm='HS256').decode('utf-8')
        return Response({"success":True, "message": "Store Register Successful","data":serializer.data,"token":token }, status=status.HTTP_200_OK)
    


@api_view(['POST'])
def user_register(request):
    if request.data['name'] == "" :
        return Response({"success":False, "message": "Name is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
    if request.data['email'] == "":
        return Response({"success":False, "message": "Email id is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
    if request.data['phone_no'] == "":
        return Response({"success":False, "message": "Phone Number is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
    if request.data['password'] == "":
        return Response({"success":False, "message": "Password is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
    if request.data['confirm_password'] == "":
        return Response({"success":False, "message": "Confirm Password is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
    if request.data['country'] == "":
        return Response({"success":False, "message": "Country is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
    email = request.data['email']
    name = request.data['name']
    phone_no = request.data['phone_no']
    password = request.data['password']
    confirm_password = request.data['confirm_password']
    country = request.data['country']
    if password != confirm_password:
        return Response({"success":False, "message": "Password and Confirm Password Does not match"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).first():
        return Response({"success":False, "message": "Email id already exist"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        password = make_password(password)
        user = User.objects.create(name=name,email=email,phone_no=phone_no,password=password,country=country)
        serializer = UserSerializer(user)
        payload = {
            'id':user.user_id,
            'exp': datetime.utcnow() + timedelta(days=365),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret' , algorithm='HS256').decode('utf-8')
        return Response({"success":True, "message": "User Register Successful","data":serializer.data }, status=status.HTTP_200_OK)
    


@api_view(['POST'])
def store_login(request):
    if request.POST.get('email') == "":
        return Response({"success":False, "message": "Email Id is required" }, status=status.HTTP_400_BAD_REQUEST) 
    email = request.POST.get('email')
    if request.POST.get('password') == "":
        return Response({"success":False, "message": "Password is required" }, status=status.HTTP_400_BAD_REQUEST) 
    password = request.POST.get('password')
    if Store.objects.filter(email=email):
        store = Store.objects.filter(email=email).first()
        pass1 = store.password
        if check_password(password, pass1):
            serializer = StoreSerializer(store)
            payload = {
                'id':store.store_id,
                'exp': datetime.utcnow() + timedelta(days=365),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(payload, 'secret' , algorithm='HS256').decode('utf-8')
            return Response({"success":True, "message": "You are logged in","data":serializer.data,"token":token }, status=status.HTTP_200_OK)
        else:
            return Response({"success":False, "message": "Password is Invalid" }, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"success":False, "message": "Email is Invalid" }, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['POST'])
def user_login(request):
    if request.POST.get('email') == "":
        return Response({"success":False, "message": "Email Id is required" }, status=status.HTTP_400_BAD_REQUEST) 
    email = request.POST.get('email')
    if request.POST.get('password') == "":
        return Response({"success":False, "message": "Password is required" }, status=status.HTTP_400_BAD_REQUEST) 
    password = request.POST.get('password')
    if User.objects.filter(email=email):
        user = User.objects.filter(email=email).first()
        pass1 = user.password
        if check_password(password, pass1):
            serializer = UserSerializer(user)
            payload = {
                'id':user.user_id,
                'exp': datetime.utcnow() + timedelta(days=365),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(payload, 'secret' , algorithm='HS256').decode('utf-8')
            return Response({"success":True, "message": "You are logged in","data":serializer.data,"token":token }, status=status.HTTP_200_OK)
        else:
            return Response({"success":False, "message": "Password is Invalid" }, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"success":False, "message": "Email is Invalid" }, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['POST'])
def add_product(request):
    auth = authentication.get_authorization_header(request).split()
    if auth:
        aaa = str(auth[1].split())
        sss = aaa.split("'")
        token = sss[1]
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except:
            return Response({"success":False, "message": "Token is expired or invalid"},status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"success":False, "message": "Token is required"},status=status.HTTP_400_BAD_REQUEST)
    store = Store.objects.filter(store_id=payload['id']).first()
    if store:
        if request.data['product_name'] == "" :
            return Response({"success":False, "message": "Product Name is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        if request.data['product_image'] == "":
            return Response({"success":False, "message": "Product Image is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        if request.data['price'] == "":
            return Response({"success":False, "message": "Price is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        if request.data['description'] == "":
            return Response({"success":False, "message": "Description is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        if request.data['quantity'] == "":
            return Response({"success":False, "message": "Quantity is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        quantity = request.data['quantity']
        if int(quantity) <= 0:
            return Response({"success":False, "message": "Please Enter quantity greater then zero" }, status=status.HTTP_401_UNAUTHORIZED)
        product_name = request.data['product_name']
        product_image = request.data['product_image']
        price = request.data['price']
        description = request.data['description'] 
        product = Product.objects.create(product_name=product_name,product_image=product_image,price=price,quantity=quantity,description=description,store_id=store)
        serializer = ProductSerializer(product)
        return Response({"success":True, "message": "Prodcut Added successfully.", "product":serializer.data }, status=status.HTTP_200_OK)
    else:
        return Response({"success":False, "message": "Please Send valid token" }, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['POST'])
def update_product(request):
    auth = authentication.get_authorization_header(request).split()
    if auth:
        aaa = str(auth[1].split())
        sss = aaa.split("'")
        token = sss[1]
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except:
            return Response({"success":False, "message": "Token is expired or invalid"},status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"success":False, "message": "Token is required"},status=status.HTTP_400_BAD_REQUEST)
    store = Store.objects.filter(store_id=payload['id']).first()
    store_id = store.store_id
    if store:
        if request.data['product_id'] == "" :
            return Response({"success":False, "message": "Product Id is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        product_id = request.data['product_id']
        if Product.objects.filter(product_id=product_id,store_id=store_id).first() == None:
            return Response({"success":False, "message": "Enter valid product Id" }, status=status.HTTP_401_UNAUTHORIZED)
        if request.data['product_name'] == "" :
            return Response({"success":False, "message": "Product Name is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        if request.data['price'] == "":
            return Response({"success":False, "message": "Price is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        if request.data['description'] == "":
            return Response({"success":False, "message": "Description is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        if request.data['quantity'] == "":
            return Response({"success":False, "message": "Quantity is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        quantity = request.data['quantity']
        if int(quantity) <= 0:
            return Response({"success":False, "message": "Please Enter quantity greater then zero" }, status=status.HTTP_401_UNAUTHORIZED)
        product = Product.objects.filter(product_id=product_id).first()
        product.product_name = request.data['product_name']
        product.price = request.data['price']
        product.description = request.data['description']
        product.quantity = quantity 
        if request.data['product_image']:
            product.product_image = request.data['product_image']
        product.save()
        serializer = ProductSerializer(product)
        return Response({"success":True, "message": "Prodcut Update successfully.", "product":serializer.data }, status=status.HTTP_200_OK)
    else:
        return Response({"success":False, "message": "Please Send valid token" }, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['POST'])
def delete_product(request):
    auth = authentication.get_authorization_header(request).split()
    if auth:
        aaa = str(auth[1].split())
        sss = aaa.split("'")
        token = sss[1]
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except:
            return Response({"success":False, "message": "Token is expired or invalid"},status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"success":False, "message": "Token is required"},status=status.HTTP_400_BAD_REQUEST)
    store = Store.objects.filter(store_id=payload['id']).first()
    store_id = store.store_id
    if store:
        if request.data['product_id'] == "" :
            return Response({"success":False, "message": "Product Id is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        product_id = request.data['product_id']
        if Product.objects.filter(product_id=product_id,store_id=store_id).first() == None:
            return Response({"success":False, "message": "Enter valid product Id" }, status=status.HTTP_401_UNAUTHORIZED)
        Product.objects.filter(product_id=product_id,store_id=store_id).delete()
        return Response({"success":True, "message": "Prodcut deleted successfully."}, status=status.HTTP_200_OK)
    else:
        return Response({"success":False, "message": "Please Send valid token" }, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['Get'])
def store_product_list(request):
    auth = authentication.get_authorization_header(request).split()
    if auth:
        aaa = str(auth[1].split())
        sss = aaa.split("'")
        token = sss[1]
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except:
            return Response({"success":False, "message": "Token is expired or invalid"},status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"success":False, "message": "Token is required"},status=status.HTTP_400_BAD_REQUEST)
    store = Store.objects.filter(store_id=payload['id']).first()
    if store:
        serializer = StoreProductSerializer(store)
        return Response({"success":True, "message": "Store's Product List", "product":serializer.data }, status=status.HTTP_200_OK)
    else:
        return Response({"success":False, "message": "Please Send valid token" }, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['Get'])
def user_store_list(request):
    auth = authentication.get_authorization_header(request).split()
    if auth:
        aaa = str(auth[1].split())
        sss = aaa.split("'")
        token = sss[1]
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except:
            return Response({"success":False, "message": "Token is expired or invalid"},status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"success":False, "message": "Token is required"},status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(user_id=payload['id']).first()
    if user:
        store = Store.objects.all()
        serializer = StoreSerializer(store,many=True)
        return Response({"success":True, "message": "Store List", "store":serializer.data }, status=status.HTTP_200_OK)
    else:
        return Response({"success":False, "message": "Please Send valid token" }, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['POST'])
def product_of_store_list(request):
    auth = authentication.get_authorization_header(request).split()
    if auth:
        aaa = str(auth[1].split())
        sss = aaa.split("'")
        token = sss[1]
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except:
            return Response({"success":False, "message": "Token is expired or invalid"},status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"success":False, "message": "Token is required"},status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(user_id=payload['id']).first()
    if user:
        if request.data['store_id'] == "" :
            return Response({"success":False, "message": "Store Id is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        store_id = request.data['store_id']
        if Store.objects.filter(store_id=store_id).first() == None:
            return Response({"success":False, "message": "Enter valid Store Id" }, status=status.HTTP_401_UNAUTHORIZED)
        product = Product.objects.filter(store_id=store_id)
        serializer = ProductSerializer(product,many=True)
        return Response({"success":True, "message": "Product List", "product":serializer.data }, status=status.HTTP_200_OK)
    else:
        return Response({"success":False, "message": "Please Send valid token" }, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
def add_to_cart(request):
    auth = authentication.get_authorization_header(request).split()
    if auth:
        aaa = str(auth[1].split())
        sss = aaa.split("'")
        token = sss[1]
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except:
            return Response({"success":False, "message": "Token is expired or invalid"},status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"success":False, "message": "Token is required"},status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(user_id=payload['id']).first()
    user_id = user.user_id
    if user:
        if request.data['product_id'] == "" :
            return Response({"success":False, "message": "Product Id is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        product_id = request.data['product_id']
        if Product.objects.filter(product_id=product_id).first() == None:
            return Response({"success":False, "message": "Enter valid product Id" }, status=status.HTTP_401_UNAUTHORIZED)
        if request.data['quantity'] == "":
            return Response({"success":False, "message": "Quantity is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.filter(product_id=product_id).first()
        quantity = int(request.data['quantity'])
        if quantity <= 0:
            return Response({"success":False, "message": "Please Enter quantity greater then zero" }, status=status.HTTP_401_UNAUTHORIZED)
        if quantity > product.quantity:
            return Response({"success":False, "message": "You can only order "+str(product.quantity)+" item." }, status=status.HTTP_401_UNAUTHORIZED)
        if Cart.objects.filter(product_id=product_id,user_id=user_id):
            cart = Cart.objects.filter(product_id=product_id,user_id=user_id).first()
            cart.quantity = quantity
            cart.price = quantity*product.price
            cart.save()
        else:
            cart = Cart.objects.create(user_id_id = user_id,product_id_id=product_id,quantity=quantity,price=quantity*product.price)
        serializer = CartSerializer(cart)
        return Response({"success":True, "message": "Cart detail", "cart":serializer.data }, status=status.HTTP_200_OK)
    else:
        return Response({"success":False, "message": "Please Send valid token" }, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['POST'])
def update_cart(request):
    auth = authentication.get_authorization_header(request).split()
    if auth:
        aaa = str(auth[1].split())
        sss = aaa.split("'")
        token = sss[1]
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except:
            return Response({"success":False, "message": "Token is expired or invalid"},status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"success":False, "message": "Token is required"},status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(user_id=payload['id']).first()
    user_id = user.user_id
    if user:
        if request.data['cart_id'] == "" :
            return Response({"success":False, "message": "Cart Id is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        cart_id = request.data['cart_id']
        if Cart.objects.filter(cart_id=cart_id).first() == None:
            return Response({"success":False, "message": "Enter valid Cart Id" }, status=status.HTTP_401_UNAUTHORIZED)
        if request.data['quantity'] == "":
            return Response({"success":False, "message": "Quantity is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        cart = Cart.objects.filter(cart_id=cart_id).first()
        quantity = int(request.data['quantity'])
        if quantity <= 0:
            return Response({"success":False, "message": "Please Enter quantity greater then zero" }, status=status.HTTP_401_UNAUTHORIZED)
        if quantity > cart.product_id.quantity:
            return Response({"success":False, "message": "You can only order "+cart.product_id.quantity+" item." }, status=status.HTTP_401_UNAUTHORIZED)
        cart.quantity = quantity
        cart.price = quantity*cart.product_id.price
        cart.save()
        serializer = CartSerializer(cart)
        return Response({"success":True, "message": "Cart detail", "cart":serializer.data }, status=status.HTTP_200_OK)
    else:
        return Response({"success":False, "message": "Please Send valid token" }, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
def remove_signle_item(request):
    auth = authentication.get_authorization_header(request).split()
    if auth:
        aaa = str(auth[1].split())
        sss = aaa.split("'")
        token = sss[1]
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except:
            return Response({"success":False, "message": "Token is expired or invalid"},status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"success":False, "message": "Token is required"},status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(user_id=payload['id']).first()
    user_id = user.user_id
    if user:
        if request.data['cart_id'] == "" :
            return Response({"success":False, "message": "Cart Id is required","status":400 }, status=status.HTTP_400_BAD_REQUEST)
        cart_id = request.data['cart_id']
        if Cart.objects.filter(cart_id=cart_id).first() == None:
            return Response({"success":False, "message": "Enter valid Cart Id" }, status=status.HTTP_401_UNAUTHORIZED)
        cart = Cart.objects.filter(cart_id=cart_id,user_id=user_id).delete()
        return Response({"success":True, "message": "Cart Deleted successfully",}, status=status.HTTP_200_OK)
    else:
        return Response({"success":False, "message": "Please Send valid token" }, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['Get'])
def remove_all_item(request):
    auth = authentication.get_authorization_header(request).split()
    if auth:
        aaa = str(auth[1].split())
        sss = aaa.split("'")
        token = sss[1]
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except:
            return Response({"success":False, "message": "Token is expired or invalid"},status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"success":False, "message": "Token is required"},status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(user_id=payload['id']).first()
    user_id = user.user_id
    if user:
        cart = Cart.objects.filter(user_id=user_id).delete()
        return Response({"success":True, "message": "All Cart Item Deleted successfully",}, status=status.HTTP_200_OK)
    else:
        return Response({"success":False, "message": "Please Send valid token" }, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['Get'])
def cart_detail(request):
    auth = authentication.get_authorization_header(request).split()
    if auth:
        aaa = str(auth[1].split())
        sss = aaa.split("'")
        token = sss[1]
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except:
            return Response({"success":False, "message": "Token is expired or invalid"},status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"success":False, "message": "Token is required"},status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(user_id=payload['id']).first()
    user_id = user.user_id
    if user:
        cart = Cart.objects.filter(user_id=user_id)
        serializer = CartSerializer(cart, many=True)
        total_price = 0
        for i in cart:
            total_price += i.price
        return Response({"success":True, "message": "Cart Detail","cart":serializer.data,"total_price":total_price}, status=status.HTTP_200_OK)
    else:
        return Response({"success":False, "message": "Please Send valid token" }, status=status.HTTP_401_UNAUTHORIZED)