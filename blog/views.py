from django.shortcuts import render
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Post, Comment, Like, PostView
from .permission import IsOwnerOrAdminDeleteOnly, IsCommentOwnerOrAdminDeleteOnly
from .serializer import PostSerializer, CommentSerializer
# Create your views here.

class PostListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')

        search = request.query_params.get('search')
        author = request.query_params.get('author')

        if search:
            posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))
        if author:
            posts = posts.filter(author__username__icontains=author)

        total_count = posts.count()
        page_size = int(request.query_params.get('page_size', 5))  
        page = int(request.query_params.get('page', 1))

        start = (page - 1) * page_size
        end = page * page_size
        paginated_posts = posts[start:end]

        serializer = PostSerializer(paginated_posts, many=True)
        return Response({
    'msg': "Post list",
    'total_count': total_count,  
    'page': page,                
    'page_size': page_size,      
    'posts': serializer.data     
}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response({
            'msg': "Post created",
            'post': serializer.data
        }, status=status.HTTP_201_CREATED)

class PostDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdminDeleteOnly]

    def get_object(self, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(self.request, post)
        return post

    def get(self, request, pk):
        post = self.get_object(pk)
        if request.user.is_authenticated:
            PostView.objects.update_or_create(post=post, user=request.user)

        serializer = PostSerializer(post)
        return Response({
            'msg': "Post detail",
            'post': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(instance=post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'msg': "Post updated",
            'post': serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(instance=post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'msg': "Post partial updated",
            'post': serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response({
            'msg': "Post deleted",
        }, status=status.HTTP_200_OK)

class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            return Response({
                'msg': "Like olib tashlandi",
                'liked': False
            }, status=status.HTTP_200_OK)
        return Response({
            'msg': "Like bosildi",
            'liked': True
        }, status=status.HTTP_201_CREATED)


class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, post_pk):
        comments = Comment.objects.filter(post_id=post_pk)
        search = request.query_params.get('search')
        if search:
            comments = comments.filter(text__icontains=search)

        total_count = comments.count()
        page_size = int(request.query_params.get('page_size', 10))
        page = int(request.query_params.get('page', 1))

        start = (page - 1) * page_size
        end = page * page_size
        paginated_comments = comments[start:end]
        serializer = CommentSerializer(paginated_comments, many=True)
        return Response({
            'msg': "Comment list",
            'total_count': total_count,
            'page': page,
            'page_size': page_size,
            'comments': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, post_pk):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, post_id=post_pk)
        return Response({
            'msg': "Comment created",
            'comment': serializer.data
        }, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentOwnerOrAdminDeleteOnly]

    def get_object(self, pk, post_pk):
        comment = get_object_or_404(Comment, pk=pk, post_id=post_pk)
        self.check_object_permissions(self.request, comment)
        return comment

    def get(self, request, pk, post_pk):
        comment = self.get_object(pk, post_pk)
        serializer = CommentSerializer(comment)
        return Response({
            'msg': "Comment detail",
            'comment': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk, post_pk):
        comment = self.get_object(pk, post_pk)
        serializer = CommentSerializer(instance=comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'msg': "Comment updated",
            'comment': serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, pk, post_pk):
        comment = self.get_object(pk, post_pk)
        serializer = CommentSerializer(instance=comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'msg': "Comment partial updated",
            'comment': serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk, post_pk):
        comment = self.get_object(pk, post_pk)
        comment.delete()
        return Response({
            'msg': "Comment deleted",
        }, status=status.HTTP_200_OK)