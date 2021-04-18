from django import forms
from django.core.exceptions import ValidationError
from .excel import RAW_LEN, TIME_R, CLASS_NUM_R, \
    TABLE_LEN, NAME_T, CLASS_NUM_T, TEACHER_T, CLASSROOM_T, \
    LECTURE_LEN, TIME_S, CLASS_NUM_S, days, data_is_list, class_postfix


raw_error_message = [
    '입력이 형식에 맞지 않습니다. 밑의 지시사항을 읽어주세요.',
    '해결이 되지 않는다면 key 값을 가지고 20-017 김병권에게 연락해주세요.',
]


raw_error = ValidationError([ValidationError(message) for message in raw_error_message])


lecture_error_message = [
    '입력이 형식에 맞지 않습니다.',
    '"교과명, 교원, 수업 시간, 분반" 또는',
    '"교과명, 교원, 수업 시간, 분반, 교실" 형식인지 확인해 주세요.',
    '해결이 되지 않는다면 key 값을 가지고 20-017 김병권에게 연락해주세요.',
]


lecture_error = ValidationError([ValidationError(message) for message in lecture_error_message])


class RawForm(forms.Form):
    raw_data = forms.CharField(widget=forms.Textarea(attrs={'rows': 15, 'cols': 150}),
                               label='',
                               help_text='''<br>
                                <a href="https://students.ksa.hs.kr/" target="_blank">https://students.ksa.hs.kr/</a>
                                > 수강정보 > 수강신청현황<br>
                                본인의 수강신청과목 표를 붙여넣으면 됩니다.(머리글 행 제외)<br>
                                Firefox 사용자는 수강시간표를 붙여넣으면 자동으로 교실도 입력됩니다.''')

    def clean_raw_list(self):
        cleaned_data = self.cleaned_data
        data = cleaned_data.get('raw_data')
        data = data.strip()
        data = data.splitlines()
        for i in range(len(data)):
            data[i] = data[i].replace('\t', '  ')  # two spaces
            data[i] = data[i].split('  ')
            data[i] = list(filter(None, data[i]))
            if len(data[i]) != RAW_LEN:
                raise raw_error
            for j in range(len(data[i])):
                data[i][j] = data[i][j].strip()
            data[i][TIME_R] = data[i][TIME_R].split('|')
            for j in range(len(data[i][TIME_R])):
                if data[i][TIME_R][j][0] not in days or (not data[i][TIME_R][j][1:].isdigit()):
                    raise raw_error
            if not data[i][CLASS_NUM_R].isdigit():
                raise raw_error
        return cleaned_data.get('raw_data')

    def clean_raw_table(self):
        cleaned_data = self.cleaned_data
        data = cleaned_data.get('raw_data')
        data = data.strip()
        data = data.split('교시')
        for i in range(1, len(data)):
            if '\n' not in data[i] and data[i] != '':
                raise raw_error
            if i < len(data)-1:
                data[i] = data[i][:data[i].rfind('\n')]
            data[i] = data[i].split('\t')
            if len(data[i]) > len(days)+1:
                raise raw_error
            for j in range(0, len(data[i])):
                data[i][j] = data[i][j].strip()
                if data[i][j] != '':
                    data[i][j] = data[i][j].splitlines()
                    if len(data[i][j]) != TABLE_LEN:
                        raise raw_error
        return cleaned_data.get('raw_data')

    def clean_raw_data(self):
        cleaned_data = self.cleaned_data
        data = cleaned_data.get('raw_data')
        if data_is_list(data):
            return self.clean_raw_list()
        else:
            return self.clean_raw_table()


class DataForm(forms.Form):
    lecture_data = forms.CharField(widget=forms.Textarea(attrs={'rows': 15, 'cols': 50}),
                                   label='수업 정보')
    use_link = forms.BooleanField(label='온라인 수업', required=False)
    include_aa = forms.BooleanField(label='AA 모임', required=False)
    links = forms.CharField(widget=forms.TextInput(attrs={'size': 50}), label='온라인 수업 링크')

    def clean_lecture_data(self):
        clean_data = self.cleaned_data
        data = clean_data.get('lecture_data')
        data = data.splitlines()
        for i in range(len(data)):
            data[i] = data[i].split(',')
            if len(data[i]) not in LECTURE_LEN:
                raise lecture_error
            for j in range(len(data[i])):
                data[i][j] = data[i][j].strip()
            data[i][TIME_S] = data[i][TIME_S].split('/')
            for j in range(len(data[i][TIME_S])):
                if not (data[i][TIME_S][j][0] in days and data[i][TIME_S][j][1:].isdigit()):
                    raise lecture_error
            if not (data[i][CLASS_NUM_S].isdigit() or data[i][CLASS_NUM_S][:-2].isdigit()):
                raise lecture_error
        return clean_data.get('lecture_data')
