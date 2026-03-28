'''
音频处理模块
'''
from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
# 音频处理库
from pydub import AudioSegment
import io
import subprocess
import os
import tempfile

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


@audio.post("/extractAudio")
async def extract_audio(file: UploadFile = File(...), type: str = Form(...)):
    '''
    从视频文件中提取音频
    '''
    # 读取视频文件数据
    video_data = await file.read()

    # 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix='.video') as temp_input:
        temp_input.write(video_data)
        temp_input_path = temp_input.name

    try:
        # 创建输出临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{type}') as temp_output:
            temp_output_path = temp_output.name

        try:
            # 使用 ffmpeg 提取音频
            # -i: 输入文件
            # -vn: 禁用视频
            # -acodec: 音频编码器 (使用 libmp3lame 为 mp3, pcm_s16le 为 wav, 等)
            codec_map = {
                'mp3': 'libmp3lame',
                'wav': 'pcm_s16le',
                'flac': 'flac',
                'ogg': 'libvorbis',
                'aac': 'aac'
            }
            codec = codec_map.get(type, 'copy')

            cmd = [
                'ffmpeg',
                '-i', temp_input_path,
                '-vn',  # 禁用视频
                '-acodec', codec,
                '-y',  # 覆盖输出文件
                temp_output_path
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                raise HTTPException(
                    status_code=500,
                    detail=f"音频提取失败: {result.stderr}"
                )

            # 读取输出文件
            with open(temp_output_path, 'rb') as f:
                output_data = f.read()

            output_buffer = io.BytesIO(output_data)
            output_buffer.seek(0)

            # 返回音频文件
            media_type_map = {
                'mp3': 'audio/mpeg',
                'wav': 'audio/wav',
                'flac': 'audio/flac',
                'ogg': 'audio/ogg',
                'aac': 'audio/aac'
            }
            media_type = media_type_map.get(type, 'audio/mpeg')

            return StreamingResponse(
                output_buffer,
                media_type=media_type,
                headers={
                    "Content-Disposition": f"attachment; filename=extracted_audio.{type}"
                }
            )

        finally:
            # 清理输出临时文件
            if os.path.exists(temp_output_path):
                os.remove(temp_output_path)

    finally:
        # 清理输入临时文件
        if os.path.exists(temp_input_path):
            os.remove(temp_input_path)
