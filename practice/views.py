from django.shortcuts import render
from django.core.files import File
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import SnippetForm,EditorForm,IDEForm
from .models import Snippet,Input,Question,OnlineIDE,Input1,Practice
from django.views.generic import CreateView
import subprocess
import json
import re
import threading
import sys

def submission(request, query):
    snippets = Snippet.objects.filter(que_id = query)
    return render(request, 'practice/submission_list.html', {"snippets":snippets})

def show_submission(request, query):
    form = EditorForm()
    snippets = Snippet.objects.filter(id=query)
    questions = ""
    text = ""

    for snippet in snippets:
        questions = Question.objects.filter(question=snippet.que_id)
    for snippet in snippets:
        text = snippet.text

    return render(request, 'practice/showSubmission.html', {'snippets':snippets,'questions':questions,'form':form, 'text':text, 'query':query})

def post_practice(request, **kwargs):
    context = {
        'practices':Practice.objects.all()
    }
    return render(request, 'practice/post_practice.html', context)

class PracticeCreateView(LoginRequiredMixin, CreateView):
    model = Practice
    fields = ['question', 'answer']

    def form_valid(self, form):
        return super().form_valid(form)

@login_required
def practice_ide(request, query):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            input = Input()
            input.input_program = request.POST.get('input_program')
            input.changeoption=request.POST.get('changeoption')
            source = input.input_program
            input_data = bytes(source,"UTF-8")
            f = open('practice/files/program.cpp','w+')
            myFile = File(f)
            doc = str(Snippet.objects.filter(author=request.user).first().text)
            myFile.write(doc)
            myFile.close()
            f.close()
            p1 = subprocess.run('g++ practice/files/program.cpp -o practice/files/program.exe',capture_output=True,text=True,shell = False)
            if(p1.stderr):
                result_compiler = str(p1.stderr,"UTF-8")
                return render(request,"practice/practice_online.html",{"form":form,"result":result_compiler})
            else:
                p2 = subprocess.run('practice/files/program.exe',input=input_data,capture_output=True,shell=False)
                return render(request, "practice/practice_online.html", {
                    "form": form,
                    "snippets": Snippet.objects.first(),"result":p2.stdout.decode("UTF-8")
                })

    else:
        form = SnippetForm()

    return render(request, 'practice/practice_online.html',{
    "form": form,
    "snippets": Snippet.objects.first(),
    "user":request.user,
    "query":query
    })

@login_required
def online_ide(request):
    threadLock = threading.Lock()
    if request.method == "POST":
        form = IDEForm(request.POST)
        if form.is_valid():
            threadLock.acquire()
            form.save()
            input = Input1()
            input.input_program1 = request.POST.get('input_program1')
            input.changeoption=int(request.POST['changeoption'])
            source = input.input_program1
            print(input.changeoption)
            input_data = bytes(source,"UTF-8")
            if(input.changeoption==1):
                f = open('practice/files/program1.cpp','w+')
                myFile = File(f)
                doc = str(OnlineIDE.objects.filter(author=request.user).first().text)
                myFile.write(doc)
                myFile.close()
                f.close()
                subprocess.call(['g++',"practice/files/program1.cpp"])
            #r=open("practice/files/file.txt",'w')
                subprocess.call("./a.out")
                t=subprocess.check_output('./a.out', shell=True)
                #threadLock.release()
                f1= open('practice/files/file.txt', 'wb')
                f1.write(t)
                f1.close()
            elif(input.changeoption==3):
                f = open('practice/files/program1.py','w+')
                myFile = File(f)
                doc = str(OnlineIDE.objects.filter(author=request.user).first().text)
                myFile.write(doc)
                myFile.close()
                f.close()
                subprocess.call(['python3',"practice/files/program1.py"])
            #r=open("practice/files/file.txt",'w')
                #subprocess.call("./a.out")
                t=subprocess.check_output('./a.out', shell=True)
                #threadLock.release()
                f1= open('practice/files/file.txt', 'wb')
                f1.write(t)
                f1.close()
            else:
                f = open('practice/files/program1.java','w+')
                myFile = File(f)
                doc = str(OnlineIDE.objects.filter(author=request.user).first().text)
                myFile.write(doc)
                myFile.close()
                f.close()
                subprocess.call(['javac',"practice/files/program1.java"])
            #r=open("practice/files/file.txt",'w')
                subprocess.call("./a.out")
                t=subprocess.check_output('./a.out', shell=True)
                #threadLock.release()
                f1= open('practice/files/file.txt', 'wb')
                f1.write(t)
                f1.close()
            
           # stdoutorigin=sys.stdout
            #sys.stdout=open('practice/files/file.txt','w');
           
           # sys.stdout.close()
            #sys.stdout=stdoutorigin
            threadLock.release()
            #f1= open('practice/files/file.txt', 'w')
           # f1.write(t)
            #file_content = f.read()
            return render(request, "practice/online_IDE.html", {
                    "form": form,
                    "codes": OnlineIDE.objects.first(),"result":t
                })
    else:
        form = IDEForm()
        return render(request, 'practice/online_IDE.html', {
        "form":form,
        "user":request.user,
        })
