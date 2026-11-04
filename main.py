import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="🎧 Streamlit 프로듀싱 워크스테이션",
    page_icon="🎹",
    layout="wide"
)

st.title("🎧 Streamlit 2옥타브 비트 & 코드 프로듀싱 스튜디오")
st.write("드럼 비트를 틀어놓고, **원클릭 코드 패드**와 피아노 멜로디를 조합하여 곡을 프로듀싱하고 녹음해 보세요!")

# HTML/CSS/JS 기반 프로듀싱 스튜디오 코드
piano_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body {
    background-color: #0f172a;
    color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15px;
  }
  
  /* 대시보드 컨트롤 박스 */
  .studio-panel {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: center;
    justify-content: center;
    background: #1e293b;
    padding: 12px 20px;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    margin-bottom: 15px;
    border: 1px solid #334155;
    width: 100%;
    max-width: 900px;
  }

  .control-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  label { font-weight: bold; font-size: 13px; color: #94a3b8; }
  
  select, button {
    padding: 8px 14px;
    border-radius: 8px;
    border: none;
    background: #334155;
    color: white;
    cursor: pointer;
    font-weight: bold;
    font-size: 13px;
    transition: all 0.2s ease;
  }
  
  select:hover, button:hover { background: #475569; transform: translateY(-1px); }

  /* 버튼 특별 스타일 */
  button.rec-btn { background: #e11d48; }
  button.rec-btn:hover { background: #f43f5e; }
  button.rec-btn.recording {
    background: #ff0055;
    animation: pulse 1.2s infinite;
  }

  button.beat-btn { background: #8b5cf6; }
  button.beat-btn:hover { background: #a78bfa; }
  button.beat-btn.active { background: #7c3aed; box-shadow: 0 0 10px #8b5cf6; }

  @keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(255, 0, 85, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(255, 0, 85, 0); }
    100% { box-shadow: 0 0 0 0 rgba(255, 0, 85, 0); }
  }

  audio { height: 34px; outline: none; border-radius: 8px; }

  /* 코드 패드 박스 */
  .chord-panel {
    display: flex;
    gap: 10px;
    justify-content: center;
    width: 100%;
    max-width: 900px;
    margin-bottom: 15px;
    background: #1e293b;
    padding: 12px;
    border-radius: 12px;
    border: 1px solid #334155;
  }
  
  .chord-btn {
    flex: 1;
    background: #0284c7;
    color: white;
    padding: 10px;
    font-size: 13px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
  }
  .chord-btn:hover { background: #0369a1; }

  /* 피아노 키보드 컨테이너 */
  .piano-container {
    position: relative;
    display: flex;
    justify-content: flex-start;
    background: #090d16;
    padding: 25px 20px 15px 20px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    border: 1px solid #1e293b;
    max-width: 100%;
    overflow-x: auto;
  }
  
  .piano {
    position: relative;
    display: flex;
    height: 195px;
  }
  
  .white-key {
    width: 42px;
    height: 180px;
    background: linear-gradient(to bottom, #ffffff 0%, #ebebeb 100%);
    border: 1px solid #cbd5e1;
    border-radius: 0 0 7px 7px;
    position: relative;
    cursor: pointer;
    box-shadow: inset 0 -5px 10px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.3);
    z-index: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
    padding-bottom: 10px;
    color: #334155;
    font-size: 10px;
    font-weight: bold;
  }
  .white-key.active {
    background: #cbd5e1;
    transform: translateY(2px);
    box-shadow: inset 0 -2px 5px rgba(0,0,0,0.2);
  }
  
  .black-key {
    width: 26px;
    height: 105px;
    background: linear-gradient(to bottom, #334155 0%, #0f172a 100%);
    position: absolute;
    border-radius: 0 0 5px 5px;
    cursor: pointer;
    box-shadow: 0 3px 8px rgba(0,0,0,0.5);
    z-index: 2;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
    padding-bottom: 6px;
    color: #fff;
    font-size: 9px;
  }
  .black-key.active {
    background: #475569;
    transform: translateY(2px);
  }
  
  .key-label { opacity: 0.6; font-size: 9px; }
  .key-bind { margin-top: 2px; color: #e11d48; font-weight: bold; }
</style>
</head>
<body>

<div class="studio-panel">
  <!-- 악기 선택 -->
  <div class="control-group">
    <label for="instrumentSelect">🎻 음색:</label>
    <select id="instrumentSelect">
      <option value="piano" selected>그랜드 피아노</option>
      <option value="synth">레트로 신디사이저</option>
      <option value="organ">성당 오르간</option>
      <option value="8bit">8비트 게임기</option>
    </select>
  </div>

  <!-- 비트 루프 -->
  <div class="control-group">
    <button id="beat1Btn" class="beat-btn">🥁 힙합 비트</button>
    <button id="beat2Btn" class="beat-btn">🪩 팝 비트</button>
  </div>

  <!-- 녹음 및 플레이어 -->
  <div class="control-group">
    <button id="recBtn" class="rec-btn">🎙️ 트랙 녹음</button>
  </div>

  <div class="control-group" id="audioPlaybackGroup" style="display: none;">
    <audio id="audioPlayback" controls></audio>
    <a id="downloadBtn" href="#" download="my_song_production.webm">
      <button style="background: #10b981;">💾 다운로드</button>
    </a>
  </div>
</div>

<!-- 원클릭 코드 패드 -->
<div class="chord-panel">
  <span style="font-size:12px; font-weight:bold; color:#38bdf8; align-self:center;">🎼 코드 패드:</span>
  <button class="chord-btn" onclick="playChord([261.63, 329.63, 392.00])">C Major</button>
  <button class="chord-btn" onclick="playChord([220.00, 261.63, 329.63])">A minor</button>
  <button class="chord-btn" onclick="playChord([174.61, 220.00, 261.63])">F Major</button>
  <button class="chord-btn" onclick="playChord([196.00, 246.94, 293.66])">G Major</button>
</div>

<div class="piano-container">
  <div class="piano" id="piano"></div>
</div>

<script>
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  const audioCtx = new AudioContext();
  const streamDestination = audioCtx.createMediaStreamDestination();
  let mediaRecorder;
  let audioChunks = [];
  let isRecording = false;

  const notes = [
    { note: 'C3', freq: 130.81, key: 'z', type: 'white' },
    { note: 'C#3', freq: 138.59, key: 's', type: 'black' },
    { note: 'D3', freq: 146.83, key: 'x', type: 'white' },
    { note: 'D#3', freq: 155.56, key: 'd', type: 'black' },
    { note: 'E3', freq: 164.81, key: 'c', type: 'white' },
    { note: 'F3', freq: 174.61, key: 'v', type: 'white' },
    { note: 'F#3', freq: 185.00, key: 'g', type: 'black' },
    { note: 'G3', freq: 196.00, key: 'b', type: 'white' },
    { note: 'G#3', freq: 207.65, key: 'h', type: 'black' },
    { note: 'A3', freq: 220.00, key: 'n', type: 'white' },
    { note: 'A#3', freq: 233.08, key: 'j', type: 'black' },
    { note: 'B3', freq: 246.94, key: 'm', type: 'white' },
    { note: 'C4', freq: 261.63, key: 'q', type: 'white' },
    { note: 'C#4', freq: 277.18, key: '2', type: 'black' },
    { note: 'D4', freq: 293.66, key: 'w', type: 'white' },
    { note: 'D#4', freq: 311.13, key: '3', type: 'black' },
    { note: 'E4', freq: 329.63, key: 'e', type: 'white' },
    { note: 'F4', freq: 349.23, key: 'r', type: 'white' },
    { note: 'F#4', freq: 369.99, key: '5', type: 'black' },
    { note: 'G4', freq: 392.00, key: 't', type: 'white' },
    { note: 'G#4', freq: 415.30, key: '6', type: 'black' },
    { note: 'A4', freq: 440.00, key: 'y', type: 'white' },
    { note: 'A#4', freq: 466.16, key: '7', type: 'black' },
    { note: 'B4', freq: 493.88, key: 'u', type: 'white' }
  ];

  const piano = document.getElementById('piano');
  const instrumentSelect = document.getElementById('instrumentSelect');
  const recBtn = document.getElementById('recBtn');
  const audioPlaybackGroup = document.getElementById('audioPlaybackGroup');
  const audioPlayback = document.getElementById('audioPlayback');
  const downloadBtn = document.getElementById('downloadBtn');

  const keyMap = {};
  let whiteCount = 0;
  
  notes.forEach((item) => {
    const keyEl = document.createElement('div');
    keyMap[item.key] = { element: keyEl, freq: item.freq };

    if (item.type === 'white') {
      keyEl.className = 'white-key';
      keyEl.innerHTML = `<span class="key-label">${item.note}</span><span class="key-bind">${item.key.toUpperCase()}</span>`;
      piano.appendChild(keyEl);
      whiteCount++;
    } else {
      keyEl.className = 'black-key';
      const leftPos = (whiteCount * 42) - 13;
      keyEl.style.left = `${leftPos}px`;
      keyEl.innerHTML = `<span class="key-bind">${item.key.toUpperCase()}</span>`;
      piano.appendChild(keyEl);
    }

    keyEl.addEventListener('mousedown', () => playNote(item.freq, keyEl));
    keyEl.addEventListener('mouseup', () => stopNote(keyEl));
    keyEl.addEventListener('mouseleave', () => stopNote(keyEl));
  });

  // 악기 파형 및 감쇄 설정
  function playNote(freq, element=null) {
    if (audioCtx.state === 'suspended') audioCtx.resume();
    if (element) element.classList.add('active');

    const osc = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();

    const inst = instrumentSelect.value;
    if (inst === 'piano') {
      osc.type = 'triangle';
      gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1.2);
    } else if (inst === 'synth') {
      osc.type = 'sawtooth';
      gainNode.gain.setValueAtTime(0.25, audioCtx.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.8);
    } else if (inst === 'organ') {
      osc.type = 'sine';
      gainNode.gain.setValueAtTime(0.4, audioCtx.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 1.5);
    } else if (inst === '8bit') {
      osc.type = 'square';
      gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.5);
    }

    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    osc.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    gainNode.connect(streamDestination);

    osc.start();
    osc.stop(audioCtx.currentTime + 1.5);
  }

  function stopNote(element) {
    if (element) element.classList.remove('active');
  }

  // 코드(3화음) 원클릭 재생 함수
  function playChord(freqArray) {
    freqArray.forEach(f => playNote(f));
  }

  // 드럼 루프 엔진 (Web Audio 신세사이저 비트)
  let beatInterval = null;
  let activeBeat = 0;

  function triggerKick(time) {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.frequency.setValueAtTime(120, time);
    osc.frequency.exponentialRampToValueAtTime(0.01, time + 0.15);
    gain.gain.setValueAtTime(0.8, time);
    gain.gain.exponentialRampToValueAtTime(0.01, time + 0.15);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    gain.connect(streamDestination);
    osc.start(time);
    osc.stop(time + 0.15);
  }

  function triggerSnare(time) {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(250, time);
    gain.gain.setValueAtTime(0.4, time);
    gain.gain.exponentialRampToValueAtTime(0.01, time + 0.1);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    gain.connect(streamDestination);
    osc.start(time);
    osc.stop(time + 0.1);
  }

  function toggleBeat(type) {
    if (audioCtx.state === 'suspended') audioCtx.resume();
    
    const b1 = document.getElementById('beat1Btn');
    const b2 = document.getElementById('beat2Btn');

    if (activeBeat === type) {
      clearInterval(beatInterval);
      beatInterval = null;
      activeBeat = 0;
      b1.classList.remove('active');
      b2.classList.remove('active');
      return;
    }

    clearInterval(beatInterval);
    activeBeat = type;
    b1.classList.toggle('active', type === 1);
    b2.classList.toggle('active', type === 2);

    let step = 0;
    const tempo = type === 1 ? 500 : 350; // 힙합 vs 팝 템포

    beatInterval = setInterval(() => {
      const now = audioCtx.currentTime;
      if (type === 1) { // 힙합 비트
        if (step % 4 === 0) triggerKick(now);
        if (step % 4 === 2) triggerSnare(now);
      } else { // 팝 비트
        if (step % 2 === 0) triggerKick(now);
        if (step % 4 === 1 || step % 4 === 3) triggerSnare(now);
      }
      step = (step + 1) % 8;
    }, tempo);
  }

  document.getElementById('beat1Btn').addEventListener('click', () => toggleBeat(1));
  document.getElementById('beat2Btn').addEventListener('click', () => toggleBeat(2));

  // 키보드 연주
  const activeKeys = {};
  window.addEventListener('keydown', (e) => {
    const k = e.key.toLowerCase();
    if (keyMap[k] && !activeKeys[k]) {
      activeKeys[k] = true;
      playNote(keyMap[k].freq, keyMap[k].element);
    }
  });

  window.addEventListener('keyup', (e) => {
    const k = e.key.toLowerCase();
    if (keyMap[k]) {
      activeKeys[k] = false;
      stopNote(keyMap[k].element);
    }
  });

  // 녹음 기능
  recBtn.addEventListener('click', () => {
    if (!isRecording) {
      audioChunks = [];
      mediaRecorder = new MediaRecorder(streamDestination.stream);
      
      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunks.push(e.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const audioUrl = URL.createObjectURL(audioBlob);
        audioPlayback.src = audioUrl;
        downloadBtn.href = audioUrl;
        audioPlaybackGroup.style.display = 'flex';
      };

      mediaRecorder.start();
      isRecording = true;
      recBtn.textContent = "⏹️ 녹음 중지";
      recBtn.classList.add('recording');
    } else {
      mediaRecorder.stop();
      isRecording = false;
      recBtn.textContent = "🎙️ 다시 녹음";
      recBtn.classList.remove('recording');
    }
  });
</script>
</body>
</html>
"""

components.html(piano_html, height=480)

st.divider()
st.subheader("🎧 프로듀싱 스튜디오 활용법")
st.markdown("""
1. **드럼 루프 켜기:** 상단 **`🥁 힙합 비트`** 또는 **`🪩 팝 비트`**를 누르면 비트가 무한 재생됩니다.
2. **코드 반주 누르기:** **`C Major`**, **`A minor`** 등 코드 패드를 누르면 3개 음이 풍성하게 어우러진 화음이 출력됩니다.
3. **악기 음색 선택:** **`그랜드 피아노`**, **`레트로 신디사이저`**, **`오르간`**, **`8비트`** 중 연주 분위기에 맞는 톤을 설정합니다.
4. **원트랙 멀티 녹음:** **`🎙️ 트랙 녹음`**을 켜면 재생되는 **비트 + 코드 + 피아노 멜로디**가 한 번에 깨끗하게 디지털 녹음되어 파일로 다운로드됩니다.
""")
