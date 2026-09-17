import sys
import subprocess
import os

#===================================PACKAGE=CHECKER================================================
try:
	import yt_dlp
except ImportError:
	print("core package 'yt_dlp' is missing, installing automatically...")
	try:
		subprocess.check_call([sys.executable, "-m", "pip", "install", "yt_dlp[default]",])
		print("installation complete, launching downloader...")
		import yt_dlp
	except Exception as e:
		print(f"failed to auto-install package: {e}")
		sys.exit(1)
#==================================================================================================

try:
	print("\033[96m" + "=" * 40, "Axo's Video Downloader", "=" * 40 + "\033[0m")

	if hasattr(sys, '_MEIPASS'):
		runtime_dir = sys._MEIPASS
	else:
		runtime_dir = os.getcwd()

	download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
	ydl_opts = {
		'format': 'bestvideo+bestaudio/best',
		'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
		'remote_components': ['ejs:github'],
		'extractor_args': {'youtube': {'player_client': ['tv', 'web_embedded', 'android'], 'formats': 'missing_pot'}},
		'nocache-dir': True,
		'restrictfilenames': True,
		'ffmpeg_location': runtime_dir,
		'js_runtimes': {'quickjs': {'path': os.path.join(runtime_dir, 'qjs')}}
	}

	multiple_downloads = input("Do you want to download multiple videos at once? (y/n): ").strip().lower()
	audio_only = input("Do you want to download audio only? (y/n): ").strip().lower()

	if audio_only == "y":
		ydl_opts['postprocessors'] = [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192'
		}]
		ydl_opts['format'] = 'bestaudio/best'
	elif audio_only == "n":
		pass
	else:
		if not audio_only:
			print("\033[91merror: choice cannot be empty\033[0m")
			sys.exit(1)
		else:
			print("\033[91merror: choice has to be y or n\033[0m")
			sys.exit(1)

	if multiple_downloads == 'y':
		raw_urls_input = input("Urls of the videos (seperated by commas): ").strip()

		if not raw_urls_input:
			print("\033[91merror: URL input cannot be empty.\033[0m")
			sys.exit(1)
		else:
			for url in raw_urls_input.split(","):
				url = url.strip()

				if not url:
					pass

				print(f"\nstarting download for: {url}...")
				try:
					with yt_dlp.YoutubeDL(ydl_opts) as ydl:
						ydl.download([url])
					print(f"\n\033[92msuccess, video saved to {download_dir}\033[0m")
				except Exception as e:
					print(f"\033[91merror downloading {url}: {e}\033[0m")
					sys.exit(1)
	elif multiple_downloads == 'n':
		url = input("Url of video: ").strip()

		if not url:
			print(f"\033[91merror: URL input cannot be empty\033[0m")
			sys.exit(1)

		print("\nstarting download...")

		try:
			with yt_dlp.YoutubeDL(ydl_opts) as ydl:
				ydl.download([url])
			print(f"\n\033[92msuccess, video saved to {download_dir}\033[0m")
		except Exception as e:
			print(f"\nerror: {e}")
	else:
		if not multiple_downloads:
			print(f"\033[91merror: choice cannot be empty\033[0m")
			sys.exit(1)
		else:
			print(f"\033[91merror: choice has to be y or n\033[0m")
			sys.exit(1)

except Exception as e:
	print("\n\033[91mcrash:\033[0m")
	print(e)

input("Press ENTER to close...")