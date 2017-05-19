from mylib.models import Notification

def notice_context(request):
    if request.user.is_authenticated:
        que= Notification.objects.filter(user=request.user)
        re_note = que.values_list('notice', flat=True)
        note=re_note[::-1]
        if note:
            if len(note)>5:
                notice=note[:5]
            else:
                notice=note
        else:
            notice=['Request Book issue for notifications',]
    else:
        notice = ['Request Book issue for notifications',]
        note=['please login']

    return {'notice':notice,'note':note}
