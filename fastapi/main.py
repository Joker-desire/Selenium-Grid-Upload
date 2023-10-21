import os
import time
from typing import List

from fastapi import FastAPI, UploadFile, File, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI(docs_url=None, redoc_url=None)


@app.post("/upload", summary="上传图片")
async def upload_company_image(*, files: List[UploadFile] = File(...)):
    try:
        result = []
        for file in files:
            file_ = await file.read()
            # 日期文件夹
            date_dir = f"{time.strftime('%Y/%m/%d')}"
            # 图片存放路径
            image_dir = os.path.join("upload", date_dir)
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)
            # 文件名
            file_name = f"{time.perf_counter_ns()}.{file.filename.split('.')[-1]}"
            # 文件路径
            file_path = f"{image_dir}/{file_name}"
            with open(file_path, "wb+") as f:
                f.write(file_)
            file_path = os.path.join(date_dir, file_name)
            browser_file_path = os.path.join("/home/upload", file_path)
            data = {
                "file_path": file_path,
                "browser_file_path": browser_file_path,
            }
            result.append(data)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": "200",
                "msg": "上传成功",
                "data": jsonable_encoder(result)
            })
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "msg": "上传失败",
                "data": str(e)
            })


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=8080)
