import numpy as np

GREEN_COLOR = Color(0, 255, 0)
RED_COLOR = Color(255, 0, 0)

led_pixels = np.array(GREEN_COLOR * 300)

while True:
    centers = []
    led_pixels = np.array(GREEN_COLOR * 300)

    if len(centers) == 2:
        if abs(centers[1] - centers[0]) < distance_pixels:
            cv.rectangle(frame, (centers[1], 0), (centers[0], height), (0, 0, 255), 2)

            led_pixels[:, :, int(centers[0] / ratio), int(centers[1] / ratio)] = RED_COLOR

    else:
        # loop i listen, udregn den absolutte forskel på index og index-1 + index og index+1
        for i in range(1, len(centers) - 1):
            if abs(centers[i] - centers[i + 1]) < distance_pixels:
                cv.rectangle(frame, (centers[i], 0), (centers[i + 1], height), (0, 0, 255), 2)

                led_pixels[:, :, centers[i], centers[i + 1]] = RED_COLOR

            if abs(centers[i] - centers[i - 1]) < distance_pixels:
                cv.rectangle(frame, (centers[i - 1], 0), (centers[i], height), (0, 0, 255), 2)

                led_pixels[:, :, int(centers[i - 1] / ratio), int(centers[i] / ratio)] = RED_COLOR

    data = json.dumps(
        {
            "led_array": led_pixels,
        }
    )
    s.send(data.encode())
