import boto3
import uuid
import os
import textwrap
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from moviepy.editor import *

from django.conf import settings


import subprocess
import shlex
import json

def get_rotation(file_path_with_file_name):
    """
    Function to get the rotation of the input video file.
    Adapted from gist.github.com/oldo/dc7ee7f28851922cca09/revisions using the ffprobe comamand by Lord Neckbeard from
    stackoverflow.com/questions/5287603/how-to-extract-orientation-information-from-videos?noredirect=1&lq=1

    Returns a rotation None, 90, 180 or 270
    """
    cmd = "ffprobe -loglevel error -select_streams v:0 -show_entries stream_tags=rotate -of default=nw=1:nk=1"
    args = shlex.split(cmd)
    args.append(file_path_with_file_name)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
    ffprobe_output = subprocess.check_output(args).decode('utf-8')
    if len(ffprobe_output) > 0:  # Output of cmdis None if it should be 0
        ffprobe_output = json.loads(ffprobe_output)
        rotation = ffprobe_output

    else:
        rotation = 0

    return rotation

#v0.1
class Video(object):
    def __init__(self, file, user, id, ask, color=1):
        self.s3 = boto3.client('s3')
        self.user = user
        self.id = id
        self.ask = ask
        self.color = color
        self.file_path = "/tmp/{}.mp4".format(str(uuid.uuid4()))
        self.thumbnail_path = "/tmp/{}.jpg".format(str(uuid.uuid4()))
        self.color_path = "/tmp/{}.jpg".format(str(uuid.uuid4()))

        with open(self.file_path, 'wb') as open_file:
            open_file.write(file.file.read())

        self.perform_thumbnail()
        self.perform_save_thumbnail()

        self.set_foreground()
        self.set_background_for_thumb_color()
        self.perform_save_color_thumbnail()

        self.perform_delete()


    def set_foreground(self):
        self.foreground = Image.open(self.thumbnail_path)

    def set_background_for_thumb_color(self):
        background = "apps/spitch/theme/{}-{}.png".format(self.color, 800)
        self.background = Image.open(background)

    def perform_thumbnail(self):
        clip = VideoFileClip(self.file_path)
        self.set_size(clip.w, clip.h)
        # clip= clip.resize( (self.width,self.height) )
        rotation = get_rotation(self.file_path)
        if rotation == 90:  # If video is in portrait
            clip = clip.rotate(-90)
        elif rotation == 270:  # Moviepy can only cope with 90, -90, and 180 degree turns
            clip = clip.rotate(90)  # Moviepy can only cope with 90, -90, and 180 degree turns
        elif rotation == 180:
            clip = clip.rotate(180)
        # clip = clip.rotate(90)
        clip.save_frame(self.thumbnail_path, t=0.00)


    def perform_save_thumbnail(self):
        self.thumb_key = "{}/spitch/{}/thumb/{}.jpg".format(self.user, self.id, self.get_uid())
        file = open(self.thumbnail_path, 'rb')
        key = settings.MEDIAFILES_LOCATION+"/"+self.thumb_key
        self.s3.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key, Body=file, ContentType='image/jpeg')

    def perform_save_color_thumbnail(self):
        self.foreground.paste(self.background, (0, 0), self.background)
        self.foreground.save(self.color_path, "JPEG")

        self.color_key = "{}/spitch/{}/thumb/{}.jpg".format(self.user, self.id, self.get_uid())
        file = open(self.color_path, 'rb')
        key = settings.MEDIAFILES_LOCATION+"/"+self.color_key
        self.s3.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key, Body=file, ContentType='image/jpeg')

    def perform_delete(self):
        os.remove(self.thumbnail_path)
        os.remove(self.file_path)
        os.remove(self.color_path)

    def get_uid(self):
        return str(uuid.uuid4()).replace("-", "")[:20]

    def set_size(self, w, h):
        self.width = h if w > h else w
        self.height = w if w > h else h






#Class with fade effect
class Video2(object):
    def __init__(self, file, user, id, ask, color=1):
        self.s3 = boto3.client('s3')
        self.user = user
        self.id = id
        self.ask = ask
        self.color = color
        self.file_path = "/tmp/{}.mp4".format(str(uuid.uuid4()))
        self.video_path = "/tmp/{}.mp4".format(str(uuid.uuid4()))
        self.thumbnail_path = "/tmp/{}.jpg".format(str(uuid.uuid4()))
        self.color_path = "/tmp/{}.jpg".format(str(uuid.uuid4()))

        with open(self.file_path, 'wb') as open_file:
            open_file.write(file.file.read())

        self.perform_thumbnail()
        self.perform_save_thumbnail()

        self.set_foreground()
        self.set_background_for_thumb_color()
        self.perform_save_color_thumbnail()

        self.set_foreground()
        self.set_background()
        self.perfom_add_text_thumb()

        self.perform_merge()
        self.perform_upload()
        self.perform_delete()

    def perform_thumbnail(self):
        clip = VideoFileClip(self.file_path)
        self.set_size(clip.w, clip.h)
        clip= clip.resize( (self.width,self.height) )
        clip.save_frame(self.thumbnail_path, t=0.00)

    def perfom_add_text_thumb(self):
        self.foreground.paste(self.background, (0, 0), self.background)

        font_size = int(40 - (len(self.ask) / 20))
        wrap_width = int(((40-font_size) / 2 ) + 18)

        font = ImageFont.truetype('/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf',  font_size)  # 55
        draw = ImageDraw.Draw(self.foreground)
        lines = textwrap.wrap(self.ask, width=wrap_width)  # 20
        W, H = self.foreground.size

        hl = font.getsize(lines[0])[1]
        ht = (hl*len(lines))+(5*len(lines))
        y_text = ((H - ht) / 2)-110  # 400

        for line in lines:
            width, height = font.getsize(line)
            w, h = draw.textsize(line, font=font)
            m = (W - w) / 2
            draw.text((m, y_text), line, font=font, fill=(255, 255, 255))
            y_text += height + 5

        self.foreground.save(self.thumbnail_path, "JPEG")


    def perform_merge(self):
        print("---- perform_merge -------")
        clip = VideoFileClip(self.file_path)
        clip = clip.resize((self.width, self.height))

        image = ImageClip(self.thumbnail_path)
        image = image.set_position('center').set_duration(3)
        image = image.crossfadeout(1)

        thumb = ImageClip(self.color_path)
        thumb = thumb.set_position('center').set_duration(2)

        final_clip = CompositeVideoClip([
            clip.set_start(2),
            thumb,
            image.crossfadeout(1),
        ])

        final_clip.write_videofile(self.video_path, audio=True, audio_codec='aac', verbose=False)

    def perform_upload(self):
        self.video_key = "{}/spitch/{}/{}.mp4".format(self.user, self.id, self.get_uid())
        file = open(self.video_path, 'rb')
        key = settings.MEDIAFILES_LOCATION + "/" + self.video_key
        self.s3.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key, Body=file, ContentType='video/mp4')

    def perform_save_thumbnail(self):
        self.thumb_key = "{}/spitch/{}/thumb/{}.jpg".format(self.user, self.id, self.get_uid())
        file = open(self.thumbnail_path, 'rb')
        key = settings.MEDIAFILES_LOCATION+"/"+self.thumb_key
        self.s3.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key, Body=file, ContentType='image/jpeg')

    def perform_save_color_thumbnail(self):
        self.foreground.paste(self.background, (0, 0), self.background)
        self.foreground.save(self.color_path, "JPEG")

        self.color_key = "{}/spitch/{}/thumb/{}.jpg".format(self.user, self.id, self.get_uid())
        file = open(self.color_path, 'rb')
        key = settings.MEDIAFILES_LOCATION+"/"+self.color_key
        self.s3.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key, Body=file, ContentType='image/jpeg')

    def perform_delete(self):
        os.remove(self.thumbnail_path)
        os.remove(self.file_path)
        os.remove(self.video_path)
        os.remove(self.color_path)

    def get_uid(self):
        return str(uuid.uuid4()).replace("-", "")[:20]

    def get_url(self):
        return "https://"+settings.AWS_S3_CUSTOM_DOMAIN+"/"+settings.MEDIAFILES_LOCATION+"/"+self.video_key

    def set_foreground(self):
        self.foreground = Image.open(self.thumbnail_path)

    def set_background(self):
        size = self.height if self.height in [640, 800] else 800
        background = "apps/spitch/theme/{}-{}.png".format(self.color, size)
        self.background = Image.open(background)

    def set_background_for_thumb_color(self):
        background = "apps/spitch/theme/{}-{}.png".format(self.color, 800)
        self.background = Image.open(background)

    def set_size(self, w, h):
        self.width = h if w > h else w
        self.height = w if w > h else h




#first whitouht effect
class Video3(object):
    def __init__(self, file, user, id, ask, color=1):
        self.s3 = boto3.client('s3')
        self.user = user
        self.id = id
        self.ask = ask
        self.color = color
        self.file_path = "/tmp/{}.mp4".format(str(uuid.uuid4()))
        self.video_path = "/tmp/{}.mp4".format(str(uuid.uuid4()))
        self.thumbnail_path = "/tmp/{}.jpg".format(str(uuid.uuid4()))
        self.color_path = "/tmp/{}.jpg".format(str(uuid.uuid4()))

        with open(self.file_path, 'wb') as open_file:
            open_file.write(file.file.read())

        self.perform_thumbnail()
        self.perform_save_thumbnail()

        self.set_foreground()
        self.set_background_for_thumb_color()
        self.perform_save_color_thumbnail()

        self.set_foreground()
        self.set_background()
        self.perfom_add_text_thumb()

        self.perform_generate_video()
        self.perform_merge()
        self.perform_upload()
        self.perform_delete()

    def perform_thumbnail(self):
        clip = VideoFileClip(self.file_path)
        self.set_size(clip.w, clip.h)
        clip= clip.resize( (self.width,self.height) )
        clip.save_frame(self.thumbnail_path, t=0.00)

    def perfom_add_text_thumb(self):
        self.foreground.paste(self.background, (0, 0), self.background)

        font_size = int(40 - (len(self.ask) / 20))
        wrap_width = int(((40-font_size) / 2 ) + 18)

        font = ImageFont.truetype('/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf',  font_size)  # 55
        draw = ImageDraw.Draw(self.foreground)
        lines = textwrap.wrap(self.ask, width=wrap_width)  # 20
        W, H = self.foreground.size

        hl = font.getsize(lines[0])[1]
        ht = (hl*len(lines))+(5*len(lines))
        y_text = ((H - ht) / 2)-110  # 400

        for line in lines:
            width, height = font.getsize(line)
            w, h = draw.textsize(line, font=font)
            m = (W - w) / 2
            draw.text((m, y_text), line, font=font, fill=(255, 255, 255))
            y_text += height + 5

        self.foreground.save(self.thumbnail_path, "JPEG")

    def perform_generate_video(self):
        print("---- perform_generate_video -------")
        some_video_clip = ImageClip(self.thumbnail_path)
        some_video_clip.set_duration(3).write_videofile(self.video_path, fps=1, verbose=False)

    def perform_merge(self):
        print("---- perform_merge -------")
        clip1 = VideoFileClip(self.video_path)
        clip2 = VideoFileClip(self.file_path, audio=True)
        clip2 = clip2.resize((self.width, self.height))
        final_clip = concatenate_videoclips([clip1, clip2])
        final_clip.write_videofile(self.video_path, audio=True, audio_codec='aac', verbose=False)

    def perform_upload(self):
        self.video_key = "{}/spitch/{}/{}.mp4".format(self.user, self.id, self.get_uid())
        file = open(self.video_path, 'rb')
        key = settings.MEDIAFILES_LOCATION + "/" + self.video_key
        self.s3.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key, Body=file, ContentType='video/mp4')

    def perform_save_thumbnail(self):
        self.thumb_key = "{}/spitch/{}/thumb/{}.jpg".format(self.user, self.id, self.get_uid())
        file = open(self.thumbnail_path, 'rb')
        key = settings.MEDIAFILES_LOCATION+"/"+self.thumb_key
        self.s3.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key, Body=file, ContentType='image/jpeg')

    def perform_save_color_thumbnail(self):
        self.foreground.paste(self.background, (0, 0), self.background)
        self.foreground.save(self.color_path, "JPEG")

        self.color_key = "{}/spitch/{}/thumb/{}.jpg".format(self.user, self.id, self.get_uid())
        file = open(self.color_path, 'rb')
        key = settings.MEDIAFILES_LOCATION+"/"+self.color_key
        self.s3.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key, Body=file, ContentType='image/jpeg')

    def perform_delete(self):
        os.remove(self.thumbnail_path)
        os.remove(self.file_path)
        os.remove(self.video_path)
        os.remove(self.color_path)

    def get_uid(self):
        return str(uuid.uuid4()).replace("-", "")[:20]

    def get_url(self):
        return "https://"+settings.AWS_S3_CUSTOM_DOMAIN+"/"+settings.MEDIAFILES_LOCATION+"/"+self.video_key

    def set_foreground(self):
        self.foreground = Image.open(self.thumbnail_path)

    def set_background(self):
        size = self.height if self.height in [640, 800] else 800
        background = "apps/spitch/theme/{}-{}.png".format(self.color, size)
        self.background = Image.open(background)

    def set_background_for_thumb_color(self):
        background = "apps/spitch/theme/{}-{}.png".format(self.color, 800)
        self.background = Image.open(background)

    def set_size(self, w, h):
        self.width = h if w > h else w
        self.height = w if w > h else h