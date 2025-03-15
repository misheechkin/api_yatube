from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CommentSerializer, GroupSerializer,
                             PostSerializer, UserSerializer)
from posts.models import Group, Post, User


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вьюсет получения данных пользователей.'''
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    '''Вьюсет получения, записи и изменения постов.'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        '''Метод создания нового поста.'''
        return serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вьюсет получения данных групп пользователей.'''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)


class CommentViewSet(viewsets.ModelViewSet):
    '''Вьюсет получения, записи и изменения комментариев.'''
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly,)

    def get_queryset(self):
        '''Метод выбора всех комментариев по нужному посту.'''
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        '''Метод создания нового комментария по нужному посту.'''
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
