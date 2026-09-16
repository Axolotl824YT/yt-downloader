import sys
import subprocess
import os


#===================================PACKAGE=CHECKER================================================
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
#==================================================================================================

try:
	print("\033[96m" + "=" * 40, "Axo's Video Downloader", "=" * 40 + "\033[0m")

	download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
	ydl_opts = {
		'format': 'bestvideo+bestaudio/best',
		'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
		'remote_components': ['ejs:github'],
		'extractor_args': {'youtube': {'player_client': ['android']}},
		'nocache-dir': True
	}

	choice = input("Do you want to download multiple videos at once? (y/n): ").strip().lower()
	if choice == 'y':
		raw_urls_input = input("Urls of the videos (seperated by commas): ").strip()

		if not raw_urls_input:
			print("\033[91merror: URL input cannot be empty.\033[0m")
		else:
			for url in raw_urls_input.split(","):
				url = url.strip()

				if not url:
					continue

				print(f"\nstarting download for: {url}...")
				try:
					with yt_dlp.YoutubeDL(ydl_opts) as ydl:
						ydl.download([url])
					print(f"\n\033[92msuccess, video saved to {download_dir}\033[0m")
				except Exception as e:
					print(f"\033[91merror downloading {url}: {e}\033[0m")
	elif choice == 'n':
		url = input("Url of video: ").strip()

		if not url:
			print(f"\033[91merror: url cannot be empty\033[0m")
			sys.exit(1)

		print("\nstarting download...")

		try:
			with yt_dlp.YoutubeDL(ydl_opts) as ydl:
				ydl.download([url])
			print(f"\n\033[92msuccess, video saved to {download_dir}\033[0m")
		except Exception as e:
			print(f"\nerror: {e}")
	else:
		print(f"\033[91merror: choice cannot be empty\033[0m")

except Exception as e:
	print("\ncrash:")
	print(e)

input("Press ENTER to close...")