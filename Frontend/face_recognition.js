document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    ApiClient.setToken(null);
    window.location.href = 'index.html';
});

document.addEventListener('DOMContentLoaded', async () => {
    const startFaceBtn = document.getElementById('startFaceBtn');
    if (startFaceBtn) {
        startFaceBtn.addEventListener('click', startLiveFaceRecognition);
    }
});

async function startLiveFaceRecognition() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        
        const contentDiv = document.getElementById('faceResultContent');
        contentDiv.innerHTML = `
            <video id="faceVideo" autoplay playsinline style="width: 100%; border-radius: var(--radius-md); background: #000;"></video>
            <p id="faceStatus" class="mt-4" style="color: var(--primary);">Establishing secure connection to engine...</p>
            <button class="btn btn-secondary mt-2" id="stopFaceBtn">Stop Camera</button>
        `;
        
        const videoEl = document.getElementById('faceVideo');
        videoEl.srcObject = stream;
        
        const pc = new RTCPeerConnection({
            iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
        });
        
        document.getElementById('stopFaceBtn').onclick = () => {
            stream.getTracks().forEach(t => t.stop());
            pc.close();
            contentDiv.innerHTML = '<p class="text-muted">Face scanner stopped.</p>';
        };
        
        stream.getTracks().forEach(track => pc.addTrack(track, stream));
        
        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);
        
        const res = await ApiClient.request('/webrtc/offer', {
            method: 'POST',
            body: JSON.stringify({
                patient_id: 1, // Demo ID
                sdp: pc.localDescription.sdp,
                type: pc.localDescription.type
            })
        });
        
        if (res && res.sdp) {
            await pc.setRemoteDescription(res);
            document.getElementById('faceStatus').innerHTML = '<span style="color: var(--success); font-weight: 500;">Live face scanning active.</span> Analyzing subjects...';
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
