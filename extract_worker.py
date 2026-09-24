import os, sys, json, time, cv2
from pathlib import Path
import numpy as np
import mediapipe as mp

POSE_DIM, HAND_DIM, FACE_DIM = 33 * 4, 21 * 3, 468 * 3
FEAT_DIM = POSE_DIM + 2 * HAND_DIM
INCLUDE_FACE = True
FULL_DIM = FEAT_DIM + FACE_DIM

CACHE_DIR = Path('/Volumes/MacX/Sw/landmark_cache')
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def _frame_vector(res):
    if res.pose_landmarks:
        pose = np.array([[p.x, p.y, p.z, p.visibility] for p in res.pose_landmarks.landmark], np.float32).ravel()
        pose_hit = 1
    else:
        pose, pose_hit = np.zeros(POSE_DIM, np.float32), 0
    if res.left_hand_landmarks:
        lh = np.array([[p.x, p.y, p.z] for p in res.left_hand_landmarks.landmark], np.float32).ravel()
        lh_hit = 1
    else:
        lh, lh_hit = np.zeros(HAND_DIM, np.float32), 0
    if res.right_hand_landmarks:
        rh = np.array([[p.x, p.y, p.z] for p in res.right_hand_landmarks.landmark], np.float32).ravel()
        rh_hit = 1
    else:
        rh, rh_hit = np.zeros(HAND_DIM, np.float32), 0
    parts = [pose, lh, rh]
    face_hit = 0
    if INCLUDE_FACE:
        if res.face_landmarks:
            fc = np.array([[p.x, p.y, p.z] for p in res.face_landmarks.landmark], np.float32).ravel()
            face_hit = 1
            if fc.size != FACE_DIM: fc = np.resize(fc, FACE_DIM)
        else:
            fc = np.zeros(FACE_DIM, np.float32)
        parts.append(fc)
    return np.concatenate(parts), pose_hit, lh_hit, rh_hit, face_hit

def extract_clip(video_path, holistic):
    cap = cv2.VideoCapture(str(video_path))
    frames, hits = [], np.zeros(4, np.int64)
    while True:
        ok, frame = cap.read()
        if not ok: break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        vec, p, l, r, f = _frame_vector(holistic.process(rgb))
        frames.append(vec)
        hits += (p, l, r, f)
    cap.release()
    seq = (np.stack(frames).astype(np.float32) if frames else np.zeros((0, FULL_DIM), np.float32))
    n = max(len(frames), 1)
    q = {'n_frames': int(len(frames)),
         'pose_rate': float(hits[0] / n), 'lh_rate': float(hits[1] / n),
         'rh_rate': float(hits[2] / n), 'face_rate': float(hits[3] / n),
         'any_hand_rate': float(max(hits[1], hits[2]) / n),
         'both_hand_rate': float(min(hits[1], hits[2]) / n)}
    return seq, q

def main(classes):
    import pandas as pd
    inv = pd.read_csv('/Volumes/MacX/Sw/outputs/tables/inventory_study_corpus.csv')
    inv_sel = inv[inv['label'].isin(classes)]
    total = len(inv_sel)
    print(f"Worker for classes {classes}: {total} clips in scope.")
    
    with mp.solutions.holistic.Holistic(static_image_mode=False, model_complexity=1,
                                       refine_face_landmarks=False, smooth_landmarks=True,
                                       min_detection_confidence=0.5, min_tracking_confidence=0.5) as h:
        done = 0
        for idx, row in inv_sel.iterrows():
            cid = row['clip_id']
            cf = CACHE_DIR / f"{cid}.npy"
            mf = cf.with_suffix('.json')
            if cf.exists() and mf.exists():
                done += 1
                continue
            seq, q = extract_clip(row['path'], h)
            np.save(cf, seq)
            with open(mf, 'w') as f:
                json.dump(q, f)
            done += 1
            if done % 10 == 0 or done == total:
                print(f"[{','.join(classes)}] Processed {done}/{total} clips.")

if __name__ == '__main__':
    classes = sys.argv[1:]
    main(classes)
