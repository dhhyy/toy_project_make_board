from django.urls import path
from .views      import PostingView, RePostingView, PostingDeleteView, PostingListView, PostingDetailView, ReplyPostingView

urlpatterns = [
    path('/post', PostingView.as_view()),
    path('/repost/<int:board_id>', RePostingView.as_view()),
    path('/delete/<int:board_id>', PostingDeleteView.as_view()),
    path('/list', PostingListView.as_view()),
    path('/detail/<int:board_id>', PostingDetailView.as_view()),
    path('/reply/<int:board_id>', ReplyPostingView.as_view())
]