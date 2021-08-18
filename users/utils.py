import jwt
import json

from django.http     import JsonResponse
from .models         import User
from my_settings     import SECRET_KEY, algorithm

def LoginDecorator(func):
      
      def wrapper(self, request, *arg, **kwargs):
            
            try:
              if 'Authorization' not in request.headers:
                    return JsonResponse({'message' : 'NOT_ACCESS_TOKEN'}, status=400)
                  
              encoded_token = request.headers['Authorization']
              data          = jwt.decode(encoded_token, SECRET_KEY, algorithm)    
              user          = User.objects.get(id=data['id'])
              request.user  = user
              
            except jwt.DecodeError:
              return JsonResponse({'message' : 'INVALID_TOKEN'}, status=400)
                
            except User.DoesNotExist:
              return JsonResponse({'message' : 'INVALID_USER'}, status=400)
                
            return func(self, request, *arg, **kwargs)
            
      return wrapper