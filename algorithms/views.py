from django.shortcuts import render,HttpResponse
import os
import copy
import subprocess
# Create your views here.
def index(request):
    algos = os.listdir('Codes/')
    data = []
    for algoname in algos:
        curr_algo = {'AlgoName':algoname,
        "cpp_code":"No",
        "py_code":"No",
        "readme":"No",
        }
        available_files = os.listdir(f'Codes/{algoname}')
        for elem in available_files:
            if elem[-2:]=="py":
                curr_algo["cpp_code"] = "Yes"
            if elem[-3:] == "cpp":
                curr_algo["py_code"] = "Yes"
            if elem[-2:] =="md":
                curr_algo["readme"] = "Yes"
        data.append(curr_algo)


    return render(request,"algorithms/index.html",{
        'data':data,
    })


def about(request):
    params = {
        'readme':open('README.md').read(),
    }
    return render(request,"algorithms/about.html",params)

def algorithms(request):
    algos = os.listdir('Codes/')
    data = []
    curr_row = []
    for index,elem in enumerate(algos):
        curr_row.append(elem)
        if (index+1)%4==0:
            data.append(copy.copy(curr_row))
            curr_row.clear()
        
    data.append(curr_row)

    params = {
       'algoname':data

    }
    return render(request,"algorithms/algorithms.html",params)

def language_page(request,algoname):
    available_files = os.listdir(f'Codes/{algoname}')
    cpp_code,py_code,readme = (False,False,False)
    for elem in available_files:
        if elem[-2:]=="py":
            py_code = True
        if elem[-3:] == "cpp":
            cpp_code = True
        if elem[-2:] =="md":
            readme = True


    params = {
        'algoname':algoname,
        'py_code':py_code,
        'cpp_code':cpp_code,
        'readme':readme,
    }
    return render(request,"algorithms/langpage.html",params)




def curr_algorithm(request,algoname,langname):
    run_code = request.GET.get('run')
    dir = os.listdir(f'Codes/{algoname}')
    params = {
        'algoname':algoname,
    }
    for elem in dir:
        if elem[-3:] == "cpp" and langname =="cpp":
            params['cpp_code'] = open(f'Codes/{algoname}/{elem}').read()
            if run_code == "true":
                output = subprocess.check_output(f"g++ Codes/{algoname}/{elem} -o run && ./run")
                params['output'] = output.decode('utf-8')
        elif elem[-2:] == "py" and langname == "py":
            params['python_code'] = open(f'Codes/{algoname}/{elem}').read()
            if run_code == "true":
                output = subprocess.check_output(f"py Codes/{algoname}/{elem}")
                params['output'] = output.decode('utf-8')
        elif elem[-2:] == "md" and langname =="readme":
            params['readme_code'] = open(f'Codes/{algoname}/{elem}').read()
    return render(request,"algorithms/curralgo.html",params)