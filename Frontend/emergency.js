document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    ApiClient.setToken(null);
    window.location.href = 'index.html';
});

let peerConnection;
let localStream;

async function initPatients() {
    try {
        const patients = await ApiClient.getPatients();
        const sel = document.getElementById('patientSelect');
        if (patients) patients.forEach(p => {
            sel.innerHTML += `<option value="${p.id}">${p.name}</option>`;
        });
    } catch(e) { console.error(e); }
}

const config = {
    iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
};

document.getElementById('startCallBtn').addEventListener('click', async () => {
    const pId = document.getElementById('patientSelect').value;
    if(!pId) return ApiClient.notify("Select a patient to call", "warning");

    const status = document.getElementById('statusOverlay');
    status.textContent = "Connecting to device...";
    document.getElementById('callControls').style.display = 'flex';

    try {
        localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        document.getElementById('localVideo').srcObject = localStream;

        peerConnection = new RTCPeerConnection(config);
        
        localStream.getTracks().forEach(track => {
            peerConnection.addTrack(track, localStream);
        });

        peerConnection.ontrack = event => {
            status.style.display = 'none';
            document.getElementById('remoteVideo').srcObject = event.streams[0];
        };

        const offer = await peerConnection.createOffer();
        await peerConnection.setLocalDescription(offer);

        // Send offer to backend
        // Note: The /face/webrtc/offer endpoint expects: sdp, type, patient_id
        const resp = await ApiClient.request('/face/webrtc/offer', {
            method: 'POST',
            body: JSON.stringify({
                sdp: peerConnection.localDescription.sdp,
                type: peerConnection.localDescription.type,
                patient_id: parseInt(pId)
            })
        });

        // Backend should return answer SDP, we set it if correct
        if(resp && resp.sdp) {
            await peerConnection.setRemoteDescription(new RTCSessionDescription({
                type: resp.type || 'answer',
                sdp: resp.sdp
            }));
            ApiClient.notify("Call connected", "success");
        } else {
            status.textContent = "Waiting for patient to accept...";
            // In complete implementation, we might poll or use WebSocket for answer
        }

    } catch(err) {
        console.error("WebRTC Error:", err);
        status.textContent = "Connection failed. Check permissions.";
        ApiClient.notify("Camera/Microphone access required", "error");
    }
});

document.getElementById('endCallBtn').addEventListener('click', () => {
    if(peerConnection) peerConnection.close();
    if(localStream) localStream.getTracks().forEach(t => t.stop());
    document.getElementById('localVideo').srcObject = null;
    document.getElementById('remoteVideo').srcObject = null;
    document.getElementById('statusOverlay').style.display = 'block';
    document.getElementById('statusOverlay').textContent = "Call ended.";
    document.getElementById('callControls').style.display = 'none';
    ApiClient.notify("Call terminated", "success");
});

document.addEventListener('DOMContentLoaded', () => {
    initPatients();
});
