import time
import datetime
import random
import sys
import subprocess
import re
import json

from ios_touch_lib import * 

import instagram_dl_login.main

def post_video(s):
	unlock_phone(s)

	press(s, 110, 1240) #press instagram
	
	#wait for instagram to load
	time.sleep(10)

	#press search menu
	press(s, 210, 1300)
	time.sleep(1)

	#press search menu again because of touch glitch
	press(s, 210, 1300)
	time.sleep(5)

	#scroll up to reset feed
	touch(s, TOUCH_DOWN, 1, 400, 400)
	time.sleep(0.1)
	touch(s, TOUCH_MOVE, 1, 400, 800)
	time.sleep(0.1)
	touch(s, TOUCH_UP, 1, 400, 800)

	time.sleep(10)

	#press reels button
	press(s, 600, 400)
	time.sleep(5)

	#press share button
	press(s, 660, 1200)
	time.sleep(1)
	
	#press get link to clipboard
	press(s, 370, 1000)
	time.sleep(2)

	clipboard = subprocess.check_output("pbpaste", shell=True, text=True)

	argv = [sys.argv[0]] + [clipboard] #creates a custom argv to pass in to insta downloader with link 
	(username, description) = instagram_dl_login.main.main(argv) 

	#move video to files
	files_location = "/private/var/mobile/Containers/Data/Application/2D890CFA-40A8-4E05-9622-1CB6E11CED64/Documents"
	subprocess.run(f"mv ig_video.mp4 {files_location}/avideos/video.mp4", shell=True, capture_output=True, text=True, check=True)
	subprocess.run(f"chown mobile:mobile {files_location}/avideos/video.mp4", shell=True, capture_output=True, text=True, check=True)

	#press return arrow to exit video
	press(s, 60, 100)
	time.sleep(2)

	#press feed button
	press(s, 80, 1300)
	time.sleep(1)

	#leave instagram app
	press_home_button(s)
	time.sleep(0.5)

	#click files app
	press(s, 280, 1250)
	time.sleep(5)

	#sometimes app glitches so click anywhere to fix
	press(s, 450, 340)

	#click video
	press(s, 150, 340)
	time.sleep(2)

	#click share
	press(s, 70, 1300)
	time.sleep(2)

	#click save video
	press(s, 100, 1040)
	time.sleep(2)

	#click done
	press(s, 80, 100)
	time.sleep(2)

	subprocess.run(f"rm {files_location}/avideos/video.mp4", shell=True, capture_output=True, text=True, check=True)

	press_home_button(s)
	time.sleep(1.5)

	press(s, 110, 1240) #press instagram

	#wait for instagram to load
	time.sleep(5)

	#press feed button to solve touch glitch
	press(s, 80, 1300)
	time.sleep(1)

	#click share
	press(s, 500, 100)
	time.sleep(2)

	#click "Post"
	press(s, 480, 170)
	time.sleep(5)

	#click next
	press(s, 675, 50)
	time.sleep(5)

	#click continue
	press(s, 380, 1270)
	time.sleep(5)

	#click next
	press(s, 675, 1270)
	time.sleep(5)

	mentions = re.findall(r'@\w+', description)

	if username not in mentions:
		mentions.append(f"@{username}")

	mentions = list(set(mentions))

	mentions = " ".join(mentions)
	hash_tags = "" #ADD YOUR OWN HASH_TAGS HERE
	description = f"Credit: {mentions}\n{hash_tags}"

	subprocess.run(f'echo "{description}" | pbcopy', shell=True, capture_output=True, text=True, check=True)

	#click write caption
	press(s, 350, 800)
	time.sleep(1.5)

	#press top of screen because of touch glitch
	press(s, 300, 50) 
	time.sleep(1.5)

	#click again to show paste (on a different spot because of touch glitch)
	press(s, 550, 200)
	time.sleep(1.5)

	#click paste
	press(s, 50, 110) 
	time.sleep(2)

	#click empty space to quit keyboard
	press(s, 230, 600)
	time.sleep(3)
	
	#click share
	press(s, 500, 1230)	
	time.sleep(1)

	#click share again because touch glitch
	press(s, 500, 1230)
	time.sleep(60) #wait for video to post

	#like video just posted
	press(s, 600, 700)
	time.sleep(0.1)
	press(s, 600, 700)
	time.sleep(1.5)
	
	press_home_button(s)
	time.sleep(1.5)

	press_power_button(s)

	current_time = datetime.datetime.now().time()
	current_datetime = datetime.datetime.combine(datetime.datetime.today(), current_time)
	post_frequency = 12 #frequency in hours
	#posts every post_frequency starting midnight. Find next post time, and calculate sleep_time based off of it
	#next post time is taken from if current time is in between (h-1-post_frequency, h-1), then post time will be h 
	h = (((current_time.hour+1)%24 // post_frequency + 1) * post_frequency)%24
	if current_time < datetime.time(h, 0):
		target_datetime = datetime.datetime.combine(datetime.datetime.today(), datetime.time(h, 0))
	else:
		tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
		target_datetime = datetime.datetime.combine(tomorrow, datetime.time(h, 0))
	sleep_time = (target_datetime - current_datetime).total_seconds() - (random.random())*15*60	

	return sleep_time

def safe_run_script(s):
	try:
		while True:
			accurate_usleep(s, 1000000*int(post_video(s)))
	except:
		close_n_apps(s, 2)		
		time.sleep(0.1)
		press_power_button(s)
		time.sleep(1)
		safe_run_script(s)
	

def main():
	try:
		#s = getSocketToDevice("192.168.1.74", 6000)
		s = getSocketToDevice("127.0.0.1", 6000)
	#	wait = input("Wait 10 seconds? [y/n]")
	#	if wait == "y":
	#		print("Waiting 10 seconds before starting to give time to lock screen if ran from phone terminal")
	#		time.sleep(10)
		time.sleep(0.1)  # please sleep after connection.
		if len(sys.argv) > 1:
			wait_time = sys.argv[1]
		else:
			wait_time = 0
		print("Sleeping for: " + str(wait_time) + " seconds before starting", flush=True)
		accurate_usleep(s, 1000000*int(wait_time))

		
		safe_run_script(s)

			

	finally:
		s.close()

if __name__ == '__main__':
	main()

