# Contest Api

- **GET /contest**
return list of contests
Response:
[ {
    "contest_id" : "xxx",
    "contest_name" : "xxx",
    "start_time" : "xxx"
}
]

- **POST /contest/**
create contest
Request: {
    "contest_name" : "xxx"
}

- **POST /contest/{contestId}/submit/**
Request:
{
    "contest_id" : "xxx",
    "user_id" : "xxx",
    "marks" : "xxx"
}

- **GET /contest/{id}**
Get all questions of the contest
Response:
[
    {
        "question_id" : "xxx",
        "question" : "xxx",
        "option_a" : "xxx",
        "option_b" : "xxx",
        "option_c" : "xxx",
        "option_d" : "xxx"
    }
]
- **POST /contests/{contestId}/problems**
Add problems to a contest
Request:
{
    problems : [x, y, z]
}

- **GET /contest/{id}/standings** 
Get the ranking of the contest
Response:
[
    {
        "user_id" : xxx
        "user_name" : xxx
    }
]
- **GET /problems/**
Response:
[
    {
        "problem_id" : "xxx",
        "question" : "xxx",
        "option_a" : "xxx",
        "option_b" : "xxx",
        "option_c" : "xxx",
        "option_d" " "xxx"
    }
]
- **POST /problems/**
Request: 
{
    "problem_id" : "xxx",
    "question" : "xxx",
    "option_a" : "xxx",
    "option_b" : "xxx",
    "option_c" : "xxx",
    "option_d" " "xxx"
}

Tables:
problem, contest, submission, user

get /contest/{id}/rankings/short 
get /contest/{id}/questions/next 
post /contest/{id}/questions/question_id/answers

post /exams/{examId}/ 
get /exams/{examId}/ratings/ 
get /exams/{examId}/standings/ 
post /exams/{examId}/users/{userId}/answers/
get exams/{examId}/users/{userId}/questions/next/ 


# Admin Api
exam/admin/question-sets/

contest -> get
contest -> post
contest/{id} -> get
contest/{id} -> put
contest/{id} -> delete                                                                                                                                                                                                                                            
