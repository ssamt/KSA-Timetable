import io
import xlsxwriter
from django.utils.translation import ugettext


NAME_R, TEACHER_R, TIME_R, CLASS_NUM_R = 3, 6, 7, 8  # index in raw string
NAME_S, TEACHER_S, TIME_S, CLASS_NUM_S = 0, 1, 2, 3  # index in readable string
NAME_X, CLASSROOM_X, CLASS_NUM_X, TEACHER_X = 0, 1, 2, 3  # index in excel data sheet
LINK_START_COLUMN = 4
days = ['월', '화', '수', '목', '금']
class_time = [
    '', '8:50~9:40', '9:50~10:40', '10:50~11:40', '11:50~12:40',
    '13:40~14:30', '14:40~15:30', '15:40~16:30', '16:40~17:30', '17:40~18:30',
    '19:30~20:20', '20:30~21:20',
]
colors = [
    '#FFA0A0', '#A0FFA0', '#A0A0FF',
    '#FFFFA0', '#FFA0FF', '#A0FFFF',
    '#FFD0A0', '#D0FFA0', '#D0A0FF',
    '#FFA0D0', '#A0FFD0', '#A0D0FF',
    '#A0E0E0', '#E0A0E0', '#E0E0A0',
    '#FFC0C0', '#C0FFC0', '#C0C0FF',
    '#FFFFC0', '#FFC0FF', '#C0FFFF',
    '#D0D0D0',
]
meals = {4: '점심', 9: '저녁'}  # meal after key-th period
# both 0-indexed
period_row = [0]  # row of nth period
meal_row = dict()  # meal in key-th row
row = 1
for i in range(1, len(class_time)):
    period_row.append(row)
    row += 2
    if i in meals.keys():
        meal_row[row] = meals[i]
        row += 1


# takes the raw string copied from https://students.ksa.hs.kr/
# returns a more readable string
def raw_to_str(data):
    data = data.strip()
    data = data.splitlines()
    for i in range(len(data)):
        data[i] = data[i].replace('\t', '  ')  # two spaces
        data[i] = data[i].split('  ')
        data[i] = list(filter(None, data[i]))
        for j in range(len(data[i])):
            data[i][j] = data[i][j].strip()
        print(data[i])
        data[i][TIME_R] = data[i][TIME_R].split('|')
        data[i][TIME_R] = '/'.join(data[i][TIME_R])
        data[i][CLASS_NUM_R] += '반'
        data[i] = ', '.join([data[i][NAME_R], data[i][TEACHER_R], data[i][TIME_R], data[i][CLASS_NUM_R]])
    data = '\n'.join(data)
    return data


class Lecture:
    # gets a line from raw_to_str
    def __init__(self, data):
        data = data.split(', ')
        data[TIME_S] = data[TIME_S].split('/')
        for i in range(len(data[TIME_S])):
            data[TIME_S][i] = [days.index(data[TIME_S][i][0]), int(data[TIME_S][i][1:])]
        data[CLASS_NUM_S] = data[CLASS_NUM_S][:-1]
        self.name = data[NAME_S]
        self.teacher = data[TEACHER_S]
        self.time = data[TIME_S]
        self.class_num = data[CLASS_NUM_S]

    # reverses __init__
    def __str__(self):
        string = [self.name, self.teacher, self.time, self.class_num]
        string[CLASS_NUM_S] += '반'
        for i in range(len(string[TIME_S])):
            string[TIME_S][i] = days[string[TIME_S][i][0]] + str(string[TIME_S][i][1])
        string[TIME_S] = '/'.join(string[TIME_S])
        string = ', '.join(string)
        return string


# combines the value of cells except empty ones
def period_formula(cells):
    string = '='
    for i in range(len(cells)):
        if i != 0:
            string += f'IF(OR(ISBLANK({cells[i-1]}), ISBLANK({cells[i]})),"",CHAR(10))&'
        string += f'IF(ISBLANK({cells[i]}),"",{cells[i]})&'
    string = string[:-1]
    return string


# creates hyperlink with the first non-empty cell
def link_formula(cells):
    string = '=if'
    for i in range(len(cells)):
        string = string.replace('if', f'IF(ISBLANK({cells[i]}),if,HYPERLINK({cells[i]}, {cells[i][:-1]}1))')
    string = string.replace('if', '""')
    return string


class Table:
    # gets data in raw_to_str output format
    # gets links in string separated by comma
    def __init__(self, data, link):
        self.lec = []
        data = data.strip()
        data = data.splitlines()
        for i in range(len(data)):
            self.lec.append(Lecture(data[i]))
        self.link = link.split(', ')

    def __str__(self):
        return '\n'.join(map(str, self.lec))

    # returns excel file data
    def get_excel(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        table = workbook.add_worksheet('시간표')
        table_format = workbook.add_format()  # format for all cells in timetable
        table_format.set_text_wrap()
        table_format.set_align('center')
        table_format.set_align('vcenter')
        table_format.set_border(1)
        # format for period cells, for each lecture
        period_format = [workbook.add_format() for i in range(len(self.lec))]
        for i in range(min(len(self.lec), len(colors))):
            period_format[i].set_bg_color(colors[i])
        for i in range(len(self.lec)):
            period_format[i].set_text_wrap()
            period_format[i].set_align('center')
            period_format[i].set_align('vcenter')
            period_format[i].set_border(1)
        # format for link cells, for each lecture
        link_format = [workbook.add_format() for i in range(len(self.lec))]
        for i in range(min(len(self.lec), len(colors))):
            link_format[i].set_bg_color(colors[i])
        for i in range(len(self.lec)):
            link_format[i].set_text_wrap()
            link_format[i].set_align('center')
            link_format[i].set_align('vcenter')
            link_format[i].set_color('blue')
            link_format[i].set_underline()
            link_format[i].set_border(1)

        # set column and row size, merge cells
        table.set_column(0, 0, 15)
        table.set_column(1, 1, 5)
        table.set_column(2, 2+len(days)-1, 15)
        table.set_row(0, 20)
        for i in range(1, len(period_row)):
            table.set_row(period_row[i], 60)
            table.set_row(period_row[i]+1, 20)
            table.merge_range(period_row[i], 0, period_row[i]+1, 0, '')
            table.merge_range(period_row[i], 1, period_row[i]+1, 1, '')
        for i in meal_row.keys():
            table.set_row(i, 40)
            table.merge_range(i, 0, i, 2+len(days)-1, '')

        # applying basic format to all cells
        for i in range(2*(len(class_time)-1)+len(meals)+1):
            for j in range(len(days)+2):
                table.write(i, j, '', table_format)

        # write data to excel
        for i in range(1, len(period_row)):
            table.write(period_row[i], 0, ugettext(class_time[i]), table_format)
            table.write(period_row[i], 1, ugettext(str(i)), table_format)
        for i in meal_row.keys():
            table.write(i, 0, ugettext(meal_row[i]), table_format)
        for i in range(len(days)):
            table.write(0, i+2, ugettext(days[i]), table_format)
        for i in range(len(self.lec)):
            for j in range(len(self.lec[i].time)):
                table.write_formula(period_row[self.lec[i].time[j][1]], self.lec[i].time[j][0]+2,
                                    period_formula([f'데이터!A{i+2}', f'데이터!D{i+2}', f'데이터!B{i+2}']),
                                    cell_format=period_format[i], value=f'{self.lec[i].name}\r\n{self.lec[i].teacher}')
                table.write_formula(period_row[self.lec[i].time[j][1]]+1, self.lec[i].time[j][0]+2,
                                    link_formula([f'데이터!{chr(ord("A")+k+4)}{i+2}' for k in range(len(self.link))]),
                                    cell_format=link_format[i], value='')

        # create 데이터 worksheet
        data = workbook.add_worksheet('데이터')
        data.write(0, NAME_X, ugettext('교과명'))
        data.write(0, CLASSROOM_X, ugettext('교실'))
        data.write(0, CLASS_NUM_X, ugettext('분반'))
        data.write(0, TEACHER_X, ugettext('교원'))
        for i in range(len(self.link)):
            data.write(0, LINK_START_COLUMN+i, ugettext(self.link[i]))
        for i in range(len(self.lec)):
            data.write(i+1, NAME_X, ugettext(self.lec[i].name))
            data.write(i+1, CLASS_NUM_X, ugettext(self.lec[i].class_num))
            data.write(i+1, TEACHER_X, ugettext(self.lec[i].teacher))
        workbook.close()
        excel_data = output.getvalue()
        return excel_data
