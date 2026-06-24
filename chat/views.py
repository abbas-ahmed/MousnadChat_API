from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q, Max, OuterRef, Subquery
from .models import Message
from .serializers import UserSerializer, MessageSerializer , UserInfo_chatSerializer
from accounts.serializers import  UserInfoSerializer
from community.serializers import  CommunitySerializer

from accounts.models import UserProfile

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_users(request):
    """الحصول على قائمة المستخدمين الذين تم الدردشة معهم"""
    user = request.user
    print(user , '................')

    # الحصول على آخر رسالة لكل محادثة
    last_messages = Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).values('sender', 'receiver').annotate(
        last_time=Max('timestamp')
    )

    # الحصول على معرفات المستخدمين الذين تم الدردشة معهم
    user_ids = set()
    for msg in last_messages:
        if msg['sender'] == user.id:
            user_ids.add(msg['receiver'])
        else:
            user_ids.add(msg['sender'])

    # جلب معلومات المستخدمين مع آخر رسالة
    chat_users = []
    for user_id in user_ids:
        other_user = User.objects.get(id=user_id)
        last_message = Message.objects.filter(
            Q(sender=user, receiver=other_user) |
            Q(sender=other_user, receiver=user)
        ).order_by('-timestamp').first()

        unread_count = Message.objects.filter(
            sender=other_user,
            receiver=user,
            is_read=False
        ).count()

        user_ = UserProfile.objects.get(user=user_id)
        print(user_)
        uersInfo_community = UserInfo_chatSerializer(user_, many=False)
        print(uersInfo_community)

        chat_users.append({
            'user': UserSerializer(other_user).data,
            'userinfo': uersInfo_community.data,
            'last_message': MessageSerializer(last_message).data if last_message else None,
            'unread_count': unread_count
        })

    # ترتيب حسب آخر رسالة
    chat_users.sort(key=lambda x: x['last_message']['timestamp'] if x['last_message'] else '', reverse=True)

    return Response(chat_users)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_messages(request):
    """الحصول على رسائل المحادثة"""
    user = request.user
   # other_username = request.query_params.get('username')
    other_username = request.data.get('username')
    try:
        other_user = User.objects.get(username=other_username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    # جلب الرسائل بين المستخدمين
    messages = Message.objects.filter(
        Q(sender=user, receiver=other_user) |
        Q(sender=other_user, receiver=user)
    ).order_by('timestamp')

    # تحديث حالة القراءة للرسائل المستلمة
    Message.objects.filter(
        sender=other_user,
        receiver=user,
        is_read=False
    ).update(is_read=True)

    return Response({
        'messages': MessageSerializer(messages, many=True).data,
        'user_info': UserSerializer(other_user).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    """إرسال رسالة جديدة"""
    sender = request.user
    receiver_username = request.data.get('receiver')
    content = request.data.get('content')

    try:
        receiver = User.objects.get(username=receiver_username)
    except User.DoesNotExist:
        return Response({'error': 'Receiver not found'}, status=404)

    message = Message.objects.create(
        sender=sender,
        receiver=receiver,
        content=content
    )

    return Response(MessageSerializer(message).data, status=201)
