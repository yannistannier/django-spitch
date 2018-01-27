import boto3
import uuid
from django.conf import settings
from .shared_task import shared_task
from apps.core.sync import SyncAsk, SyncUser
from apps.notification.utils import NotificationHandler
from apps.authentication.models import User
from apps.relation.models import Follow
from apps.ask.models import Ask
from apps.spitch.models import Spitch
from apps.feed.models import Feed

#remove when betatest is over
@shared_task
def new_user(user):
    user = User.objects.get(id=user)
    spitchs = Spitch.objects.filter(active=True).exclude(user__id=305).order_by('-created')[0:100]
    Feed.objects.bulk_create(
        [Feed(user=user, feed_type=1, content_object=spitch)
         for spitch in reversed(spitchs)]
    )


@shared_task
def follow_user(emitter, follow):
    emitter = User.objects.get(id=emitter)
    follow = User.objects.get(id=follow)
    NotificationHandler(emitter=emitter, type_name="follow_user", object=follow).send()

    spitchs = Spitch.objects.filter(user=follow, active=True).order_by('-created')[0:20]

    if spitchs.exists():
        if not Feed.objects.filter(user=emitter, feed_type=1, object_id=spitchs.first().id).exists():
            Feed.objects.bulk_create(
                [Feed(user=emitter, feed_type=1, content_object=spitch)
                 for spitch in reversed(spitchs)]
        )


@shared_task
def follow_all(emitter):
    user = User.objects.get(id=emitter)
    ids = user.facebook_friends \
        .exclude(friend_id__in=user.follows.values_list('follow_id', flat=True)) \
        .values_list('friend_id', flat=True)

    if ids:
        Follow.objects.bulk_create(
            [Follow(user=user, follow_id=x) for x in ids]
        )
        NotificationHandler(emitter=user, type_name="follow_all", object=ids).send()

        spitchs = Spitch.objects.filter(user__id__in=list(ids), active=True).order_by('created')
        Feed.objects.bulk_create(
            [Feed(user=user, feed_type=1, content_object=spitch)
             for spitch in spitchs]
        )

@shared_task
def ask(ask):
    ask = Ask.objects.get(id=ask)
    NotificationHandler(emitter=ask.user, type_name="ask", object=ask).send()
    if not ask.is_private():
        SyncAsk(ask.id).set_object(ask).create()

@shared_task
def sync_user(user, action):
    user = User.objects.get(id=user)
    if action == "create" :
        SyncUser(user.id).set_object(user).create()
    if action == "update":
        SyncUser(user.id).set_object(user).update()


@shared_task
def like_spitch(emitter, spitch):
    spitch = Spitch.objects.get(id=spitch)
    emitter = User.objects.get(id=emitter)
    NotificationHandler(emitter=emitter, type_name="like_spitch", object=spitch).send()




@shared_task
def new_spitch(spitch):
    spitch = Spitch.objects.get(id=spitch)

    client = boto3.client('elastictranscoder')

    prefix = "{}/spitch/{}/".format(spitch.user.id, spitch.id)
    key = "{}.mp4".format(str(uuid.uuid4()).replace("-", "")[:20])

    response = client.create_job(
        PipelineId='xxxxx',
        Input=
        {
            'Key': 'media/'+str(spitch.spitch),
            'FrameRate': 'auto',
            'Resolution': 'auto',
            'AspectRatio': 'auto',
            'Interlaced': 'auto',
            'Container': 'auto'
        },
        Output={
            'Key': key,
            'Rotate': 'auto',
            'PresetId': 'xxxxxx'
        },
        OutputKeyPrefix='media/'+prefix
    )

    spitch.spitch_transcoded.name = prefix+key
    spitch.save()

    Feed.objects.bulk_create(
        [Feed(user=f.user, feed_type=1, content_object=spitch)
            for f in spitch.user.followers.all()]
    )

    # No --------------------------------------
    # if not spitch.ask.is_private():
    #     receivers = spitch.ask.user.followers.exclude(
    #         user_id__in=Feed.objects.filter(feed_type=2, object_id=spitch.ask.id).values_list('user_id', flat=True)
    #     )
    #     Feed.objects.bulk_create(
    #         [Feed(user=f.user, feed_type=2, content_object=spitch.ask)
    #          for f in receivers]
    #     )
    # ----------------------------------------

    NotificationHandler(emitter=spitch.user, type_name="new_spitch", object=spitch).send()


