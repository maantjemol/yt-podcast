from pytube import Playlist, YouTube
from feedgen.feed import FeedGenerator
import os


playlist_url = "https://www.youtube.com/playlist?list=PLvp6IYp4bLbO7X9UeGhgjBoCqLDBoEPte"

def get_video_urls(playlist_url: str) -> list:
  p = Playlist(playlist_url)
  return p.video_urls

def read_history_file():
  videos = []
  with open('videos.txt', 'r') as f:
    for line in f:
      videos.append(line.strip())
  return videos

def write_history_file(videos: list):
  with open('videos.txt', 'w') as f:
    for video in videos:
      f.write(video + '\n')


def generate_podcast(podcasts):
  fg = FeedGenerator()
  fg.title('Youtube Podcast')
  fg.author( {'name':'John Doe','email':'john@example.de'} )
  fg.link( href='http://example.com', rel='alternate' )

  fg.subtitle('This is a cool feed!')
  fg.link( href='http://larskiesow.de/test.atom', rel='self' )
  fg.language('en')
  fg.load_extension('podcast')
  fg.podcast.itunes_category('Technology', 'Podcasting')
  for podcast in podcasts:
    fe = fg.add_entry()
    fe.id(f'http://lernfunk.de/media/654321/mp3/{podcast["id"]}.mp3')
    fe.title(podcast['title'])
    fe.description(podcast['title'])
    fe.enclosure(f'http://lernfunk.de/media/654321/mp3/{podcast["id"]}.mp3', 0, 'audio/mpeg')
  
  fg.rss_str(pretty=True)
  fg.rss_file('feed.xml')

def donwload_mp3(yt_url):
  youtube_video = YouTube(yt_url)
  audio = youtube_video.streams.get_audio_only()
  
  audio_download = audio.download(output_path='mp3', filename=youtube_video.video_id)
  base, ext = os.path.splitext(audio_download)
  new_file = base + '.mp3'
  os.rename(audio_download, new_file)

def main():
  current_videos = get_video_urls(playlist_url)
  history_videos = read_history_file()
  print(current_videos, history_videos)
  write_history_file(current_videos)


podcasts = [{'title':'Youtube Podcast', 'id':'1298234'},]

# generate_podcast(podcasts)

# donwload_mp3("https://www.youtube.com/watch?v=xxGEUFwO2io")

