import sys
import subprocess
import os


try:
	import yt_dlp
except ImportError:
	print("core package 'yt_dlp' is missing, installing automatically...")
	try:
		subprocess.check_call([sys.executable, "-m", "pip", "install", "yt_dlp[default]", "-q"])
		print("installation complete, launching downloader...")
		import yt_dlp
	except Exception as e:
		print(f"failed to auto-install package: {e}")
		sys.exit(1)

try:
	print("=" * 40, " Axo's Video Downloader ", "=" * 40)
	url = input("Url of video: ").strip()

	if not url:
		print("error: url cannot be empty")
		sys.exit(1)

	download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

	ydl_opts = {
		'format': 'bestvideo+bestaudio/best',
		'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
		'remote_components': ['ejs:github'],
		'extractor_args': {'youtube': {'player_client': ['android']}},
		'nocache-dir': True
	}

	print("\nstarting download...")

	try:
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])
		print(f"\nsuccess, video saved to {download_dir}")
	except Exception as e:
		print(f"\nerror: {e}")
except Exception as e:
	print("\ncrash:")
	print(e)

input("Press ENTER to close...")