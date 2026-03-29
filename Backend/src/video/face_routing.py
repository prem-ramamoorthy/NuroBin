import asyncio
import logging
from typing import cast
import uuid
from fastapi import APIRouter, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.rtcrtpreceiver import RemoteStreamTrack
import av
from numpy.typing import NDArray
from sqlmodel import Session

from src.video.face_identification import analyze_frame, analyze_emotion
from src.database.create_tables import engine

router = APIRouter()

pcs = set()


def process_frame(img: NDArray, patient_id: int):
    with Session(engine) as session:
        identities, count = analyze_frame(session, img, patient_id)
        logging.info(
            f"identities: {identities}, count: {count}"
        )  # TODO: Update the code to store the logs in an actual table in postgres

def process_emotion_frame(img: NDArray, patient_id: int):
    with Session(engine) as session:
        emotions = analyze_emotion(session, img, patient_id)
        logging.info(
            f"emotions: {emotions}"
        )  # TODO: Store real-time emotions in db for timeline

@router.post("/webrtc/emotion_offer")
async def emotion_offer(request: Request):
    params = await request.json()

    patient_id = params["patient_id"]
    offer = RTCSessionDescription(
        sdp=params["sdp"],
        type=params["type"],
    )

    pc = RTCPeerConnection()
    pc_id = f"EmotionPeerConnection({uuid.uuid4()})"
    pcs.add(pc)

    @pc.on("track")
    def on_track(track: RemoteStreamTrack):
        print("Emotion track received:", track.kind)

        if track.kind == "video":

            async def receive_video():
                nonlocal patient_id
                count = 0
                while True:
                    frame = await track.recv()
                    # Sample every 15th frame to avoid bottleneck
                    if count != 15:
                        count = (count + 1) % 16
                        continue
                    video_frame = cast(av.VideoFrame, frame)
                    img = video_frame.to_ndarray(format="bgr24")
                    await run_in_threadpool(process_emotion_frame, img, patient_id)

            asyncio.create_task(receive_video())

        @track.on("ended")
        async def on_ended():
            print("Emotion track ended")

    await pc.setRemoteDescription(offer)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return JSONResponse(
        {
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type,
        }
    )

@router.post("/webrtc/offer")
async def offer(request: Request):
    params = await request.json()

    patient_id = params[
        "patient_id"
    ]  # TODO: Later remember to add jwt auth to get the patient id instead of this which is unsecure in nature
    offer = RTCSessionDescription(
        sdp=params["sdp"],
        type=params["type"],
    )

    pc = RTCPeerConnection()
    pc_id = f"PeerConnection({uuid.uuid4()})"
    pcs.add(pc)

    @pc.on("track")
    def on_track(track: RemoteStreamTrack):
        print("Track received:", track.kind)

        if track.kind == "video":

            async def receive_video():
                nonlocal patient_id
                count = 0
                while True:
                    frame = await track.recv()
                    if count != 15:
                        count = (count + 1) % 16
                        continue
                    video_frame = cast(av.VideoFrame, frame)
                    img = video_frame.to_ndarray(format="bgr24")
                    await run_in_threadpool(process_frame, img, patient_id)

            asyncio.create_task(receive_video())

        @track.on("ended")
        async def on_ended():
            print("Track ended")

    await pc.setRemoteDescription(offer)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return JSONResponse(
        {
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type,
        }
    )
