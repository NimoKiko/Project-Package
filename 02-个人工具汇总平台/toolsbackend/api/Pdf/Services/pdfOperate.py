'''
PDF操作 业务代码
'''
import io
import os
import tempfile
from PyPDF2 import PdfReader, PdfWriter
from fastapi import File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pdf2docx import Converter


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


# 移除PDF权限限制（复制/打印/编辑等）
async def unlock_pdf_permissions(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="请上传PDF文件")

    try:
        # 读取文件到内存
        pdf_content = await file.read()

        # 创建pdf_reader
        pdf_reader = PdfReader(io.BytesIO(pdf_content))

        # 创建写入器
        writer = PdfWriter()

        # 如果PDF加密，尝试用空密码解密（绕过权限密码）
        if pdf_reader.is_encrypted:
            try:
                # 空密码可以绕过权限密码限制
                pdf_reader.decrypt("")
            except Exception:
                # 如果解密失败（可能是打开密码保护），仍然尝试继续
                pass

        # 复制所有页面到新的PDF（不设置加密）
        for page in pdf_reader.pages:
            writer.add_page(page)

        # 将解锁后的PDF写入字节流
        pdf_bytes = io.BytesIO()
        writer.write(pdf_bytes)
        pdf_bytes.seek(0)

        return pdf_bytes.getvalue()

    except Exception as e:
        # 打印异常信息
        print(f"发生异常: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理PDF时出错: {str(e)}")


# PDF转Word
async def convert_pdf_to_word(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="请上传PDF文件")

    try:
        # 读取PDF文件内容到内存
        pdf_content = await file.read()

        # 创建临时文件用于转换（pdf2docx需要文件路径）
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
            tmp_pdf.write(pdf_content)
            tmp_pdf_path = tmp_pdf.name

        # 创建临时输出文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_docx:
            tmp_docx_path = tmp_docx.name

        try:
            # 使用pdf2docx进行转换
            cv = Converter(tmp_pdf_path)
            cv.convert(tmp_docx_path, start=0, end=None)
            cv.close()

            # 读取转换后的docx文件
            with open(tmp_docx_path, 'rb') as f:
                docx_bytes = f.read()

            return docx_bytes

        finally:
            # 清理临时文件
            if os.path.exists(tmp_pdf_path):
                os.unlink(tmp_pdf_path)
            if os.path.exists(tmp_docx_path):
                os.unlink(tmp_docx_path)

    except Exception as e:
        print(f"PDF转Word发生异常: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF转Word失败: {str(e)}")
