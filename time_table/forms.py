from django import forms


raw_data_example = '''예시
1 	수리정보과학부 	자연계열교과핵심 	수학2 	4 	1 	정명주 	월3|월4|화2|수1|목5 	3 	18 	15
2 	화학생물학부 	자연계열교과핵심 	생물학및실험2 	3 	1 	권창섭 	월5|수2|목1 	6 	18 	16
3 	인문예술학부 	인문계열교과핵심 	한국사의이해 	3 	1 	강재순 	월6|목2|금1 	3 	18 	15
4 	인문예술학부 	인문계열교과핵심 	미술 	2 	1 	박주영 	화6|화7 	2 	18 	17
5 	수리정보과학부 	자연계열교과심화 	자료구조 	3 	2 	김호숙 	화1|수4|금2 	1 	18 	18
6 	화학생물학부 	자연계열교과핵심 	화학및실험2 	3 	1 	탁주환 	목4|금5|금6 	5 	18 	17
7 	인문예술학부 	인문계열교과핵심 	체육2 	1 	1 	이종훈 	금3 	9 	18 	14
8 	인문예술학부 	인문계열교과핵심 	영어2 	3 	1 	Kevin Anderson 	화3|수6|목6 	8 	18 	16
9 	물리지구과학부 	자연계열교과핵심 	물리학및실험2 	3 	1 	이정훈 	월7|월8|화5|금4 	1 	18 	15'''


class RawForm(forms.Form):
    raw_data = forms.CharField(widget=forms.Textarea(attrs={'placeholder': raw_data_example, 'rows': 15, 'cols': 150}),
                               label='',
                               help_text='''<br><a href="https://students.ksa.hs.kr/" target="_blank">https://students.ksa.hs.kr/</a>
                                > 수강정보 > 수강신청현황<br>
                                수강신청과목 표를 붙여넣으면 됨(머리글 행 제외)<br>''')


class DataForm(forms.Form):
    lecture_data = forms.CharField(widget=forms.Textarea(attrs={'rows': 15, 'cols': 50}), label='수업 정보')
    links = forms.CharField(widget=forms.TextInput(attrs={'size': 50}), label='온라인 수업 링크')
