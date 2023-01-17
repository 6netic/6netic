from django.utils.html import escape


def update_list(request):
    """ Removes one id from the list in normal view """

    question_id, ids_list, new_ids_list = int(), [], []
    if request.GET.get('question_id'):
        question_id = int(request.GET.get('question_id'))
    ids_list = escape(request.GET.get('ids_list'))
    for i in ids_list:
        if i == '[' or i == ']' or i == ' ':
            pass
        else:
            new_ids_list.append(i)
    new_ids_list = ''.join(new_ids_list)
    new_ids_list = new_ids_list.split(',')
    ids_list = [int(i) for i in new_ids_list]
    ids_list.remove(question_id)
    return question_id, ids_list


def assisted_update_list(request):
    """ Removes one id from the list in assisted view """

    question_id, ids_list, new_ids_list = int(), [], []
    if request.POST.get('question_id'):
        question_id = int(request.POST.get('question_id'))
    ids_list = escape(request.POST.get('ids_list'))
    for i in ids_list:
        if i == '[' or i == ']' or i == ' ':
            pass
        else:
            new_ids_list.append(i)
    new_ids_list = ''.join(new_ids_list)
    new_ids_list = new_ids_list.split(',')
    ids_list = [int(i) for i in new_ids_list]
    ids_list.remove(question_id)
    return question_id, ids_list






































