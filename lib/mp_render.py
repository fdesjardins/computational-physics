from multiprocessing import Pool
import subprocess
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML

def mp_render(fig, ax, genfn, draw=plt.imshow, len_sec=10, fps=45, pool_size=2, update=None):
    start = time.time()
    def log(message):
        print(f'[{time.time() - start:3.3f}]: {message}')

    interval = 1000 / fps
    num_frames = int(np.ceil(len_sec * 1000 / interval)) + 1

    log('initializing figure...')
    width, height = fig.canvas.get_width_height()
    fig.canvas.draw()

    frames = []

    log('running computations...')
    if pool_size > 1:
        pool = Pool(pool_size)
        t_0 = 0
        for res in pool.map(genfn, range(0, num_frames)):
            frames.append(res)
    else:
        [frames.append(genfn(f)) for f in range(0, num_frames)]

    log('drawing frames...')
    images = [[draw(f)] for f in frames]
    ani = animation.ArtistAnimation(fig, images, interval=1, blit=True)
    frameList = list(ani.new_frame_seq())

    outf = 'movie.mp4'
    cmdstring = f'ffmpeg -pix_fmt argb -y -r {fps} -s {width}x{height} -f rawvideo -i - -qscale:v 2 -c:v libx264 {outf}'.split(' ')

    def draw_children(ax, artists):
        if type(artists) is tuple or type(artists) is list:
            [draw_children(ax, a) for a in artists]
        else:
            ax.draw_artist(artists)

    log('rendering final frames...')
    bg = fig.canvas.copy_from_bbox(ax.bbox)
    finalFrames = []
    for i,frame in enumerate(frameList):
        if update:
            update(i)
        else:
            ax.clear()

        fig.canvas.draw()
        bg = fig.canvas.copy_from_bbox(ax.bbox)
        fig.canvas.restore_region(bg)

        draw_children(ax, frame)

        fig.canvas.blit(ax.bbox)
        finalFrames.append(ax.figure.canvas.tostring_argb())

    log('piping frames to ffmpeg...')
    p = subprocess.Popen(cmdstring, stdin=subprocess.PIPE)
    for f in finalFrames:
        p.stdin.write(f)
    log('closing pipe...')
    p.communicate()

    log('done')
    return ani
