from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.http import HttpResponse


from online_test_app.forms import FileForm
from online_test_app.app_funcs import get_q_and_a, read_ans_from_file
from online_test_app.models import FileObject, QuestionAnswerModel, AnswerModel
# Create your views here.
import re


@csrf_exempt
def upload_form(request):
    ctx = dict()
    if request.method == 'GET':
        form = FileForm()
        ctx['form'] = form
    
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            print("Valid form")
            uploadedFile = FileObject(file = request.FILES['file'])
            uploadedFile.save()
            file = request.FILES['file']
            all_questions, all_answers = get_q_and_a(file)
            user_name = "Test_user"
            QuestionAnswerModel.objects.filter(user_name=user_name).delete()
            for indx in range(0,len(all_questions)):
                current_ques = all_questions[indx]
                current_ans = all_answers[indx]
                # print(all_answers[1])
                obj = QuestionAnswerModel.objects.create(
                                user_name = user_name,
                                qNum = indx + 1,
                                mainQ = current_ques[0],
                                subQuestion1 = current_ques[1],
                                subQuestion2 = current_ques[2],
                                subQuestion3 =current_ques[3],
                                subQuestion4 =current_ques[4],
                                ans1 = current_ans[0],
                                ans2 = current_ans[1],
                                ans3 = current_ans[2],
                                ans4 = current_ans[3],
                                selected_answer = '')
                obj.save()
                
            return redirect('/exam/quiz?page=1')
    return render(request,'index.html',ctx)

@csrf_exempt
def quiz(request):
    ctx = dict()
    print('Method', request.method)
    if request.method == 'GET':
        requested_page =request.GET['page']
        print('requested_page',requested_page)
        objects = QuestionAnswerModel.objects.all()
        total_questions = objects.count()
        p = Paginator(objects, 1)
        page_to_return = p.page(requested_page)
        page_data = page_to_return.object_list.values()
        print(page_data)
        try:

            ctx['page_data'] = page_data
            ctx['total_questions'] = total_questions
            ctx['page_object'] = page_to_return
            ctx['qNumber'] = page_data[0]['qNum']
            ctx['current_page'] = requested_page
        except Exception as e:
            print("Error")
            print(str(e))
        
        
        return render(request,'question.html',ctx)
    
    if request.method == 'POST':
        page = request.POST['page']
        answer = request.POST['answer']
        qNumber = request.POST['qNum']

        print(page,answer)
        if answer != "--Select--":
            QuestionAnswerModel.objects.filter(qNum=qNumber).update(selected_answer=answer)
        
        url = f'/exam/quiz?page={page}'
        return HttpResponse(url)


@csrf_exempt
def quiz_clear(request):
    print('Inside clear')
    qNumber = request.POST['qNum']
    page = request.POST['page']
    QuestionAnswerModel.objects.filter(qNum=qNumber).update(selected_answer='')
    url = f'/exam/quiz?page={page}'
    return HttpResponse(url)

@csrf_exempt
def ans_sheet(request):
    ctx = dict()
    if request.method == 'GET':
        form = FileForm()
        ctx['form'] = form
    
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            print("Valid form")
            uploadedFile = FileObject(file = request.FILES['file'])
            uploadedFile.save()
            file = request.FILES['file']
            answers = read_ans_from_file(file)

            corrected_answers = 0
            total_questions = 0
            skipped_questions = 0
            attempted_questions = 0
            corrected_question_nums = []
            incorrect_answ_list = []
            if answers:
                AnswerModel.objects.all().delete()
                for ans in answers:
                    qNum = int(re.sub("[a-zA-Z\. ]","",ans))
                    obj = AnswerModel.objects.create(qNum=qNum,answer=ans)
                    obj.save()
                
                submitted_ans = QuestionAnswerModel.objects.only("selected_answer", "qNum")
                total_questions = submitted_ans.count()
                submitted_ans_dict = submitted_ans.values()


                for data in submitted_ans_dict:
                    selected_answer = data['selected_answer']
                    qNum = data['qNum']

                    if len(selected_answer.strip()) > 0:
                        attempted_questions += 1
                        correct_answers = AnswerModel.objects.filter(qNum=qNum)
                        correct_answer_dict = correct_answers.values()[0]
                        correct_answer = correct_answer_dict['answer']
                        pos_dot = correct_answer.find(".")
                        answer_char = f'({str(correct_answer[pos_dot + 1:]).lower()})'
                        print(answer_char)
                        if selected_answer.strip().startswith(answer_char):
                            corrected_answers = corrected_answers + 1
                            corrected_question_nums.append(qNum)
                        else:
                            incorrect_answ_list.append(qNum)
                    else:
                        skipped_questions =+ 1
                ctx['corrected_answers'] = corrected_answers
                ctx['skipped_questions'] = total_questions - attempted_questions
                ctx['total_questions'] = total_questions
                ctx['attempted_questions'] = attempted_questions
                ctx['corrected_question_nums'] = incorrect_answ_list
                return render(request,'result.html',ctx)
            else:
                return render(request,'error.html',ctx)
    return render(request,'answer_sheet.html',ctx)