from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    SubCommentSerializer,
    SubCommentUpdateSerializer,
    CommentSerializer,
    CommentUpdateSerializer,
    SolutionSerializer,
    SolutionUpdateSerializer,
    MiniSolutionSerializer,
    SolutionDetailSerializer,
    SolutionCountSerializer,
    CommentLikeSerializer,
)
from .models import Solution, Comment, SubComment
from problems.models import OriginProb, Problem
from users.models import User
# from pprint import pprint


class GetProblemsSolutions(APIView):
    """
    get all solutions of origin problem only whose own group's user
    """
    def get(self, request, originId):
        user = request.user
        my_group = set()
        my_group.add(user.id)
        groups = user.group.all()
        for group in groups:
            my_group |= set(group.members.values_list('id', flat=True))

        try:
            origin_prob = OriginProb.objects.get(id=originId)
        except OriginProb.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        found_solutions = origin_prob.solutions.filter(solved=True).filter(creator__id__in=my_group)
        serializer = MiniSolutionSerializer(found_solutions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProblemsQuestions(APIView):
    """
    get all Questions of origin problem only whose own group's user
    """
    def get(self, request, originId):
        user = request.user
        my_group = set()
        my_group.add(user.id)
        groups = user.group.all()
        for group in groups:
            my_group |= set(group.members.values_list('id', flat=True))

        try:
            origin_prob = OriginProb.objects.get(id=originId)
        except OriginProb.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        found_solutions = origin_prob.solutions.filter(solved=False).filter(creator__id__in=my_group)
        serializer = MiniSolutionSerializer(found_solutions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class GetQuestions(APIView):
    """
    get all questions only whose own group's user
    """
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
        solutions = user.solutions.filter(solved=False)
        serializer = MiniSolutionSerializer(solutions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetSolutions(APIView):
    """
    get all solutions only whose own group's user
    """
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
        solutions = user.solutions.filter(solved=True)
        serializer = MiniSolutionSerializer(solutions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class GetAllQuestions(APIView):
    """
    get all questions only whose own group's user
    """
    def get(self, request):
        user = request.user
        my_group = set()
        groups = user.group.all()
        for group in groups:
            my_group |= set(group.members.values_list('id', flat=True))

        solutions = Solution.objects.filter(solved=False).filter(creator__id__in=my_group)
        serializer = MiniSolutionSerializer(solutions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchQuestions(APIView):
    """
    search questions
    """
    def get(self, request, txt):
        user = request.user
        my_group = set()
        groups = user.group.all()
        for group in groups:
            my_group |= set(group.members.values_list('id', flat=True))

        solutions = set()
        found_solutions = Solution.objects.filter(creator__id__in=my_group).filter(problem__title__icontains=txt).filter(solved=False)
        solutions |= set(found_solutions)
        if txt.isdigit():
            found_solutions = Solution.objects.filter(creator__id__in=my_group).filter(problem__number=int(txt)).filter(solved=False)
            solutions |= set(found_solutions)
        serializer = MiniSolutionSerializer(solutions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetSolution(APIView):
    """
    get Solution or Question
    """
    def get(self, request, solutionId):
        try:
            found_solution = Solution.objects.get(id=solutionId)
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = SolutionDetailSerializer(found_solution)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetSolutionCounts(APIView):
    """
    get solution count
    """
    def get(self, request, solutionId):
        try:
            found_solution = Solution.objects.get(id=solutionId)
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = SolutionCountSerializer(found_solution, context={"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SolutionAPI(APIView):
    """
    Solution APIs
    """
    def post(self, request):
        """
        ### request data
        - original problem id
        - code
        - lang (c, cpp, java, python, javascript 중 하나)
        - solved
        - caption( solved가 True일 때만 받는다.)
        """
        user = request.user

        serializer = SolutionSerializer(data=request.data)
        if serializer.is_valid():
            solution = serializer.save(creator=user)
            if solution:
                if solution.solved:
                    problem = user.problems.get(origin__id=solution.problem.id)
                    if problem and not problem.is_solved:
                        problem.is_solved = True
                        problem.save()
                
                new_serializer = SolutionDetailSerializer(solution)
                return Response(new_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        """
        ### request data
        - solution id
        - code
        - lang
        - solved
        - caption
        """
        if 'id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            found_solution = Solution.objects.get(id=request.data['id'], creator=request.user)
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = SolutionUpdateSerializer(found_solution, data=request.data)
        if serializer.is_valid():
            solution = serializer.save()
            if solution:
                new_serializer = SolutionDetailSerializer(solution)
                return Response(new_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request):
        """
        ### request data
        - solution id
        """
        if 'id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            solution = Solution.objects.get(id=request.data['id'], creator=request.user)
            solution.delete()
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


class GetComments(APIView):
    """
    get Comments API
    """
    def get(self, request, solutionId):
        """
        ### request data
        - solution id
        """
        try:
            solution = Solution.objects.get(id=solutionId)
            comments = solution.comments.all()
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(comments, many=True, context={"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetCommentLikes(APIView):
    """
    get single comment's like_count
    """
    def get(self, request, commentId):
        """
        # param : comment's id
        """
        try:
            comment = Comment.objects.get(id=commentId)
            serializer = CommentLikeSerializer(comment, context={"request":request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    

class CommentAPI(APIView):
    """
    Comment APIs
    """

    def post(self, request):
        """
        ### request data
        - solution id
        - message
        """
        user = request.user
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment = serializer.save(creator=user)
            if comment:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        ### request data
        - comment id
        - message
        """
        if 'id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            found_comment = Comment.objects.get(id=request.data['id'])
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentUpdateSerializer(found_comment, data=request.data)

        if serializer.is_valid():
            comment = serializer.save()
            if comment:
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        """
        ### request data
        - comment id
        """
        if 'id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            found_comment = Comment.objects.get(id=request.data['id'])
            found_comment.delete()
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetSubComments(APIView):
    """
    get Comments API
    """
    def get(self, request, commentId):
        """
        ### request data
        - comment id
        """
        try:
            comment = Comment.objects.get(id=commentId)
            comments = comment.sub_comments.all()
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = SubCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubCommentAPI(APIView):
    """
    Comment APIs
    """
    def post(self, request):
        """
        ### request data
        - comment id
        - message
        """
        user = request.user
        serializer = SubCommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(creator=user)
            if comment:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        ### request data
        - id (subcomment id)
        - message
        """
        if 'id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            found_comment = SubComment.objects.get(id=request.data['id'])
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = SubCommentUpdateSerializer(found_comment, data=request.data)

        if serializer.is_valid():
            comment = serializer.save()
            if comment:
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        """
        ### request data
        - id (subcomment id)
        """
        if 'id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            found_comment = SubComment.objects.get(id=request.data['id'])
            found_comment.delete()
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class ViewCount(APIView):

    def get(self, request, solutionId):

        try:
            solution = Solution.objects.get(id=solutionId)
            solution.view += 1
            solution.save()
            return Response(status=status.HTTP_200_OK)
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LikeSolution(APIView):

    def get(self, request, solutionId):

        user = request.user

        try:
            found_solution = Solution.objects.get(id=solutionId)
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if user in found_solution.likes.all():
            found_solution.likes.remove(user)
        else:
            found_solution.likes.add(user)
        found_solution.save()

        return Response(status=status.HTTP_200_OK)


class LikeComment(APIView):

    def get(self, request, commentId):

        user = request.user

        try:
            comment = Comment.objects.get(id=commentId)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if user in comment.likes.all():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
        comment.save()

        return Response(status=status.HTTP_200_OK)