# from moviepy.editor import VideoFileClip
# import moviepy.editor as mp
from ffmpeg import FFmpeg
import os
from PIL import Image
from moviepy.editor import VideoFileClip, concatenate_videoclips
#需要进行剪裁
def delete_video_time(video_path,ad_path,delete_time):
    vidoe_duration = get_video_duration(video_path)
    if delete_time>vidoe_duration:
        return -1
    clip1 = VideoFileClip(video_path).subclip(0, delete_time)
    delete_time_2 = min(vidoe_duration,delete_time+600)
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
    enable_expression = f"gte(t,{show_every_seconds})*lt(mod(t,{show_every_seconds}),{show_duration_seconds})"
    overlay_command = f"overlay=enable='{enable_expression}':x={x_offset}:y={y_offset}"
    return overlay_command

def fixed_watermarking(video_path,water_path,scale_size,show_every_seconds, show_duration_seconds,x,y):
    water_temp_path = water_path[:-4] + "_temp.png"
    ffmpeg_fix = (
        FFmpeg()
        .option("y")
        .input(water_path)
        .output(water_temp_path,
                vf="format=rgba,scale=iw*{}:-1".format(scale_size), q="0")
    )

    @ffmpeg_fix.on("completed")
    def on_completed():
        print("completed")
        video_path_complete = video_path[:-4] + "_1.mp4"
        ffmpeg_fix_1 = (
            FFmpeg()
            .option("y")
            .input(video_path)
            .input(water_temp_path)
            .output(video_path_complete,
                    {"c:a": "copy","filter_complex":get_ffmpeg_cmd(show_every_seconds, show_duration_seconds,x,y)})
        )

        @ffmpeg_fix_1.on("completed")
        def on_completed():
            print("固定水印完成")

        ffmpeg_fix_1.execute()
    ffmpeg_fix.execute()
def random_watermarking(video_path,water_path,scale_size,show_every_seconds, show_duration_seconds,is_fix=False):

    #cmd = 'ffmpeg -i input.mp4 -i water.jpg -filter_complex "overlay='if(ld(0), if(lte(mod(t/5,1),0.05),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(W-w));NAN)':'if(ld(0), if(lte(mod(t/5,1),0.05),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(H-h));NAN)'" temp.mp4'
    water_temp_path = water_path[:-4]+"_temp.png"
    t1 = show_every_seconds+show_duration_seconds
    t2 = show_every_seconds
    ffmpeg1 = (
        FFmpeg()
        .option("y")
        .input(water_path)
        .output(water_temp_path,
                vf="format=rgba,scale=iw*{}:-1".format(scale_size),q="0")
    )
    @ffmpeg1.on("completed")
    def on_completed():
        print("completed")
        if(is_fix==False):
            video_path_complete = video_path[:-4]+"_1.mp4"
        else:
            video_path_complete = video_path[:4]+"_2.mp4"
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(video_path)
            .input(water_temp_path)
            .output(video_path_complete,{"c:a": "copy","filter_complex":f"overlay='if(ld(0), if(lt(mod(t,{t1}),{t2}),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(W-w));NAN)':'if(ld(0), if(lt(mod(t,{t1}),{t2}),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(H-h));NAN)"})
        )
        @ffmpeg.on("completed")
        def on_completed():
            print("完成")
        ffmpeg.execute()
    ffmpeg1.execute()