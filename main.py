import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="🎹 Streamlit 가상 피아노",
    page_icon="🎹",
    layout="wide"
)

st.title("🎹 Streamlit 온라인 가상 피아노")
st.write("마우스로 건반을 클릭하거나 키보드(`A S D F G H J...`)를 사용해 피아노를 연주해 보세요!")

# HTML/CSS/JS 기반 Web Audio API 피아노 코드
piano_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body {
    background-color: #1a1a2e;
    color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
  }
  .controls {
    margin-bottom: 25px;
    display: flex;
    gap: 15px;
    align-items: center;
    background: #16213e;
    padding: 12px 24px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
  }
  label { font-weight: bold; font-size: 14px; }
  select, button {
    padding: 8px 16px;
    border-radius: 8px;
    border: none;
    background: #0f3460;
    color: white;
    cursor: pointer;
    font-weight: bold;
    transition: 0.2s;
  }
  select:hover, button:hover { background: #e94560; }
  
  /* 피아노 키보드 컨테이너 */
  .piano-container {
    position: relative;
    display: flex;
    justify-content: center;
    background: #0f172a;
    padding: 30px 20px 20px 20px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  }
  .piano {
    position: relative;
    display: flex;
    height: 220px;
  }
  
  /* 흰색 건반 */
  .white-key {
    width: 50px;
    height: 200px;
    background: linear-gradient(to bottom, #ffffff 0%, #ebebeb 100%);
    border: 1px solid #ccc;
    border-radius: 0 0 8px 8px;
    position: relative;
    cursor: pointer;
    box-shadow: inset 0 -5px 10px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.3);
    z-index: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
    padding-bottom: 12px;
    color: #333;
    font-size: 12px;
    font-weight: bold;
  }
  .white-key.active {
    background: #e2e8f0;
    transform: translateY(2px);
    box-shadow: inset 0 -2px 5px rgba(0,0,0,0.2);
  }
  
  /* 검은색 건반 */
  .black-key {
    width: 32px;
    height: 120px;
    background: linear-gradient(to bottom, #333 0%, #000 100%);
    position: absolute;
    border-radius: 0 0 5px 5px;
    cursor: pointer;
    box-shadow: 0 3px 8px rgba(0,0,0,0.5);
    z-index: 2;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
    padding-bottom: 8px;
    color: #fff;
    font-size: 10px;
  }
  .black-key.active {
    background: #444;
    transform: translateY(2px);
  }
  
  .key-label { opacity: 0.7; font-size: 11px; }
  .key-bind { margin-top: 4px; color: #ff2e63; font-weight: bold; }
</style>
</head>
<body>

<div class="controls">
  <label for="waveType">음색 선택:</label>
  <select id="waveType">
    <option value="triangle" selected>기본 피아노 (Triangle)</option>
    <option value="sine">부드러운 음 (Sine)</option>
    <option value="sawtooth">전자 피아노 (Sawtooth)</option>
    <option value="square">8비트 오락실 (Square)</option>
  </select>
</div>

<div class="piano-container">
  <div class="piano" id="piano"></div>
</div>

<script>
  // Web Audio API 생성
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  const audioCtx = new AudioContext();

  // 음계 및 주파수 정의
  const notes = [
    { note: 'C4', freq: 261.63, key: 'a', type: 'white' },
    { note: 'C#4', freq: 277.18, key: 'w', type: 'black' },
    { note: 'D4', freq: 293.66, key: 's', type: 'white' },
    { note: 'D#4', freq: 311.13, key: 'e', type: 'black' },
    { note: 'E4', freq: 329.63, key: 'd', type: 'white' },
    { note: 'F4', freq: 349.23, key: 'f', type: 'white' },
    { note: 'F#4', freq: 369.99, key: 't', type: 'black' },
    { note: 'G4', freq: 392.00, key: 'g', type: 'white' },
    { note: 'G#4', freq: 415.30, key: 'y', type: 'black' },
    { note: 'A4', freq: 440.00, key: 'h', type: 'white' },
    { note: 'A#4', freq: 466.16, key: 'u', type: 'black' },
    { note: 'B4', freq: 493.88, key: 'j', type: 'white' },
    { note: 'C5', freq: 523.25, key: 'k', type: 'white' },
    { note: 'C#5', freq: 554.37, key: 'o', type: 'black' },
    { note: 'D5', freq: 587.33, key: 'l', type: 'white' },
    { note: 'D#5', freq: 622.25, key: 'p', type: 'black' },
    { note: 'E5', freq: 659.25, key: ';', type: 'white' }
  ];

  const piano = document.getElementById('piano');
  const waveTypeSelect = document.getElementById('waveType');
  const keyMap = {};

  let whiteCount = 0;
  
  // 피아노 건반 동적 생성
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
      // 검은 건반 위치 계산
      const leftPos = (whiteCount * 50) - 16;
      keyEl.style.left = `${leftPos}px`;
      keyEl.innerHTML = `<span class="key-bind">${item.key.toUpperCase()}</span>`;
      piano.appendChild(keyEl);
    }

    // 마우스 누름/떼기 이벤트
    keyEl.addEventListener('mousedown', () => playNote(item.freq, keyEl));
    keyEl.addEventListener('mouseup', () => stopNote(keyEl));
    keyEl.addEventListener('mouseleave', () => stopNote(keyEl));
  });

  // 소리 재생 함수
  function playNote(freq, element) {
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    
    element.classList.add('active');

    const osc = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();

    osc.type = waveTypeSelect.value;
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);

    // 자연스러운 소리 감쇄 (ADSR Envelope)
    gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1.2);

    osc.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    osc.start();
    osc.stop(audioCtx.currentTime + 1.2);
  }

  function stopNote(element) {
    element.classList.remove('active');
  }

  // 키보드 입력 연동
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
</script>
</body>
</html>
"""

# Streamlit에 피아노 컴포넌트 렌더링
components.html(piano_html, height=350)

st.divider()
st.subheader("💡 사용법")
st.markdown("""
* **마우스 연주:** 화면의 흰색/검은색 건반을 직접 클릭합니다.
* **키보드 연주:** 
  * 흰색 건반 (도~시~도): `A` `S` `D` `F` `G` `H` `J` `K` `L` `;`
  * 검은색 건반 (반음): `W` `E` `T` `Y` `U` `O` `P`
* **음색 변경:** 상단 메뉴에서 `8비트 오락실`, `전자 피아노` 등 원하는 소리로 변경해 보세요.
""")
