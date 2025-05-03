from django.shortcuts import render

from django.http import JsonResponse
from .models import User, Exam, AnswerSet, QuestionSetMapping


from django.db.models import Max


def get_or_create_user_with_incremented_id(request):
    # print()
    name = request.GET.get('first_name')
    # print(request.POST)
    print("create user")

    max_id = User.objects.aggregate(Max('id'))['id__max']
    if max_id is None:
        max_id = 0

    new_id = max_id + 1


    user, created = User.objects.get_or_create(id = new_id, first_name = name)
    if created:
        user.save()

    return JsonResponse({
        "id" : new_id
    })



def start_exam(request, user_id, exam_id):
    # user_id = request.GET.get('user_id')
    # exam_id = request.GET.get('exam_id')

    # user = User.objects.get(id=user_id)
    # user = User.objects.get_or_create(id = user_id)
    exam = Exam .objects.get(id=exam_id)
    first_name = User.objects.get(id = user_id).first_name

    # Check if the AnswerSet already exists for this user and exam
    answer_set, created = AnswerSet.objects.get_or_create(user_id=user_id, exam_id=exam_id, user_name= first_name)
    
    # if answer_set.status :
    #     return JsonResponse({'message' : "Your exam finished"})
  
    if created or not answer_set.current_question:
        
        # 
        first_question_mapping = QuestionSetMapping.objects.filter(
            question_set=exam.question_set
        ).order_by('order').first()

        if first_question_mapping:
            answer_set.current_question = first_question_mapping.question
            answer_set.save()

    return JsonResponse({
        'message': 'Exam started',
    })


def get_question(request, user_id, exam_id):
    # user_id = request.GET.get('user_id')
    # exam_id = request.GET.get('exam_id')

    user = User.objects.get(id=user_id)
    exam = Exam.objects.get(id=exam_id)

    # Get the user's answer set to find the current question
    answer_set = AnswerSet.objects.get(user=user, exam=exam)

    
    question = answer_set.current_question
    res = {
        'question': question.text,
        'options': [question.option_a,
             question.option_b,
             question.option_c,
             question.option_d],
        "answer": '4',
        "time": 55,
        
    }
    # if answer_set.status == 0:
    #     return JsonResponse({}, status=204)

    current_question = answer_set.current_question
    
    next_question_mapping = QuestionSetMapping.objects.filter(
        question_set=exam.question_set,
        order__gt=QuestionSetMapping.objects.get(question=current_question).order
    ).order_by('order').first()
    
    if next_question_mapping:
        answer_set.current_question = next_question_mapping.question
        answer_set.save()
    else :
        answer_set.status = 0
        answer_set.save()

    res['exam_status'] = answer_set.status
    return JsonResponse(res)
        
def get_score_rank_and_participants(user_id, exam_id) :
    answer_set = AnswerSet.objects.filter(exam_id=exam_id).order_by('-marks')

    total_participants = answer_set.count()

    user_ids = list(answer_set.values_list('user_id', flat=True))
    user_score = 0
    try:
        user_rank = user_ids.index(user_id) + 1
        user_score = answer_set.get(user_id=user_id, exam_id = exam_id).marks
    except ValueError:
        user_rank = None
        
    return user_score, user_rank, total_participants
    
def submit_question(request, user_id, exam_id, selected_answer):
    # user_id = request.POST.get('user_id')
    # exam_id = request.POST.get('exam_id')
    # selected_answer = request.POST.get('selected_answer')  # e.g., 'A', 'B', 'C', 'D'

    user = User.objects.get(id=user_id)
    exam = Exam.objects.get(id=exam_id)
    next_question = AnswerSet.objects.get(user=user_id, exam=exam_id).current_question
    previous_question_mapping = QuestionSetMapping.objects.filter(
        question_set=exam.question_set,
        order__lt=QuestionSetMapping.objects.get(question=next_question).order
    ).order_by('-order').first()


    # Get the user's current answer set and question
    answer_set = AnswerSet.objects.get(user=user, exam=exam)
    res = {}


    submitted_question = previous_question_mapping.question
    print(answer_set.marks)
    if submitted_question:
        # Check if the submitted answer is correct

        if selected_answer == submitted_question.correct_answer:
            answer_set.marks += 1
            answer_set.save()
    score, rank, participants = get_score_rank_and_participants(user_id, exam_id)
    print(answer_set.marks)
    print(score)
    res['score'] = score
    res['rank'] = rank
    res['participants'] = participants
    res['exam_status'] = answer_set.status
    return JsonResponse(res)
def get_short_rank(request, user_id, exam_id):
    score, rank, participants = get_score_rank_and_participants(user_id, exam_id)
    res = {
        'score': score,
        'rank': rank,
        'participants': participants
    }

    return JsonResponse(res)
def get_rank(request, exam_id):

    res = []
    rows = AnswerSet.objects.filter(exam_id=exam_id).order_by('-marks')
    rows_list = list(rows.values())
    print(rows_list)
    cnt = 1
    for row in rows_list:
        tmp = {
            "user_id" : row['user_id'],
            "user_name" : row['user_name'],
            "position": cnt,
            "score" : row['marks'],
            "status" : row['status'],
        }
        cnt += 1
        res.append(tmp)
    return JsonResponse(res, safe= False)
class Admin():
    pass
