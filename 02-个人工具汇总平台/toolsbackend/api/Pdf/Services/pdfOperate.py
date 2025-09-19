'''
PDF操作 业务代码
'''
import io
from PyPDF2 import PdfReader, PdfWriter
from fastapi import File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse


# 按照文件的奇偶数页面 穿插合并文件
async def merge_pdf_alternating_even_odd(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    if file1.content_type != "application/pdf" or file2.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="请上传PDF文件")

    try:
        # 直接读取文件内容到内存
        pdf1_content = await file1.read()
        pdf2_content = await file2.read()

        pdf1_reader = PdfReader(io.BytesIO(pdf1_content))
        pdf2_reader = PdfReader(io.BytesIO(pdf2_content))

        # 获取两个PDF的页数
        pdf1_pages = len(pdf1_reader.pages)
        pdf2_pages = len(pdf2_reader.pages)

        # 确定最大页数
        max_pages = max(pdf1_pages, pdf2_pages)

        # 创建写入器
        writer = PdfWriter()

        # 交替添加页面
        for i in range(max_pages):
            # 添加第一个PDF的页面（如果存在）
            if i < pdf1_pages:
                writer.add_page(pdf1_reader.pages[i])

            # 添加第二个PDF的页面（如果存在）
            if i < pdf2_pages:
                writer.add_page(pdf2_reader.pages[i])

        # 创建内存字节流并写入PDF内容
        pdf_bytes = io.BytesIO()
        writer.write(pdf_bytes)
        pdf_bytes.seek(0)

        return pdf_bytes.getvalue()

    except Exception as e:
        # 打印异常信息
        print(f"发生异常: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理PDF时出错: {str(e)}")


# 逆序排列 PDF文件页面 API
async def reverse(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="请上传PDF文件")

    try:

        # 读取文件到内存
        pdf_content = await file.read()

        # 创建pdf_reader
        pdf_reader = PdfReader(io.BytesIO(pdf_content))

        # 创建写入器
        writer = PdfWriter()

        for i in range(len(pdf_reader.pages) - 1, -1, -1):
            writer.add_page(pdf_reader.pages[i])

            # 将逆序后的PDF写入字节流
        pdf_bytes = io.BytesIO()
        writer.write(pdf_bytes)
        pdf_bytes.seek(0)

        return pdf_bytes.getvalue()

    except Exception as e:
        # 打印异常信息
        print(f"发生异常: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理PDF时出错: {str(e)}")
