import json
from django.db.models.expressions import RawSQL
from django.utils.regex_helper import Group
import requests
import bcrypt

from django.views        import View
from django.http         import HttpResponse, JsonResponse
from boards.models       import Board, Tag
from users.utils         import LoginDecorator
from users.views         import User
from django.forms.models import model_to_dict
from django.db.models    import F, Count, Case, When
from django.db           import connection

class PostingView(View):
    @LoginDecorator
    def post(self, request):
        
        try:
            data = json.loads(request.body)
            
            title   = data['title']
            content = data['content']
            writer  = request.user
            
            if not title or not content:
                return JsonResponse({'message' : 'CHECK_YOUR_INPUT'}, status=400)
            
            if Board.objects.filter(title=title).exists():
                return JsonResponse({'message' : 'SAME_TITLE, CHANGE TITLE'}, status=400)
            
            board = Board(
                title     = title,
                content   = content,
                writer    = writer,
                password  = request.user.password,
                tag       = Tag.objects.get(id=1)
            )
            
            board.save()
            
            board.groupno = board.id
            board.save()

            return JsonResponse({'message' : data}, status=200)
            
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
class RePostingView(View):
    @LoginDecorator
    def post(self, request, board_id):
        try:
            data = json.loads(request.body)
            
            title    = data['title']
            content  = data['content']
            password = data['password']
            
            board = Board.objects.get(id=board_id)
            
            if not bcrypt.checkpw(password.encode('utf-8'), board.password.encode('utf-8')):
                JsonResponse({'message' : 'NOT_MATCHED_PASSWORD'}, status=400)

            board.title = title
            board.content = content
            
            board.save()
            
            return JsonResponse({'message' : 'SUCCESS'})
            
        except KeyError:
            JsonResponse({'message' : 'KEY_ERROR'}, status=400)
            
class PostingDeleteView(View):
    @LoginDecorator
    def post(self, request, board_id):
        
        try:
            data = json.loads(request.body)
            
            password = data['password']
            
            board = Board.objects.get(id=board_id)
            
            if not bcrypt.checkpw(password.encode('utf-8'), board.password.encode('utf-8')):        
                JsonResponse({'message' : 'NOT_MATCHED_PASSWORD'}, status=400)
                
            board.delete()
        
            return JsonResponse({'message' : 'SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'})

# 정렬 기능 수정 필요
class PostingListView(View):
    def get(self, request):
        
        limit           = int(request.GET.get('limit', 0))
        offset          = int(request.GET.get('offset', 0))
        order_condition = request.GET.get('order',None) 
        
        post_type_ordering = Case(
            When(
                tag_id=1, then=1),
                default=0
            )
        
        boards = Board.objects.all().annotate(ordering=post_type_ordering).order_by('groupno', 'orderno')
        
        if order_condition == "hits":
            boards = Board.objects.order_by("hits")
            
        if order_condition == "recents":
            boards = Board.objects.order_by("create_at")
        
        post_list = [
            {
                'id'        : board.id,
                'title'     : board.title,
                'content'   : board.content,
                'hits'      : board.hits,
                'groupno'   : board.groupno,
                'orderno'   : board.orderno,
                'depth'     : board.depth,
                'writer'    : board.writer.name,
                'tag'       : board.tag.name,
                'create_at' : board.create_at
                } for board in boards][offset:limit]
                
        return JsonResponse({'message' : post_list}, status=200)
    
class PostingDetailView(View):
    def get(self, request, board_id):
        try:
            if not board_id:
                return JsonResponse({'message' : 'CHECK_BOARD_ID'}, status=401)
            
            boards = Board.objects.filter(id=board_id)
            
            # get으로 가져오는 방법 강구
            # 조회수 늘리는 건 방법이 다양한 것 같다. 찾아보고 바꾸기
            for board in boards:
                board.hits += 1
                board.save()
            
            data = [
                {
                    'id'      : board.id,
                    'title'   : board.title,
                    'content' : board.content,
                    'hits'    : board.hits,
                    'groupno' : board.groupno,
                    'orderno' : board.orderno,
                    'depth'   : board.depth,
                    'writer'  : board.writer.name,
                    'tag'     : board.tag.name
                    } for board in boards]
            
            return JsonResponse({'message' : data}, status=200)
                
        except KeyError:
            JsonResponse({'message' : 'KEY_ERROR'}, status=400)
            
class ReplyPostingView(View):
    @LoginDecorator
    def post(self, request, board_id):
        
        try:
            if not board_id:
                return JsonResponse({'message' : 'CHECK_BOARD_ID'}, status=401)         
            
            data = json.loads(request.body)
            
            title = data['title']
            content = data['content']
            writer = request.user
            
            board1 = Board.objects.get(id=board_id)
            
            reply_list = Board.objects.filter(groupno=board1.groupno, orderno__gt=board1.orderno)
            
            board2 = Board(
                title    = title,
                content  = content,
                writer   = writer,
                password = request.user.password,
                tag      = Tag.objects.get(id=1)
            )
            
            board2.save()
            
            if reply_list:
                reply_list.update(orderno=F('orderno') + 1)
            
            board2.groupno = board1.groupno
            board2.orderno = board1.orderno+1
            board2.depth   = board1.depth+1
            
            board2.save()

            return JsonResponse({'message' : 'SUCCESS'}, status=200)
        
        except KeyError:
            JsonResponse({'message' : 'KEY_ERROR'}, status=400)    