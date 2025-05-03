from django.db import models
class User(models.Model):
    # username = models.CharField(max_length=150, unique=True)
    # email = models.EmailField(unique=True)
    # password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username

class Question(models.Model):
    text = models.CharField(max_length=300)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D')
    ])

    def __str__(self):
        return self.text

class QuestionSet(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class QuestionQuestionSetMapper(models.Model):
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        unique_together = ('question_set', 'question')
        ordering = ['order']

    def __str__(self):
        return f"{self.question_set.name} - {self.question.text} (Order: {self.order})"

class QuestionSetMapping(models.Model):
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        unique_together = ('question_set', 'question')
        ordering = ['order']

    def __str__(self):
        return f"{self.question_set.name} - {self.question.text} (Order: {self.order})"

class Exam(models.Model):
    name = models.CharField(max_length=100)
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AnswerSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    current_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    marks = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    user_name = models.TextField(max_length=100, default="name")

    class Meta:
        unique_together = ('user', 'exam')

    # def __str__(self):
    #     return f"{self.user.username} - {self.exam.name} - Marks: {self.marks}"

