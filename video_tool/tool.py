# from moviepy.editor import VideoFileClip
# import moviepy.editor as mp
import time

from ffmpeg import FFmpeg
import os
from PIL import Image
from moviepy.editor import VideoFileClip, concatenate_videoclips
#需要进行剪裁
def delete_video_time(video_path,ad_path,delete_time,need_delete_time=600):
    vidoe_duration = get_video_duration(video_path)
    if delete_time>vidoe_duration:
        return -1
    clip1 = VideoFileClip(video_path).subclip(0, delete_time)
    delete_time_2 = min(vidoe_duration,delete_time+need_delete_time)
    if(delete_time_2<vidoe_duration):
        clip2 = VideoFileClip(video_path).subclip(delete_time_2, vidoe_duration)
        ad_video = VideoFileClip(ad_path).resize(clip1.size)
        final_clip = concatenate_videoclips([clip1,ad_video,clip2])
        # os.rename(video_path, video_path[:-4] + "_完整版.mp4")
        save_apth = video_path[:-4] + "_裁剪版.mp4"
        final_clip.write_videofile(save_apth)
    else:
        ad_video = VideoFileClip(ad_path).resize(clip1.size)
        final_clip = concatenate_videoclips([clip1, ad_video])
        # os.rename(video_path, video_path[:-4] + "_完整版.mp4")
        save_apth = video_path[:-4] + "_裁剪版.mp4"
        final_clip.write_videofile(save_apth)
#这个函数是直接合并，不进行剪裁
def delete_video_time_2(video_path,ad_path,delete_time):
    vidoe_duration = get_video_duration(video_path)
    if delete_time>vidoe_duration:
        return -1
    clip1 = VideoFileClip(video_path).subclip(0, delete_time)
    clip2 = VideoFileClip(video_path).subclip(delete_time, vidoe_duration)
    ad_video = VideoFileClip(ad_path).resize(clip1.size)
    final_clip = concatenate_videoclips([clip1,ad_video,clip2])
    #os.rename(video_path, video_path[:-4] + "_完整版.mp4")
    save_apth = video_path[:-4] + "_裁剪版.mp4"
    final_clip.write_videofile(save_apth)

def get_video_size(path):
    video = VideoFileClip(path)
    size = video.size
    # print(size)  # 获取分辨率
    return size
def get_img_size(path):
    file_path = path
    img = Image.open(file_path)
    w = img.width  # 图片的宽
    h = img.height  # 图片的高
    return w,h
def get_video_dimensions(file_path):
    clip = VideoFileClip(file_path)
    width = clip.size[0]
    height = clip.size[1]
    return width, height
def get_video_duration(path):
    clip = VideoFileClip(path)
    return clip.duration

def get_ffmpeg_cmd(show_every_seconds, show_duration_seconds,x_offset, y_offset):
    # FFmpeg命令构建，假设水印始终位于右下角
    # 根据show_every_seconds和show_duration_seconds调整时间表达式
    #enable_expression = f"gte(t,{show_every_seconds})*lt(mod(t,{show_every_seconds}),{show_duration_seconds})"
    cycle_duration =show_duration_seconds+show_every_seconds
    hidden_duration = show_every_seconds
    #enable_expression = f'between(t,0,{cycle_duration})*mod(t,{cycle_duration})>{hidden_duration}\'
    # overlay_command = f"overlay=enable='{enable_expression}':x={x_offset}:y={y_offset}"
    overlay_command = f"overlay=x=if(lt(mod(t,{cycle_duration}),{show_duration_seconds}),{x_offset},NAN):y={y_offset},overlay=x=if(gt(mod(t,{cycle_duration}),{show_duration_seconds}),{x_offset},NAN ) :y={y_offset}"
    return overlay_command

def fixed_watermarking(video_path,water_path,scale_size,show_every_seconds, show_duration_seconds,x,y,random_data):


    water_temp_path = water_path[:-4] + "_temp.png"
    r_x = x
    r_y = y
    video_size = get_video_size(video_path)
    video_w = video_size[0]
    video_h = video_size[1]
    ffmpeg_fix = (
        FFmpeg()
        .option("y")
        .input(water_path)
        .output(water_temp_path,
                vf="format=rgba,scale={w}:{h}".format(w=video_w*scale_size,h=video_h*scale_size), q="0")
    )

    @ffmpeg_fix.on("completed")
    def on_completed():
        print("固定水印,开始运行")

        cycle_duration = int(show_duration_seconds + show_every_seconds)
        img_w, img_h = get_img_size(water_temp_path)

        x = r_x + video_w - img_w
        y = int(r_y) + int(video_h / 2)
        video_path_complete = video_path[:-4] + "_1.mp4"
        #get_ffmpeg_cmd(show_every_seconds, show_duration_seconds,x,y)
        ffmpeg_fix_1 = (
            FFmpeg()
            .option("y")
            .input(video_path)
            .input(water_temp_path)
            .output(video_path_complete,
                    {"c:a": "copy","filter_complex":"overlay='x=if(gt(mod(t,{cycle_duration}),{show_every_seconds}),{x},NAN ):y={y}'".format(cycle_duration=cycle_duration,show_every_seconds=int(show_every_seconds),x=x,y=y)})
        )

        @ffmpeg_fix_1.on("completed")
        def on_completed():
            print("固定水印完成")
            # if(random_data!=""):
            #     random_water_path = random_data['random_water_path']
            #     scale_size = random_data['scale_size']
            #     show_every_seconds = random_data['show_every_seconds']
            #     show_duration_seconds = random_data['show_duration_seconds']
            #     random_watermarking(video_path[:-4]+"_1.mp4", random_water_path, scale_size, show_every_seconds, show_duration_seconds,
            #                         True)

        ffmpeg_fix_1.execute()
    ffmpeg_fix.execute()
def random_watermarking(video_path,water_path,scale_size,show_every_seconds, show_duration_seconds,is_fix=False):

    #cmd = 'ffmpeg -i input.mp4 -i water.jpg -filter_complex "overlay='if(ld(0), if(lte(mod(t/5,1),0.05),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(W-w));NAN)':'if(ld(0), if(lte(mod(t/5,1),0.05),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(H-h));NAN)'" temp.mp4'
    video_size = get_video_size(video_path)
    video_w = video_size[0]
    video_h = video_size[1]
    water_temp_path = water_path[:-4]+"_temp.png"
    t1 = int(show_every_seconds+show_duration_seconds)
    t2 = int(show_every_seconds)
    ffmpeg1 = (
        FFmpeg()
        .option("y")
        .input(water_path)
        .output(water_temp_path,
                vf="format=rgba,scale={w}:{h}".format(w=video_w*scale_size,h=video_h*scale_size),q="0")
    )
    @ffmpeg1.on("completed")
    def on_completed():
        print("随机水印,开始运行")
        video_path_complete = video_path[:-4]+"_1.mp4"
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(video_path)
            .input(water_temp_path)
            .output(video_path_complete,{"c:a": "copy","filter_complex":f"overlay='if(ld(0), if(lt(mod(t,{t1}),{t2}),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(W-w));NAN)':'if(ld(0), if(lt(mod(t,{t1}),{t2}),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(H-h));NAN)'"})
        )
        @ffmpeg.on("completed")
        def on_completed():
            print("随机水印完成")
        ffmpeg.execute()
    ffmpeg1.execute()
def fixed_and_random_watermarking(data):
    """首先先将随机水印缩放到需要的大小"""
    video_size = get_video_size(data['video_path'])
    video_w = video_size[0]
    video_h = video_size[1]
    water_temp_random_path = data['random_water_path'][:-4] + "_temp_random.png"
    t1 = int(data['show_every_seconds_random'] + data['show_duration_seconds_random'])
    t2 = int(data['show_every_seconds_random'])
    scale_size = data['scale_size_random']

    ffmpeg1 = (
        FFmpeg()
        .option("y")
        .input(data['random_water_path'])
        .output(water_temp_random_path,
                vf="format=rgba,scale={w}:{h}".format(w=video_w * scale_size, h=video_h * scale_size), q="0")
    )

    @ffmpeg1.on("completed")
    def on_completed():
        """缩放完毕后，对固定水印图片进行缩放"""
        video_size = get_video_size(data['video_path'])
        video_w = video_size[0]
        video_h = video_size[1]
        water_temp_fix_path = data['fix_water_path'][:-4] + "_temp_fix.png"
        # t1 = int(data['show_every_seconds_fix'] + data['show_duration_seconds_fix'])
        # t2 = int(data['show_every_seconds_fix'])
        scale_size = data['scale_size_fix']
        ffmpeg2 = (
            FFmpeg()
            .option("y")
            .input(data['fix_water_path'])
            .output(water_temp_fix_path,
                    vf="format=rgba,scale={w}:{h}".format(w=video_w * scale_size, h=video_h * scale_size), q="0")
        )
        @ffmpeg2.on("completed")
        def on_completed():
            print("随机和固定水印缩放完成")

            video_path_complete = data['video_path'][:-4] + "_1.mp4"
            data['cycle_duration_fix'] = int(data['show_duration_seconds_fix'] + data['show_every_seconds_fix'])
            img_w, img_h = get_img_size(water_temp_fix_path)
            x = data['x'] + video_w - img_w
            y = int(data['y']) + int(video_h / 2)
            ffmpeg = (
                FFmpeg()
                .option("y")
                .input(data['video_path'])
                .input(water_temp_random_path)
                .input(water_temp_fix_path)
                .output(video_path_complete, {"c:a": "copy",
                                              "filter_complex": f"overlay='if(ld(0), if(lt(mod(t,{t1}),{t2}),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(W-w));NAN)':'if(ld(0), if(lt(mod(t,{t1}),{t2}),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(H-h));NAN)',"+"overlay='x=if(gt(mod(t,{cycle_duration}),{show_every_seconds}),{x},NAN ):y={y}'".format(cycle_duration=data['cycle_duration_fix'],show_every_seconds=int(data['show_every_seconds_fix']),x=x,y=y)})
            )

            @ffmpeg.on("completed")
            def on_completed():
                print("水印完成")
            ffmpeg.execute()
        ffmpeg2.execute()

    ffmpeg1.execute()