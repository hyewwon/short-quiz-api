# Generated by Django 3.2.14 on 2024-06-19 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplaintType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cause', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'complaintType',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='퀴즈 제목')),
                ('question', models.CharField(max_length=255, verbose_name='문제')),
                ('question_image', models.ImageField(null=True, upload_to='image/question_image/', verbose_name='퀴즈 이미지')),
                ('options', models.CharField(max_length=255, verbose_name='정답지')),
                ('answer', models.IntegerField(verbose_name='정답')),
                ('answer_image', models.ImageField(null=True, upload_to='image/answer_image/', verbose_name='정답 이미지')),
                ('description', models.TextField(null=True, verbose_name='설명')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'quiz',
            },
        ),
        migrations.CreateModel(
            name='QuizComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reply_cnt', models.IntegerField(default=0, verbose_name='답글 수')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_comment', to='api.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_comment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'quiz_comment',
            },
        ),
        migrations.CreateModel(
            name='QuizSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(db_column='subject', max_length=255)),
            ],
            options={
                'db_table': 'quiz_subject',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='api.quizcomment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reply',
            },
        ),
        migrations.CreateModel(
            name='SolvedQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solved_at', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solved_quiz', to='api.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solved_quiz', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'solved_quiz',
            },
        ),
        migrations.CreateModel(
            name='ReplyLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='api.reply')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_like', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reply_like',
            },
        ),
        migrations.CreateModel(
            name='ReplyComplaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('compaint_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_complaint', to='api.complainttype')),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_complaint', to='api.reply')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_complaint', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reply_complaint',
            },
        ),
        migrations.CreateModel(
            name='QuizLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_like', to='api.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_like', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'quiz_like',
            },
        ),
        migrations.CreateModel(
            name='QuizComplaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('complaint_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_complaint', to='api.complainttype')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_complaint', to='api.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_complaint', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'quiz_complaint',
            },
        ),
        migrations.AddField(
            model_name='quiz',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='api.quizsubject'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quiz', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.TextField(db_column='profile_image', default='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'auth_profile',
            },
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_like', to='api.quizcomment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_like', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comment_like',
            },
        ),
        migrations.CreateModel(
            name='CommentComplaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_complaint', to='api.quizcomment')),
                ('complaint_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_complaint', to='api.complainttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_complaint', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comment_complaint',
            },
        ),
    ]