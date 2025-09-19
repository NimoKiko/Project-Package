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
