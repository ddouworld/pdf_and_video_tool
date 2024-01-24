import PyPDF2
import os

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
    #下面是再水印上覆盖pdf
    image_page = pdfReader.pages[0]
    if(w>=water_w or h>=water_h):
        print("ppt")
        image_page.scale_to(w, h)
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
    pdfWriter = PyPDF2.PdfWriter()  # 用于写pdf
    pdfReader = PyPDF2.PdfReader(path)  # 读取pdf内容

    a4_water_h,a4_water_w = get_pdf_size(a4_water_path)
    ppt_water_h,ppt_water_w = get_pdf_size(ppt_water_path)
    # 遍历pdf的每一页,添加水印
    for page in range(len(pdfReader.pages)):
        h,w = get_pdf_size(pdfReader.pages[page],True)
        if(get_pdf_type(pdfReader.pages[page],True)):
            page_pdf = add_watermark(a4_water_path, pdfReader.pages[page],w,h,a4_water_w,a4_water_h)
        else:
            page_pdf = add_watermark(ppt_water_path, pdfReader.pages[page], w, h,ppt_water_w,ppt_water_h)
        pdfWriter.add_page(page_pdf)

    with open(path[:-4]+'_1.pdf', 'wb') as target_file:
        pdfWriter.write(target_file)
    print("转换成功")
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
def delete_pdf_page(path,ad_path,num,is_insertion=False):
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
            if(page<num or page>num+10):
                page_pdf = pdfReader.pages[page]
                pdfWriter.add_page(page_pdf)
            if(page==num):
                pdfWriter.add_page(ad_pdf.pages[0])
    os.rename(path, path[:-4]+"_完整版.pdf")
    with open(path, 'wb') as target_file:
        pdfWriter.write(target_file)
