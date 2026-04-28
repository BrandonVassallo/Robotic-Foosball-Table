import sys
import cv2
import numpy
import time


# ---------------------------------------------------------------------------
# PUBLIC API EXPECTED BY Mod_Game_Class.py
#
#   vid, frame, v_width, v_height  = initalize_video(buffer, x_size, y_size)
#   frame, tracker                 = initalize_tracker(vid, frame, x_size, y_size,
#                                                       v_width, v_height, buffer, tgt_color)
#   count, tracker, fps, prev,
#   ball_pos, lost_counter         = tracking_alg(vid, buffer, tracker,
#                                                  x_size, y_size, v_width, v_height,
#                                                  tgt_color, count, prev, fps, lost_counter)
#
# NOTE FOR Mod_Game_Class.py  ──────────────────────────────────────────────
#   tracking_alg now returns 6 values (lost_counter added at the end).
#   Update update_PLAYING() to unpack it:
#
#       self.count, self.tracker, self.fps, self.prev, \
#       self.ball_pos, self.lost_counter = my_cv.tracking_alg(
#           self.vid, self.buffer, self.tracker,
#           self.x_size, self.y_size, self.v_width, self.v_height,
#           self.tgt_color, self.count, self.prev, self.fps, self.lost_counter)
#
#   Also initialise  self.lost_counter = 0  alongside self.count/fps/prev
#   in restart_cv().
# ---------------------------------------------------------------------------


# Pre-allocate the morphological kernel once at import time so it is not
# rebuilt on every BoundDetect call (saves a small but real alloc each frame).
_MORPH_KERNEL = numpy.ones((3, 3), numpy.uint8)


def initalize_video(buffer: int, x_size: int, y_size: int):
    """
    Open the default webcam, apply settings, warm up auto-exposure, and
    return the video capture object plus one warm-up frame.

    Returns: vid, frame, v_width, v_height
    """
    cv2.waitKey(20)
    vid = cv2.VideoCapture(0)

    if not vid.isOpened():
        print("No webcam found")
        sys.exit()
    else:
        print("Opening webcam...")

    # Uncomment to request MJPG codec for higher FPS on supported cameras:
    # vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    vid.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    vid.set(cv2.CAP_PROP_FPS,          30)

    # Stability settings
    vid.set(cv2.CAP_PROP_AUTO_EXPOSURE,  1)
    # vid.set(cv2.CAP_PROP_EXPOSURE,     -6)
    vid.set(cv2.CAP_PROP_AUTO_WB,        1)
    vid.set(cv2.CAP_PROP_WB_TEMPERATURE, 4500)

    v_width  = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    v_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print("Width :", v_width)
    print("Height:", v_height)
    print("FPS   :", vid.get(cv2.CAP_PROP_FPS))

    # Warm up auto-exposure (discard early frames)
    for _ in range(20):
        frame = pull_frame(vid, x_size, y_size)

    return vid, frame, v_width, v_height


def initalize_tracker(vid, frame, x_size, y_size, v_width, v_height, buffer, tgt_color,
                      show: bool = False):
    """
    Spin until the ball is detected, then create and initialise a MOSSE tracker.

    Parameters
    ----------
    show : bool
        When True (debug mode) shows two windows while searching:
          "Searching..." - live camera feed so you can verify the ball is in view
          "HSV Mask"     - raw colour mask so you can diagnose HSV range issues
                          (if the ball is visible but the mask is blank, the
                           HSV range in BoundDetect needs tuning)

    Returns: frame, tracker
    """
    print("Searching for ball...")
    bbox = findingROI(frame, x_size, y_size, buffer, tgt_color)

    while bbox is None:
        frame = pull_frame(vid, x_size, y_size)
        bbox  = findingROI(frame, x_size, y_size, buffer, tgt_color)

        if show:
            # Live feed — confirms camera is working and ball is in frame
            display = frame.copy()
            cv2.putText(display, "Searching for ball... (ESC to quit)",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.imshow("Searching...", display)

            # HSV mask — if ball is visible above but mask is dark, tune HSV range
            hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv,
                               numpy.array([145, 120, 120], dtype=numpy.uint8),
                               numpy.array([165, 255, 255], dtype=numpy.uint8))
            cv2.imshow("HSV Mask", mask)

        if cv2.waitKey(1) & 0xFF == 27:
            print("EXITING...")
            sys.exit()

    if show:
        cv2.destroyWindow("Searching...")
        cv2.destroyWindow("HSV Mask")

    print("Ball found - starting tracker.")
    tracker = cv2.legacy.TrackerCSRT.create()
    tracker.init(frame, bbox)
    return frame, tracker


def tracking_alg(vid: cv2.VideoCapture,
                 buffer: int,
                 tracker,
                 x_size: int,
                 y_size: int,
                 v_width: int,
                 v_height: int,
                 tgt_color: tuple,
                 count: int,
                 prev: float,
                 fps: float,
                 lost_counter: int,
                 show: bool = False):
    """
    Single-frame tracking step — call this in a loop from the game class.

    Inputs that must be fed back from the previous call:
        tracker, count, prev, fps, lost_counter

    Parameters
    ----------
    show : bool
        Set True to render a debug window (adds overhead; leave False on Pi).

    Returns
    -------
    count, tracker, fps, prev, ball_pos, lost_counter

    ball_pos : tuple(float, float) | None
        (x, y) centre of the ball in frame coordinates, or None if lost.
    """

    curr  = time.time()
    count += 1

    # ── Key input (1 ms poll; harmless with no display window open) ─────────
    key = cv2.waitKey(1) & 0xFF

    # ── Grab frame ──────────────────────────────────────────────────────────
    frame = pull_frame(vid, x_size, y_size)

    # ── Rolling FPS average ─────────────────────────────────────────────────
    dt  = curr - prev if curr > prev else 1e-6
    fps = 0.9 * fps + 0.1 * (1.0 / dt)

    # ── ESC → exit ──────────────────────────────────────────────────────────
    if key == 27:
        print("ESCAPED IN CV")
        sys.exit()

    # ── R → manual recalibrate ──────────────────────────────────────────────
    if key == ord('r'):
        tracker = _reinit_tracker(frame, x_size, y_size, buffer, tgt_color)
        lost_counter = 0

    # ── Run MOSSE tracker ───────────────────────────────────────────────────
    #   FIX: tracker.update() was previously called TWICE per frame
    #   (once above the key-check block, once inside the else branch),
    #   wasting CPU and corrupting MOSSE's internal state.
    ball_pos = None

    if tracker is not None:
        success, bbox = tracker.update(frame)
    else:
        success = False

    if success:
        lost_counter = 0
        x, y, w, h   = [int(v) for v in bbox]
        ball_pos      = (x + w / 2.0, y + h / 2.0)

        if show:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if count % 5 == 0:
                cv2.putText(frame, "Tracking",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        lost_counter += 1

        # Attempt colour-based re-detection after a few consecutive failures
        if lost_counter > 3:
            tracker = _reinit_tracker(frame, x_size, y_size, buffer, tgt_color)
            if tracker is not None:
                lost_counter = 0

        if show:
            cv2.putText(frame, "LOST",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    prev = curr

    # ── Optional debug display ──────────────────────────────────────────────
    if show:
        if count % 5 == 0:
            cv2.putText(frame, f"FPS: {int(fps)}",
                        (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"POS: {ball_pos}",
                        (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        cv2.imshow("Webcam", frame)

    return count, tracker, fps, prev, ball_pos, lost_counter


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _reinit_tracker(frame, x_size, y_size, buffer, tgt_color):
    """
    Try to find the ball with colour detection and create a fresh MOSSE tracker.
    Returns the tracker on success, or None on failure (caller keeps trying).
    """
    bbox = findingROI(frame, x_size, y_size, buffer, tgt_color)
    if bbox is None:
        return None
    tracker = cv2.legacy.TrackerCSRT.create()
    tracker.init(frame, bbox)
    return tracker


def findingROI(frame, x_size, y_size, buffer, tgt_color):
    """
    Use colour segmentation to locate the ball and return a bounding-box tuple
    (x, y, w, h) suitable for tracker.init(), or None if the ball is not found.

    Tunable constants
    -----------------
    AREA_MIN : smallest plausible ball area in pixels (reject noise)
    AREA_MAX : largest plausible ball area in pixels  (reject false positives)
    """
    AREA_MIN = 200      # ~14×14 px minimum  — tune to your ball size
    AREA_MAX = 2500   # ~50×50 px maximum

    top, bottom = BoundDetect(frame, tgt_color)
    if top is None or bottom is None:
        return None

    half_h = abs(bottom[1] - top[1]) // 2 + buffer

    tl_x = top[0] - half_h - buffer
    tl_y = top[1] - buffer
    br_x = top[0] + half_h + buffer
    br_y = bottom[1] + buffer

    box_w = abs(br_x - tl_x)
    box_h = abs(br_y - tl_y)

    if not (AREA_MIN <= box_w * box_h <= AREA_MAX):
        return None

    # Clamp to frame boundaries
    tl_x  = max(0, tl_x)
    tl_y  = max(0, tl_y)
    box_w = min(box_w, x_size - tl_x)
    box_h = min(box_h, y_size - tl_y)

    return (tl_x, tl_y, box_w, box_h)


def BoundDetect(frame, tgt_color=None, sensitivity=None):
    """
    Locate the magenta ball using HSV segmentation.

    Returns (top_of_object, bottom_of_object) as (x,y) tuples,
    or (None, None) if nothing is found.

    Performance notes for Pi5
    -------------------------
    - Morphological ops use a 3×3 kernel (down from 5×5) and 1 iteration
      (down from 2) — adequate for a foosball-sized blob, ~2× faster.
    - The Gaussian blur pass has been removed; the erode/dilate is sufficient
      to suppress single-pixel noise at this scale.
    - The kernel is pre-allocated at module level (_MORPH_KERNEL) so it is not
      re-created on every call.
    """

    # Convert to HSV (single-channel hue makes colour range checks cheap)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Magenta range — Hue ~145–165 in OpenCV's 0–179 scale
    lower = numpy.array([130, 60, 60], dtype=numpy.uint8)
    upper = numpy.array([175, 255, 255], dtype=numpy.uint8)

    mask = cv2.inRange(hsv, lower, upper)

    # One pass of erode then dilate is enough to kill single-pixel noise
    mask = cv2.erode( mask, _MORPH_KERNEL, iterations=1)
    mask = cv2.dilate(mask, _MORPH_KERNEL, iterations=1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None

    largest = max(contours, key=cv2.contourArea)
    if cv2.contourArea(largest) < 50:
        return None, None

    x, y, w, h = cv2.boundingRect(largest)
    return (x, y), (x + w, y + h)


def pull_frame(vid: cv2.VideoCapture, x_size: int, y_size: int):
    """
    Read one frame from the webcam, crop the borders, and resize to the
    requested dimensions.  Exits after 5 consecutive failed reads.
    """
    LEFT_CROP  = 95
    RIGHT_CROP = 88
    TOP_CROP   = 25
    BOT_CROP   = 35

    ok_count = 0
    while True:
        ok, frame = vid.read()
        if ok and frame is not None:
            break
        print("ERROR: frame not found")
        ok_count += 1
        if ok_count >= 5:
            print("TOO MANY FRAMES DROPPED. EXITING...")
            sys.exit()

    h, w = frame.shape[:2]
    frame = frame[TOP_CROP : h - BOT_CROP, LEFT_CROP : w - RIGHT_CROP]
    frame = cv2.resize(frame, (x_size, y_size))
    return frame


# ---------------------------------------------------------------------------
# movementVector — kept for reference, not called by the game loop
# ---------------------------------------------------------------------------
def movementVector(frame, object_center_curr, object_center_prev):
    """
    Draw and return the per-frame displacement vector.
    Not used in the main game loop; enable if you need velocity later.
    """
    VECTOR_SCALE = 1

    if object_center_curr is None or object_center_prev is None:
        return None

    dx = object_center_curr[0] - object_center_prev[0]
    dy = object_center_curr[1] - object_center_prev[1]

    pt1 = tuple(map(int, object_center_curr))
    pt2 = (int(object_center_curr[0] + dx * VECTOR_SCALE),
           int(object_center_curr[1] + dy * VECTOR_SCALE))

    frame = cv2.line(frame, pt1, pt2, (0, 0, 255), 3)
    return frame, (dx, dy)


# ---------------------------------------------------------------------------
# Debug utility — run this file directly to verify webcam + colour detection
# ---------------------------------------------------------------------------
def debug():
    """
    Standalone debug loop.  Run with:  python Jack_Tweaks_CV.py
    Press ESC to quit, R to force a colour-detection recalibration.

    initalize_video() opens the camera — do NOT also call VideoCapture(0)
    here or the two handles will fight over the device and the second open
    will fail with "can't open camera by index".
    """
    X_SIZE, Y_SIZE = 640, 360
    BUFFER         = 5
    TGT_COLOR      = (100, 35, 100)

    # initalize_video opens the camera, warms up auto-exposure, and returns
    # the VideoCapture object — use that handle for everything below.
    vid, frame, v_width, v_height = initalize_video(BUFFER, X_SIZE, Y_SIZE)

    frame, tracker = initalize_tracker(vid, frame, X_SIZE, Y_SIZE,
                                       v_width, v_height, BUFFER, TGT_COLOR,
                                       show=True)

    count = fps = prev = lost_counter = 0

    while True:
        count, tracker, fps, prev, ball_pos, lost_counter = tracking_alg(
            vid, BUFFER, tracker, X_SIZE, Y_SIZE, v_width, v_height,
            TGT_COLOR, count, prev, fps, lost_counter,
            show=True)   # show=True renders the debug window

        print(f"Ball pos: {ball_pos}  FPS: {fps:.1f}")

        if cv2.waitKey(1) & 0xFF == 27:
            break

    vid.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    debug()
