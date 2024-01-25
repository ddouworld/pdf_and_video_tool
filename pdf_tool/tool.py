import PyPDF2
import os
import shutil

def PDFtk_add_watermark(pdf_path,water_path,num):
    pdf_name = pdf_path.split("\\")[:-1]
    pdf_name = '\\'.join(pdf_name)
    # pdf_file_path = os.getcwd()+"\\temp\\"+pdf_name
    cmd = f'pdftk.exe "{pdf_path}" multistamp "{water_path}" output "{pdf_name}\\{num}_water.pdf"'
    # print(cmd)
    os.system(cmd)
def Merge_pdf(file_path,original_pdf,num):
    #先获取原始pdf的名字
    pdf_name = original_pdf.split("/")[-1][:-4]
    new_pdf_name = pdf_name+"_1.pdf"
    #先合并第一页和第二页
    pdf_1 = file_path+"\{}_water.pdf".format(1)
    pdf_2 = file_path + "\{}_water.pdf".format(2)
    temp_num = 1
    temp_name = file_path+"\{}_Merge.pdf".format(str(temp_num))
    cmd = 'pdftk.exe "{pdf_1}" "{pdf_2}" output "{new_pdf}"'.format(pdf_1=pdf_1,pdf_2=pdf_2,new_pdf=temp_name)
    os.system(cmd)
    for page in range(3,num+1):
            pdf_1 = temp_name
            pdf_2 = file_path +"\{}_water.pdf".format(page)
            temp_num+=1
            temp_name = file_path+"\{}_Merge.pdf".format(str(temp_num))
            cmd = 'pdftk.exe "{pdf_1}" "{pdf_2}" output "{new_pdf}"'.format(pdf_1=pdf_1, pdf_2=pdf_2, new_pdf=temp_name)
            os.system(cmd)
    os.rename(file_path+"\{}_Merge.pdf".format(str(temp_num)),file_path+"\\"+new_pdf_name)
    source = file_path+"\\"+new_pdf_name
    destination = os.path.dirname(original_pdf)
    shutil.copy(source, destination)


def add_watermark(water_file,page_pdf,w,h,water_w,water_h):
    """
    将水印pdf与pdf的一页进行合并
    :param water_file:
    :param page_pdf:
    :return:
    """
    mediabox = page_pdf.mediabox
    # print(mediabox)
    pdfReader = PyPDF2.PdfReader(water_file)
    #pdfReader.pages[0].scale_to(float(w), float(h))#将水印文件缩放到被加水印的pdf一样大小
    #下面这两行是再pdf上覆盖水印
    # page_pdf.transfer_rotation_to_content()
    # page_pdf.merge_page(pdfReader.pages[0],expand=True)
    #D:\tools\python_tool\pdftk.exe  D:\tools\python_tool\test\PDF测试(1)\PDF\PPT.pdf stamp D:\tools\python_tool\test\PDF测试(1)\water_pdf\比例测试_PPT.pdf output.pdf
    #下面是再水印上覆盖pdf
    image_page = pdfReader.pages[0]
    if(w>=water_w or h>=water_h):
        print("ppt")
        print(w,h)
        image_page.scale_to(float(w), float(h))
    else:
        print("a4")
        x = float(w/water_w)
        y = float(h/water_h)
        # print(x,y)
        op = PyPDF2.Transformation().scale(sx=x, sy=y)
        image_page.add_transformation(op)
    page_pdf.transfer_rotation_to_content()
    page_pdf.merge_page(image_page,expand=True)
    # page_pdf.mediabox = mediabox1
    return page_pdf
def add_watermark_2(path,a4_water_path,ppt_water_path):
    # pdfWriter = PyPDF2.PdfWriter()  # 用于写pdf

    pdfReader = PyPDF2.PdfReader(path)  # 读取pdf内容
    Split_pdf(path,5)
    pdf_name = path.split("/")[-1][:-4]
    pdf_file_path = os.getcwd()+"\\temp\\"+pdf_name #临时文件保存路径
    # 遍历pdf的每一页,添加水印
    # for page in range(len(pdfReader.pages)):
    #     h,w = get_pdf_size(pdfReader.pages[page],True)
    #     if(get_pdf_type(pdfReader.pages[page],True)):
    #         page_pdf = add_watermark(a4_water_path, pdfReader.pages[page],w,h,a4_water_w,a4_water_h)
    #     else:
    #         page_pdf = add_watermark(ppt_water_path, pdfReader.pages[page], w, h,ppt_water_w,ppt_water_h)
    #     pdfWriter.add_page(page_pdf)
    # with open(path[:-4]+'_1.pdf', 'wb') as target_file:
    #     pdfWriter.write(target_file)
    # print("转换成功")
    page_num = len(pdfReader.pages)
    for page in range(page_num):
        pdf_path = pdf_file_path+"\page{:0>5d}.pdf".format(page+1)
        # h,w = get_pdf_size(pdfReader.pages[page],True)
        if(get_pdf_type(pdfReader.pages[page],True)):
            PDFtk_add_watermark(pdf_path,a4_water_path,page+1)
        else:
            # page_pdf = add_watermark(ppt_water_path, pdfReader.pages[page], w, h,ppt_water_w,ppt_water_h)
            PDFtk_add_watermark(pdf_path,ppt_water_path,page+1)
    Merge_pdf(pdf_file_path,path,page_num)
    shutil.rmtree(pdf_file_path)
def Split_pdf(pdf_path,num):
    path = os.getcwd()
    pdf_name = pdf_path.split("/")[-1][:-4]
    if not os.path.exists(path+"/temp/"+pdf_name):
        os.makedirs(path+"/temp/"+pdf_name)
    cmd = r'pdftk.exe "{pdf_path}" burst output "{path}\temp\{pdf_name}\page%0{num}d.pdf"'.format(pdf_path=pdf_path,path=path,pdf_name=pdf_name,num=num)
    os.system(cmd)
def get_pdf_size(path,is_page=False):
    if is_page:
        page_1 = path
    else:
        pdf = PyPDF2.PdfReader(path)
        page_1 = pdf.pages[0]
    if page_1.get('/Rotate', 0) in [90, 270]:
        return page_1['/MediaBox'][2], page_1['/MediaBox'][3]
    else:
        return page_1['/MediaBox'][3], page_1['/MediaBox'][2]
def get_pdf_type(path,is_page=False):
    if is_page==True:
        page_1 = path

    else:
        pdf = PyPDF2.PdfReader(path)
        page_1 = pdf.pages[0]
    if page_1.get('/Rotate', 0) in [90, 270]:
        h = page_1['/MediaBox'][2]
        w = page_1['/MediaBox'][3]
        if(h>w):
            return 1
        else:
            return 0
    else:
        h = page_1['/MediaBox'][3]
        w = page_1['/MediaBox'][2]
        if(h>w):
            return 1
        else:
            return 0
def delete_pdf_page(path,ad_path,num,delete_num=10,is_insertion=False):
    pdfWriter = PyPDF2.PdfWriter()  # 用于写pdf
    pdfReader = PyPDF2.PdfReader(path)  # 读取pdf内容
    ad_pdf = PyPDF2.PdfReader(ad_path)
    # 遍历pdf的每一页
    if(is_insertion):
        for page in range(len(pdfReader.pages)):
            if (page == num):
                pdfWriter.add_page(ad_pdf.pages[0])
            page_pdf = pdfReader.pages[page]
            pdfWriter.add_page(page_pdf)
    else:
        for page in range(len(pdfReader.pages)):
            if(page<num or page>num+int(delete_num)):
                page_pdf = pdfReader.pages[page]
                pdfWriter.add_page(page_pdf)
            if(page==num):
                pdfWriter.add_page(ad_pdf.pages[0])
    os.rename(path, path[:-4]+"_完整版.pdf")
    with open(path, 'wb') as target_file:
        pdfWriter.write(target_file)
