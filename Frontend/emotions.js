document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    ApiClient.setToken(null);
    window.location.href = 'index.html';
});

document.addEventListener('DOMContentLoaded', async () => {
    const startEmotionBtn = document.getElementById('startEmotionBtn');
    if (startEmotionBtn) {
        startEmotionBtn.addEventListener('click', startLiveEmotionRecognition);
    }
});

async function startLiveEmotionRecognition() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        
        const contentDiv = document.getElementById('emotionResultContent');
        contentDiv.innerHTML = `
            <video id="emotionVideo" autoplay playsinline style="width: 100%; border-radius: var(--radius-md); background: #000;"></video>
            <p id="emotionStatus" class="mt-4" style="color: var(--primary);">Establishing secure connection to engine...</p>
            <button class="btn btn-secondary mt-2" id="stopEmotionBtn">Stop Camera</button>
        `;
        
        const videoEl = document.getElementById('emotionVideo');
        videoEl.srcObject = stream;
        
        const pc = new RTCPeerConnection({
            iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
        });
        
        document.getElementById('stopEmotionBtn').onclick = () => {
            stream.getTracks().forEach(t => t.stop());
            pc.close();
            contentDiv.innerHTML = '<p class="text-muted">Emotion scanner stopped.</p>';
        };
        
        stream.getTracks().forEach(track => pc.addTrack(track, stream));
        
        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);
        
        const res = await ApiClient.request('/webrtc/emotion_offer', {
            method: 'POST',
            body: JSON.stringify({
                patient_id: 1, // Demo ID
                sdp: pc.localDescription.sdp,
                type: pc.localDescription.type
            })
        });
        
        if (res && res.sdp) {
            await pc.setRemoteDescription(res);
            document.getElementById('emotionStatus').innerHTML = '<span style="color: var(--success); font-weight: 500;">Live emotion scanning active.</span> Monitoring...';
        } else {
            throw new Error("Invalid response from WebRTC engine");
        }
    } catch (e) {
        if (e.name === 'NotAllowedError' || e.name === 'NotFoundError') {
            ApiClient.notify('Camera access denied or no camera found.', 'error');
        } else {
            ApiClient.notify('Failed to start Live Camera: ' + (e.message || 'Check connection'), 'error');
        }
        console.error("Live Camera error:", e);
    }
}
