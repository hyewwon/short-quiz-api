from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_image = models.TextField(default='', db_column='profile_image')

    class Meta:
        db_table='auth_profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, oauth_type='')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# 퀴즈 주제
class QuizSubject(models.Model):
    subject = models.CharField(db_column='subject', max_length=255)

    class Meta:
        db_table = 'quiz_subject'

# 퀴즈
class Quiz(models.Model):
    subject = models.ForeignKey(QuizSubject, on_delete=models.CASCADE, related_name='quiz')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='quiz')
    title = models.CharField(null=False, max_length=255, verbose_name="퀴즈 제목")
    question = models.CharField(null=False, max_length=255, verbose_name="문제")
    question_image = models.ImageField(null=True, verbose_name="퀴즈 이미지",upload_to="image/question_image/")
    options = models.CharField(null=False, max_length=255, verbose_name="정답지")
    answer = models.IntegerField(null=False, verbose_name="정답")
    answer_image = models.ImageField(null=True, verbose_name="정답 이미지", upload_to="image/answer_image/")
    description = models.TextField(null=True, verbose_name="설명")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quiz'

# 푼 문제
class SolvedQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="solved_quiz")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="solved_quiz")
    solved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "solved_quiz"


# 신고 유형
class ComplaintType(models.Model):
    cause = models.CharField(null=False, max_length=255)

    class Meta:
        db_table = 'complaintType'


# 퀴즈 신고
class QuizComplaint(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_complaint")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_complaint")
    complaint_type = models.ForeignKey(ComplaintType, on_delete=models.CASCADE, related_name="quiz_complaint")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quiz_complaint'
    

# 퀴즈 좋아요 
class QuizLike(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_like")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_like")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quiz_like'


# 퀴즈 댓글
class QuizComment(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_comment")
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reply_cnt = models.IntegerField(default=0, verbose_name="답글 수")

    class Meta:
        db_table = 'quiz_comment'


# 댓글 신고
class CommentComplaint(models.Model):
    comment = models.ForeignKey(QuizComment, on_delete=models.CASCADE, related_name="comment_complaint")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_complaint")
    complaint_type = models.ForeignKey(ComplaintType, on_delete=models.CASCADE, related_name="comment_complaint")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment_complaint'


#댓글 좋아요
class CommentLike(models.Model):
    comment = models.ForeignKey(QuizComment, on_delete=models.CASCADE, related_name="comment_like")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_like")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment_like'


# 대댓글
class Reply(models.Model):
    comment = models.ForeignKey(QuizComment, on_delete=models.CASCADE, related_name="reply")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reply")
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reply'


# 대댓글 신고
class ReplyComplaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reply_complaint")
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name="reply_complaint")
    compaint_type = models.ForeignKey(ComplaintType, on_delete=models.CASCADE, related_name="reply_complaint")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reply_complaint'


# 대댓글 좋아요
class ReplyLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reply_like")
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name="reply")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reply_like'
    



