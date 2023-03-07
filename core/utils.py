import jwt
from growth_guide.settings import SECRET_KEY

def checking_admin_login(request):
    if 'token' in request.session:
        token=request.session['token']
        decoded_data=jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if decoded_data['username'] == 'admin' and decoded_data['password'] == 'admin':
            return True
        else:
            return False