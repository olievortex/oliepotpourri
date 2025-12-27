# oliedashcam
A very simple Python script to compress dashcam video for historical keeping.

I ran a dashcam every time I worked an Amazon Flex shift. Rather then overwriting old footage, I always downloaded the videos to my computer. I keep these files just in case a bogus legal claim emerges. I wrote the script to compress the files to save space on my storage. Now I can keep many months of video.

The script assumes you have [ffmpeg](https://www.ffmpeg.org/) in your path.

The output is 1 frame per second using the default compression quality.
