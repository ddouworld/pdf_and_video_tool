import time
from video_tool.tool import *
from ffmpeg import FFmpeg
import os
def random_watermarking(video_path,water_path,scale_size):
    #cmd = 'ffmpeg -i input.mp4 -i water.png -filter_complex "overlay='if(ld(0), if(lte(mod(t/5,1),0.05),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(W-w));NAN)':'if(ld(0), if(lte(mod(t/5,4),0.05),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(H-h));NAN)'" -c:a copy temp.mp4'
    water_temp_path = water_path[:-4]+"_temp.png"
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
        video_path_complete = video_path[:-4]+"_1.mp4"
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(video_path)
            .input(water_path)
            .output(video_path_complete,filter_complex="overlay=enable='gte(t,3)*lt(mod(t,3),2)':x=random(0,871):y=random(0,694)")
        )
        @ffmpeg.on("completed")
        def on_completed():
            print("完成")
        ffmpeg.execute()
    ffmpeg1.execute()
def get_ffmpeg_cmd(video_path,water_path,show_every_seconds, show_duration_seconds):
    # FFmpeg命令构建，根据视频尺寸设置随机位置，并调整时间表达式
    enable_expression = f"gte(t,{show_every_seconds})*lt(mod(t,{show_every_seconds}),{show_duration_seconds})"
    video_w,video_h = get_video_dimensions(video_path)
    water_w,water_h = get_img_size(water_path)
    W,H = video_w,video_h
    w,h = water_w,water_h
    # 假设视频宽度为W，高度为H，水印宽度为w，高度为h
    # 这里假设水印应位于视频内部，所以x和y范围分别限制在[0,W-w]和[0,H-h]
    # 构建overlay滤镜表达式
    overlay_expression = f"overlay=x='if(lt(mod(t,{show_every_seconds}),{show_duration_seconds}),{(W-w)}+trunc(random(-1)*(({W-w})/2));if(lt(mod(t,{show_every_seconds}),{show_every_seconds}-{show_duration_seconds}+1),{W-w});NAN)':y='if(lt(mod(t,{show_every_seconds}),{show_duration_seconds}),{(H-h)}+trunc(random(-1)*(({H-h})/2));if(lt(mod(t,{show_every_seconds}),{show_every_seconds}-{show_duration_seconds}+1),{H-h});NAN)':enable='between(t,n*{show_every_seconds},n*{show_every_seconds}+{show_duration_seconds})'"

    ffmpeg_command = [
        'ffmpeg',
        '-i', video_path,
        '-i', water_path,
        '-filter_complex', overlay_expression,
        "test.mp4"
    ]

    command_str = ' '.join(ffmpeg_command)

    print(command_str)
# get_ffmpeg_cmd("input.mp4","water_temp.png",3,2)
# add_watermark(3,2)
# random_watermarking("input.mp4","water.png",0.5)
# cmd ="""'ffmpeg -i input.mp4 -i water.png -filter_complex "overlay='if(ld(0), if(lt(mod(t,5),2),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(W-w));NAN)':'if(ld(0), if(lt(mod(t,5),2),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(H-h));NAN)'" -c:acopy temp.mp4'"""
# print(cmd)

def random_watermarking1(video_path,water_path,scale_size,show_every_seconds, show_duration_seconds):
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
        video_path_complete = video_path[:-4]+"_1.mp4"
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(video_path)
            .input(water_temp_path)
            .output(video_path_complete
                  ,{"c:a": "copy","filter_complex":f"overlay='if(ld(0), if(lt(mod(t,{t1}),{t2}),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(W-w));NAN)':'if(ld(0), if(lt(mod(t,{t1}),{t2}),st(0,0);NAN,ld(1)), st(0,1);ld(1);st(1,random(time(0))*(H-h));NAN)"} )
        )
        @ffmpeg.on("completed")
        def on_completed():
            print("完成")
        ffmpeg.execute()
    ffmpeg1.execute()
# random_watermarking1("input2.mp4","water.png",0.5,5,3)



from moviepy.editor import VideoFileClip, concatenate_videoclips
def delete_vidoe_time(video_path,ad_path,save_apth,delete_time):
    vidoe_duration = get_video_duration(video_path)
    if delete_time>vidoe_duration:
        return -1
    clip1 = VideoFileClip(video_path).subclip(0, delete_time)
    delete_time_2 = min(vidoe_duration,delete_time+600)
    if(delete_time_2<vidoe_duration):
        clip2 = VideoFileClip(video_path).subclip(delete_time_2, vidoe_duration)
        ad_video = VideoFileClip(ad_path).resize(clip1.size)
        final_clip = concatenate_videoclips([clip1,ad_video,clip2])
        final_clip.write_videofile(save_apth)
def delete_vidoe_time_2(video_path,ad_path,save_apth,delete_time):
    vidoe_duration = get_video_duration(video_path)
    if delete_time>vidoe_duration:
        return -1
    clip1 = VideoFileClip(video_path).subclip(0, delete_time)
    clip2 = VideoFileClip(video_path).subclip(delete_time, vidoe_duration)
    ad_video = VideoFileClip(ad_path).resize(clip1.size)
    final_clip = concatenate_videoclips([clip1,ad_video,clip2])
    final_clip.write_videofile(save_apth)
def Split_pdf(pdf_path,num):
    path = os.getcwd()
    pdf_name = pdf_path.split("\\")[-1][:-4]
    if not os.path.exists(path+"/temp/"+pdf_name):
        os.makedirs(path+"/temp/"+pdf_name)
    cmd = r'pdftk.exe "{pdf_path}" burst output "{path}\temp\{pdf_name}\page%0{num}d.pdf"'.format(pdf_path=pdf_path,path=path,pdf_name=pdf_name,num=num)
    os.system(cmd)
# Split_pdf(r"D:\tools\python_tool\dist\测试PPT.pdf",4)
# print("{:0>5d}".format(5))
a = ['ffmpeg', '-y', '-i', '"D:/tools/python_tool/test/测试文档/测试文档/视频/待处理/3 待处理_720P (2).mp4"', '-i', '"D:/tools/python_tool/test/测试文档/测试文档/视频/固定水印_temp.png"', '-c:a', 'copy', '-filter_complex', '"overlay=x=if(lt(mod(t,20),10),10,NAN ):y=10"', '"D:/tools/python_tool/test/测试文档/测试文档/视频/待处理/3 待处理_720P (2)_1.mp4"']
for i in a:
    print(i,end=" ")
#ffmpeg -y -i "D:/tools/python_tool/test/测试文档/测试文档/视频/待处理/3 待处理_720P (2).mp4" -i "D:/tools/python_tool/test/测试文档/测试文档/视频/固定水印_temp.png" -c:a copy -filter_complex overlay=x=1152:y=360:enable='between(t,0,15)*mod(t,15)>5' "D:/tools/python_tool/test/测试文档/测试文档/视频/待处理/3 待处理_720P (2)_1.mp4"
#command = f'ffmpeg -i "{video_file}" -vf "movie={watermark_file} [watermark]; [in][watermark] overlay=x=10:y=10:enable=\'between(t,0,{cycle_duration})*mod(t,{cycle_duration})>{hidden_duration}\'" -c:a copy "{output_file}"'

#ffmpeg -y -t 60 -i input.mp4 -i logo1.png -i logo2.png -filter_complex "overlay=x=if(lt(mod(t\,20)\,10)\,10\,NAN ):y=10,overlay=x=if(gt(mod(t\,20)\,10)\,W-w-10\,NAN ) :y=10" output.mp4


#ffmpeg -y -t 60 -i input.mp4 -i logo2.png -filter_complex "overlay=x=if(lt(mod(t\,20)\,10)\,10\,NAN ):y=10,overlay=x=if(gt(mod(t\,20)\,10)\,W-w-10\,NAN ) :y=10" output.mp4

#ffmpeg -y -i "D:/tools/python_tool/test/测试文档/测试文档/视频/待处理/3 待处理_720P (2).mp4" -i "D:/tools/python_tool/test/测试文档/测试文档/视频/固定水印_temp.png" -c:a copy -filter_complex "overlay=x=if(lt(mod(t\,20)\,10)\,10\,NAN ):y=10" "D:/tools/python_tool/test/测试文档/测试文档/视频/待处理/3 待处理_720P (2)_1.mp4"