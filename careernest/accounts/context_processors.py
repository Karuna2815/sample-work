from .models import Notification


def notifications(request):
    if request.user.is_authenticated:
        return {
            'notifications': Notification.objects.filter(user=request.user)[:5],
            'unread_count': Notification.objects.filter(user=request.user, is_read=False).count(),
        }
    return {}
