# import datetime
#
#
# def convert_formats(request):
#     start_time_date = request.get('start_time_0')
#     start_time_time = request.get('start_time_1')
#     expected_time_date = request.get('expected_finish_time_0')
#     expected_time_time = request.get('expected_finish_time_1')
#     due_date = request.get('due_date_0')
#     due_time = request.get('due_date_1')
#
#     start_time = datetime.datetime.strptime(start_time_date + ' ' + start_time_time, '%d %B, %Y %I:%M%p')
#     expected_finish_time = datetime.datetime.strptime(expected_time_date + ' ' + expected_time_time, '%d %B, %Y %I:%M%p')
#     due_date = datetime.datetime.strptime(due_date + ' ' + due_time, '%d %B, %Y %I:%M%p')
#
#     info = dict()
#     info['name'] = request.get('name')
#     info['course_name'] = request.get('course_name')
#     info['start_time_0'] = datetime.datetime.strptime(start_time.strftime('%Y-%m-%d'), '%Y-%m-%d')
#     info['start_time_1'] = datetime.datetime.strptime(start_time.strftime('%H:%M:%S'), '%H:%M:%S')
#     info['expected_finish_time_0'] = datetime.datetime.strptime(expected_finish_time.strftime('%Y-%m-%d'), '%Y-%m-%d')
#     info['expected_finish_time_1'] = datetime.datetime.strptime(expected_finish_time.strftime('%H:%M:%S'), '%H:%M:%S')
#     info['due_date_0'] = datetime.datetime.strptime(due_date.strftime('%Y-%m-%d'), '%Y-%m-%d')
#     info['due_date_1'] = datetime.datetime.strptime(due_date.strftime('%H:%M:%S'), '%H:%M:%S')
#     info['comments'] = request.get('comments')
#
#     return info
