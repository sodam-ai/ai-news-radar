# -*- mode: python ; coding: utf-8 -*-
"""AI News Radar — PyInstaller Spec File"""
import os
import sys
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

block_cipher = None

# 프로젝트 루트
PROJECT_ROOT = os.path.dirname(os.path.abspath(SPEC))

# Streamlit 관련 데이터 수집
st_datas, st_binaries, st_hiddenimports = collect_all('streamlit')

# 추가 hidden imports
extra_hiddenimports = [
    'streamlit.web.cli',
    'streamlit.web.bootstrap',
    'streamlit.runtime.scriptrunner',
    'streamlit.runtime.caching',
    'plotly',
    'plotly.express',
    'plotly.graph_objects',
    'pandas',
    'numpy',
    'feedparser',
    'bs4',
    'google.generativeai',
    'apscheduler',
    'apscheduler.schedulers.background',
    'apscheduler.triggers.interval',
    'dotenv',
    'fpdf2',
    'fpdf',
    'edge_tts',
    'pystray',
    'PIL',
    'PIL.Image',
    'PIL.ImageDraw',
    'webview',
    'plyer',
    'plyer.platforms.win',
    'plyer.platforms.win.notification',
    'tweepy',
    'requests',
    'json',
    'email',
    'email.mime',
    'email.mime.text',
    'email.mime.multipart',
    'multiprocessing',
    'multiprocessing.pool',
    'pkg_resources',
    'altair',
    'pyarrow',
    'pydeck',
    'tornado',
    'toml',
]

# 프로젝트 Python 모듈 (app.py, config.py, ai/, crawler/, etc.)
project_datas = [
    # 메인 앱 파일
    (os.path.join(PROJECT_ROOT, 'app.py'), '.'),
    (os.path.join(PROJECT_ROOT, 'config.py'), '.'),
    # 모듈 디렉토리
    (os.path.join(PROJECT_ROOT, 'ai'), 'ai'),
    (os.path.join(PROJECT_ROOT, 'crawler'), 'crawler'),
    (os.path.join(PROJECT_ROOT, 'reader'), 'reader'),
    (os.path.join(PROJECT_ROOT, 'export'), 'export'),
    (os.path.join(PROJECT_ROOT, 'utils'), 'utils'),
    (os.path.join(PROJECT_ROOT, 'sns'), 'sns'),
    (os.path.join(PROJECT_ROOT, 'bot'), 'bot'),
    # 데이터 파일
    (os.path.join(PROJECT_ROOT, 'data', 'preset_sources.json'), 'data'),
    # Streamlit 설정
    (os.path.join(PROJECT_ROOT, '.streamlit'), '.streamlit'),
    # 아이콘/에셋
    (os.path.join(PROJECT_ROOT, 'assets'), 'assets'),
]

# .env.example 포함 (실제 .env는 포함하지 않음 — 보안)
env_example = os.path.join(PROJECT_ROOT, '.env.example')
if os.path.exists(env_example):
    project_datas.append((env_example, '.'))

# 추가 패키지 데이터
plotly_datas = collect_data_files('plotly')
altair_datas = collect_data_files('altair')
pydeck_datas = collect_data_files('pydeck')

all_datas = st_datas + project_datas + plotly_datas + altair_datas + pydeck_datas
all_hiddenimports = st_hiddenimports + extra_hiddenimports
all_binaries = st_binaries

a = Analysis(
    [os.path.join(PROJECT_ROOT, 'launcher.py')],
    pathex=[PROJECT_ROOT],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'unittest',
        'test',
        'xmlrpc',
        # Heavy ML/CUDA packages not needed for this app
        'torch', 'torchvision', 'torchaudio',
        'xformers', 'triton',
        'cupy', 'cupy_backends',
        'cuda', 'cudnn',
        'tensorflow', 'keras',
        'scipy', 'sklearn', 'scikit-learn',
        'onnx', 'onnxruntime',
        'transformers', 'tokenizers', 'safetensors',
        'diffusers', 'accelerate',
        'huggingface_hub',
        'cv2', 'opencv',
        'yt_dlp',
        'IPython', 'jupyter', 'notebook', 'ipykernel',
        'matplotlib',
        'sympy',
        'cryptodome', 'Cryptodome',
        'brotli',
        'curl_cffi',
        'mutagen',
        'secretstorage',
        'PIL.ImageTk',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AI_News_Radar',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI 앱 (콘솔 창 숨김)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(PROJECT_ROOT, 'assets', 'icon.ico'),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AI_News_Radar',
)
