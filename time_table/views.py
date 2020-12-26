from django.shortcuts import render
from django.http import HttpResponse
from .excel import Table, raw_to_str
from .forms import RawForm, DataForm


raw = '''1 	수리정보과학부 	자연계열교과핵심 	수학2 	4 	1 	정명주 	월3|월4|화2|수1|목5 	3 	18 	15
2 	화학생물학부 	자연계열교과핵심 	생물학및실험2 	3 	1 	권창섭 	월5|수2|목1 	6 	18 	16
3 	인문예술학부 	인문계열교과핵심 	한국사의이해 	3 	1 	강재순 	월6|목2|금1 	3 	18 	15
4 	인문예술학부 	인문계열교과핵심 	미술 	2 	1 	박주영 	화6|화7 	2 	18 	17
5 	수리정보과학부 	자연계열교과심화 	자료구조 	3 	2 	김호숙 	화1|수4|금2 	1 	18 	18
6 	화학생물학부 	자연계열교과핵심 	화학및실험2 	3 	1 	탁주환 	목4|금5|금6 	5 	18 	17
7 	인문예술학부 	인문계열교과핵심 	체육2 	1 	1 	이종훈 	금3 	9 	18 	14
8 	인문예술학부 	인문계열교과핵심 	영어2 	3 	1 	Kevin Anderson 	화3|수6|목6 	8 	18 	16
9 	물리지구과학부 	자연계열교과핵심 	물리학및실험2 	3 	1 	이정훈 	월7|월8|화5|금4 	1 	18 	15'''
default_links = 'Zoom, Google Meet'


def home_view(request):
    if request.method == 'GET':
        context = {'form': RawForm()}
        return render(request, 'raw_input.html', context=context)
    elif request.method == 'POST':
        if 'raw_data' in request.POST:
            raw_form = RawForm(request.POST)
            if raw_form.is_valid():
                data = raw_form.cleaned_data
                lecture_str = raw_to_str(data['raw_data'])
                data_form = DataForm({'lecture_data': lecture_str, 'links': default_links})
                context = {'form': data_form}
                return render(request, 'data_input.html', context=context)
            else:
                context = {'form': raw_form}
                return render(request, 'raw_input.html', context=context)
        elif 'lecture_data' in request.POST:
            data_form = DataForm(request.POST)
            if data_form.is_valid():
                data = data_form.cleaned_data
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=timetable.xlsx'
                table = Table(data['lecture_data'], data['links'])
                excel_data = table.get_excel()
                response.write(excel_data)
                return response
            else:
                context = {'form': data_form}
                return render(request, 'data_input.html', context=context)
