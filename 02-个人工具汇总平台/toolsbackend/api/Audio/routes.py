'''
音频处理模块
'''
import string
from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
# 音频处理库
from pydub import AudioSegment
import io

audio = APIRouter()


@audio.post("/fileFormateTransform")
async def audio_format_transform(file: UploadFile = File(...), type: str = Form(...)):

    audio_data = await file.read()
    # 2. 使用 pydub 加载音频（自动识别格式）
    audio = AudioSegment.from_file(io.BytesIO(
        audio_data), format=file.filename.split(".")[-1])

    # 3. 转换格式（例如：WAV → MP3）
    output_buffer = io.BytesIO()
    audio.export(output_buffer, format=type)  # 可选格式: "wav", "ogg", "flac"
    output_buffer.seek(0)  # 重置指针位置

    # 4. 返回处理后的音频文件
    return StreamingResponse(
        output_buffer,
        media_type="audio/mpeg",  # 根据输出格式调整
        headers={
            "Content-Disposition": f"attachment; filename=converted.{file.filename.split('.')[-1]}"}
    )
