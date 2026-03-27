from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse

from .Services.pdfOperate import *

pdf = APIRouter()


# 按照文件的奇偶数页面 穿插合并文件 API
@pdf.post("/mergePdf")
async def merge_pdf(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    # 获取合并后 PDF 文件字节流数据
    pdf_bytes = await merge_pdf_alternating_even_odd(file1, file2)

    # 创建正确的生成器函数
    def iter_file():
        # 直接返回字节数据，而不是整数
        yield pdf_bytes

    return StreamingResponse(
        iter_file(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=merged_output.pdf"}
    )


# 逆序排列 PDF文件页面 API
@pdf.post("/reversePdf")
async def reverse_pdf(file: UploadFile = File(...)):
    pdf_bytes = await reverse(file)
    # 创建正确的生成器函数

    def iter_file():
        # 直接返回字节数据，而不是整数
        yield pdf_bytes

    return StreamingResponse(
        iter_file(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=merged_output.pdf"}
    )


# 移除PDF权限限制 API
@pdf.post("/unlockPdf")
async def unlock_pdf_route(file: UploadFile = File(...)):
    pdf_bytes = await unlock_pdf_permissions(file)

    def iter_file():
        yield pdf_bytes

    return StreamingResponse(
        iter_file(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=unlocked_output.pdf"}
    )


# PDF转Word API
@pdf.post("/convertToWord")
async def convert_to_word_route(file: UploadFile = File(...)):
    docx_bytes = await convert_pdf_to_word(file)

    def iter_file():
        yield docx_bytes

    return StreamingResponse(
        iter_file(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=converted.docx"}
    )
