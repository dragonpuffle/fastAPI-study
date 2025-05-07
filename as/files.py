from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, StreamingResponse


app = FastAPI()


@app.post("/upload_files")
async def upload_file(uploaded_file: UploadFile):
    file = uploaded_file.file
    filename = uploaded_file.filename
    with open(filename, "wb") as f:
        f.write(file.read())


@app.post("/upload_many_files")
async def upload_many_files(uploaded_files: list[UploadFile]):
    for uploaded_file in uploaded_files:
        file = uploaded_file.file
        filename = uploaded_file.filename
        with open(filename, "wb") as f:
            f.write(file.read())


@app.get("/files/{filename}")
async def get_file_pc(filename: str):
    return FileResponse(filename)


def iterfile(filename: str):
    with open(filename, "rb") as f:
        while chunk := f.read(1024 * 1024):
            yield chunk


@app.get("/files_stream/{filename}")
async def get_file_pc_chunk(filename: str):
    return StreamingResponse(iterfile(filename), media_type="video/mp4")
